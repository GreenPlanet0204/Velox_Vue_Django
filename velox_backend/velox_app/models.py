from __future__ import annotations

import base64
import json
import logging
from io import BytesIO
import datetime
from typing import Union, Type
from decimal import Decimal

import requests
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token
from redo import retriable
import pandas as pd
from constance import config

from .common import gcs
from .managers import CustomUserManager
from .options import *
from .forms import GCSBlobForm, GCSMultiForm
from .common import score_tabular_prediction, score_tabular_classification_prediction, create_task


def set_scores(obj: models.Model):
    """Set score for the concrete model instance
    Model (instance) need to have defined score_prob_fields field

    :param obj - concrete object for which score will be set
    """
    score_bins = ScoreBins.objects.all()
    score_data = dict()
    for score_bin in score_bins:
        score_data[score_bin.prob_field_name] = score_bin

    for score_field, prob_field in getattr(obj, 'score_prob_fields', []):
        score_bin = score_data.get(prob_field, None)
        prob_value = getattr(obj, prob_field, None)
        if prob_value is None:  # if there is no probability value set score to None (just in case)
            setattr(obj, score_field, prob_value)
            continue
        if score_bin is None:  # if there is ScoreBins object set score to None (just in case)
            setattr(obj, score_field, None)
            continue
        score = score_bin.get_score(prob_value)
        setattr(obj, score_field, score)


class CommonData(models.Model):
    """Common data """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.email


class GCSObject(models.Model):
    gcs_bucket = models.CharField('GCS Bucket', max_length=100, null=True, blank=True)
    gcs_filename = models.CharField('GCS Filename', max_length=200, null=True, blank=True)
    gcs_path = models.CharField('GCS Path', max_length=300, null=True, blank=True, unique=True)
    gcs_gs_uri = models.CharField('GCS GS URI', max_length=310, null=True, blank=True)

    @property
    def gcs_url(self):
        if self.gcs_bucket and self.gcs_path:
            bucket = gcs.bucket(self.gcs_bucket)
            blob = bucket.blob(self.gcs_path)
            signed_url = blob.generate_signed_url(expiration=datetime.timedelta(hours=2), method='GET', version='v4')
            return signed_url
        else:
            return ''

    gcs_url.fget.short_description = 'GCS URL'

    def get_gcs_gs_uri(self):
        return f'gs://{self.gcs_bucket}/{self.gcs_path}'

    class Meta:
        abstract = True


class GCSBlob(object):
    def __init__(self, bucket, filename, path=None):
        self.bucket = bucket
        self.filename = filename
        if not path:
            self.path = filename
        else:
            self.path = path

    @property
    def uri(self):
        return f'gs://{self.bucket}/{self.path}'

    @property
    def url(self):
        bucket = gcs.bucket(self.bucket)
        blob = bucket.blob(self.path)
        signed_url = blob.generate_signed_url(expiration=datetime.timedelta(hours=2), method='GET', version='v4')
        return signed_url

    @classmethod
    def create_from_uri(cls, gcs_uri):
        gcs_uri = gcs_uri.replace('gs://', '')
        split = gcs_uri.split('/')
        bucket = split[0]
        split_len = len(split)
        if split_len < 2:
            raise ValueError(f'Not valid GCS URI {gcs_uri}')
        if len(split) == 2:
            filename = split[-1]
            return GCSBlob(bucket=bucket, filename=filename)
        else:
            filename = split[-1]
            path = "/".join(split[1:])
            return GCSBlob(bucket=bucket, filename=filename, path=path)

    def download_as_bytes(self):
        if self.bucket and self.path:
            bucket = gcs.bucket(self.bucket)
            blob = bucket.blob(self.path)
            return blob.download_as_bytes()

    def __str__(self):
        return self.uri

    def to_dict(self):
        return {
            'bucket': self.bucket,
            'filename': self.filename,
            'path': self.path,
            'uri': self.uri,
            'url': self.url
        }


class GCSField(models.Field):
    """GCS """

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    def get_internal_type(self):
        return 'TextField'

    def from_db_value(self, value, expression, connection):
        if not value:
            return None
        try:
            gcs_data = json.loads(value)
            gcp_blob = GCSBlob(**gcs_data)
            return gcp_blob
        except ValueError:
            return None

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            return value
        data = {
            'bucket': value.bucket,
            'filename': value.filename,
            'path': value.path,
        }
        return json.dumps(data)

    def to_python(self, value):
        if isinstance(value, GCSBlob):
            return value

        if value is None:
            return value

        if isinstance(value, str) and value.startswith('gs://'):  # this is for a case when field is displayed in Admin
            gcs_blob = GCSBlob.create_from_uri(value)
            return gcs_blob
        try:
            gcs_data = json.loads(value)
            gcp_blob = GCSBlob(**gcs_data)
            return gcp_blob
        except ValueError as e:
            raise e

    # def formfield(self, **kwargs):
    #     # TODO see form for DateTime field
    #     defaults = {'form_class': GCSMultiForm}
    #     defaults.update(kwargs)
    #     return super().formfield(**defaults)


class Horse(CommonData):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=15, choices=HORSE_TYPES)
    sex = models.CharField(max_length=10, choices=SEX)
    date_of_birth = models.DateField()
    starts = models.IntegerField(null=True, blank=True, default=0)

    date_last_start = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=15, choices=COUNTRIES, null=True, blank=True)
    tf_reg = models.CharField('TFReg', max_length=15, null=True, blank=True)
    race_rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)
    active = models.CharField(max_length=5, choices=ACTIVE, default='No')
    elite = models.CharField(max_length=5, choices=ELITE, default='No')
    status = models.CharField(max_length=10, choices=HORSE_STATUS, default='Unnamed')
    optimal_distance = models.CharField(max_length=10, choices=OPTIMAL_DISTANCE, null=True, blank=True)
    distance1 = models.CharField(max_length=5, choices=DISTANCE, null=True, blank=True)
    distance2 = models.CharField(max_length=5, choices=DISTANCE, null=True, blank=True)
    size1 = models.CharField(max_length=5, choices=SIZE1, null=True, blank=True)
    class1 = models.CharField(max_length=5, choices=CLASS1, null=True, blank=True)
    class2 = models.CharField(max_length=5, choices=CLASS2, null=True, blank=True)
    class3 = models.CharField(max_length=5, choices=CLASS3, null=True, blank=True)
    pred_opt_dist = models.CharField(max_length=10, choices=OPTIMAL_DISTANCE, null=True, blank=True)

    sire = models.CharField(max_length=50, null=True, blank=True)
    dam = models.CharField(max_length=50, null=True, blank=True)
    broodmare_sire = models.CharField('Broodmare Sire', max_length=50, null=True, blank=True)
    country_code = models.CharField('Country Code', max_length=10, null=True, blank=True)
    starts_country = models.ForeignKey('CountryWeight', on_delete=models.SET_NULL, related_name='horses',
                                       null=True, blank=True)
    avg_distance_raced = models.IntegerField('Average Distance Raced', null=True, blank=True)
    hurdle = models.CharField(max_length=4, null=True, blank=True)
    cpi_rating = models.FloatField('CPI Rating', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    @property
    def update_days(self):
        if self.updated_at:
            date_diff = timezone.now() - self.updated_at
            return date_diff.days
        else:
            return 0

    @property
    def start_days(self):
        if self.date_last_start:
            date_diff = datetime.date.today() - self.date_last_start
            return date_diff.days
        else:
            return 0

    @property
    def days_old(self):
        if self.date_of_birth:
            date_diff = datetime.date.today() - self.date_of_birth
            return date_diff.days
        else:
            return 0

    def score_optimal_distance(self):
        if self.pred_opt_dist:
            return
        fields = ('sex', 'distance1', 'distance2', 'size1', 'class1', 'class2', 'class3',)
        empty_fields = []
        input_data = dict()

        for field in fields:
            field_val = getattr(self, field, None)
            if field_val is None or field_val == '':
                empty_fields.append(field)
                continue
            input_data[field] = field_val

        if empty_fields:
            return

        OPTIMAL_DISTANCE_PREDICTION_SERVICE = 'https://optimal-distance-prediction-ezvwl7dg6a-uc.a.run.app/predict'
        res = score_tabular_classification_prediction(OPTIMAL_DISTANCE_PREDICTION_SERVICE, input_data)
        if res:
            self.pred_opt_dist = res

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.starts and self.starts >= 3:
            self.active = 'Yes'

        if self.race_rating and self.race_rating >= 3.0:
            self.elite = 'Yes'
        else:
            self.elite = 'No'
        # set country from CountryWeight
        if self.starts_country and self.starts_country.country:
            self.country = self.starts_country.country
        self.score_optimal_distance()
        super().save(force_insert, force_update, using, update_fields)

    # def update_status(self):
    #     """Obsolete, now it's used update_status_new method"""
    #     no_years = 3 * 365
    #     # calculate Active
    #     if self.starts and self.starts >= 3 and self.active == 'No':
    #         self.active = 'Yes'
    #     else:
    #         self.active = 'No'
    #
    #     # calculate Elite
    #     if self.days_old >= no_years and self.type == 'Flat' and self.active == 'Yes' and self.race_rating >= 100:
    #         self.elite = 'Yes'
    #     elif self.days_old >= no_years and self.type == 'National Hunt' and self.active == 'Yes' and self.race_rating >= 140:
    #         self.elite = 'Yes'
    #     elif self.days_old < no_years and self.type == 'Flat' and self.active == 'Yes':
    #         pass
    #     else:
    #         self.elite = 'No'
    #
    #     # calculate Live
    #     if self.starts and self.starts > 0:
    #         self.status = 'Live'
    #
    #     # calculate Retired
    #     if self.days_old >= 2200:
    #         self.status = 'Retired'
    #
    #     self.save()

    def update_status_new(self):
        """based on https://tasks.hubstaff.com/app/organizations/24036/projects/210554/tasks/4129161

        """
        if not self.tf_reg:
            return
        name = self.name.lower()
        if name != 'un-named' and self.starts == 0:
            self.status = 'Unraced'
        if name != 'un-named' and self.days_old > 2200:
            self.status = 'Retired'
        if name == 'un-named':
            self.status = 'Unnamed'
            self.name = f'Unnamed ex {self.dam}'
        else:
            self.status = 'Live'

        if self.starts and self.starts > 3:
            self.active = 'Yes'
        if self.days_old > 2200:
            self.status = 'Retired'
        if self.starts and self.start_days > 650:
            self.status = 'Retired'
        if self.starts and self.starts >= 3 and self.avg_distance_raced:
            if self.avg_distance_raced <= 1400:
                self.optimal_distance = '5-7f'
            elif 1400 < self.avg_distance_raced <= 1600:
                self.optimal_distance = '6-8f'
            elif 1600 < self.avg_distance_raced <= 2000:
                self.optimal_distance = '8-10f'
            elif self.avg_distance_raced > 2000:
                self.optimal_distance = '10f+'
        if self.hurdle == 'Y':
            self.type = 'National Hunt'
        elif self.hurdle == 'N':
            self.type = 'Flat'
        self.save()


class Measure(GCSObject, CommonData):
    score_prob_fields = (
        ('cardio_video_score', 'cardio_video_probability'),
        ('biomechanics_video_score', 'biomechanics_video_probability'),
        ('biomechanics_gaf_score', 'biomechanics_gaf_probability'),
        ('biomechanics_keypoint_score', 'biomechanics_keypoint_probability'),
        ('prob_bio_model_score', 'prob_bio_model'),
        ('prob_cardio_bio_model_score', 'prob_cardio_bio_model'),
        ('prob_dna_cardio_bio_model_score', 'prob_dna_cardio_bio_model'),
        ('dlc_jrg_score', 'dlc_jrg_probability')
    )
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='measures')
    date_of_measure = models.DateField()
    days_old = models.IntegerField()
    measure_type = models.CharField(max_length=100, null=True, blank=True)
    video_qc = models.CharField(max_length=20, choices=VIDEO_QC, null=True, blank=True)
    biomechanics_video_probability = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)
    biomechanics_video_score = models.CharField(max_length=10, null=True, blank=True)
    biomechanics_operation_id = models.CharField(max_length=255, null=True, blank=True)
    biomechanics_gaf_probability = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)
    biomechanics_gaf_score = models.CharField(max_length=10, null=True, blank=True)
    biomechanics_keypoint_probability = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)
    biomechanics_keypoint_score = models.CharField(max_length=10, null=True, blank=True)
    biomechanics_cluster = models.IntegerField(null=True, blank=True)

    dlc_video = GCSField('DLC Video', null=True, blank=True, unique=True)
    dlc_h5_file = GCSField('DLC H5 File', null=True, blank=True, unique=True)
    dlc_gaf_image = GCSField('DLC GAF Image', null=True, blank=True, unique=True)
    dlc_jrg_image = GCSField('DLC JRG Image', null=True, blank=True, unique=True)
    cardio_video = GCSField('Cardio Video', null=True, blank=True, unique=True)
    cardio_video_probability = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)
    cardio_video_score = models.CharField(max_length=10, null=True, blank=True)
    cardio_quality_label = models.CharField(max_length=100, null=True, blank=True)
    cardio_quality = models.CharField(max_length=20, choices=VIDEO_QC, null=True, blank=True)
    cardio_type_label = models.CharField(max_length=100, null=True, blank=True)
    cardio_type = models.CharField(max_length=50, choices=CARDIO_TYPE, null=True, blank=True)
    cardio_cluster = models.IntegerField(null=True, blank=True)
    dlc_jrg_score = models.CharField(max_length=10, null=True, blank=True)
    dlc_jrg_probability = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)

    prob_bio_model = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)
    prob_bio_model_score = models.CharField(max_length=10, null=True, blank=True)

    prob_cardio_bio_model = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)
    prob_cardio_bio_model_score = models.CharField(max_length=10, null=True, blank=True)

    prob_dna_cardio_bio_model = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)
    prob_dna_cardio_bio_model_score = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['gcs_gs_uri', ]),
        ]
        ordering = ['id']

    @property
    def measure_age(self) -> str:
        if self.days_old:
            if 365 >= self.days_old >= 0:
                return 'Weanling'
            elif 680 >= self.days_old >= 366:
                return 'Yearling'
            elif 1095 >= self.days_old >= 681:
                return '2YO'
            elif 1460 >= self.days_old >= 1096:
                return '3YO'
            elif self.days_old >= 1461:
                return 'Older'
        return ''

    @property
    def video_url(self):
        return self.gcs_url

    @property
    def dlc_video_url(self):
        if self.dlc_video:
            url = self.dlc_video.url
            return url
        else:
            return ''

    @property
    def dlc_video_gs_uri(self):
        if self.dlc_video:
            return self.dlc_video.uri
        else:
            return ''

    @property
    def dlc_h5_file_url(self):
        if self.dlc_h5_file:
            return self.dlc_h5_file.url
        else:
            return ''

    @property
    def dlc_h5_file_uri(self):
        if self.dlc_h5_file:
            return self.dlc_h5_file.uri
        else:
            return ''

    @property
    def dlc_gaf_image_url(self):
        if self.dlc_gaf_image:
            return self.dlc_gaf_image.url
        else:
            return ''

    @property
    def dlc_gaf_image_uri(self):
        if self.dlc_gaf_image:
            return self.dlc_gaf_image.uri
        else:
            return ''

    @property
    def dlc_jrg_image_uri(self):
        if self.dlc_jrg_image:
            return self.dlc_jrg_image.uri
        else:
            return ''

    @property
    def dlc_jrg_image_url(self):
        if self.dlc_jrg_image:
            return self.dlc_jrg_image.url
        else:
            return ''

    @property
    def cardio_video_url(self):
        if self.cardio_video:
            return self.cardio_video.url
        else:
            return ''

    @property
    def cardio_video_uri(self):
        if self.cardio_video:
            return self.cardio_video.uri
        else:
            return ''

    def __str__(self):
        return f'{self.horse.name} {self.date_of_measure}'

    def get_gcs_gs_uri(self):
        # TODO if gcs_bucket (and gcs_path) is not set, return empty. write migration file to fix for existing
        return f'gs://{self.gcs_bucket}/{self.gcs_path}'

    # def get_score(self, prediction_output: [float, Decimal, int]) -> [None, str]:
    #     if prediction_output is None:
    #         return None
    #     prediction_output = Decimal(prediction_output)
    #     video_score = None
    #     if Decimal('0.0') <= prediction_output < Decimal('0.25'):
    #         video_score = "D"
    #     elif Decimal('0.25') <= prediction_output < Decimal('0.5'):
    #         video_score = "C"
    #     elif Decimal('0.5') <= prediction_output < Decimal('0.7'):
    #         video_score = "B"
    #     elif Decimal('0.7') <= prediction_output < Decimal('0.8'):
    #         video_score = "B+"
    #     elif Decimal('0.8') <= prediction_output < Decimal('0.9'):
    #         video_score = "A"
    #     elif Decimal('0.9') <= prediction_output <= Decimal('1.0'):
    #         video_score = "A+"
    #     return video_score

    def get_cardio_type(self, cardio_cluster) -> str:
        cardio_type = None
        if cardio_cluster:
            if cardio_cluster == -1:
                cardio_type = 'Failed'
            elif cardio_cluster == 0:
                cardio_type = 'Bullseye Late Maturing Turf'
            elif cardio_cluster == 1:
                cardio_type = 'Bullseye On-Pace Dirt Miler'
            elif cardio_cluster == 2:
                cardio_type = 'Bullseye Dirt Classic/Miler'
            elif cardio_cluster == 3:
                cardio_type = 'Turf/Off Speed Dirt Miler'
            elif cardio_cluster == 4:
                cardio_type = 'Bullseye Dirt Sprinter'
            elif cardio_cluster == 5:
                cardio_type = 'Late Maturing Turf Sprinter/Miler'
            elif cardio_cluster == 6:
                cardio_type = 'Australian Bullseye Turf Sprinter'
            elif cardio_cluster == 7:
                cardio_type = 'Bullseye Dirt Miler'
            elif cardio_cluster == 8:
                cardio_type = 'Euro Bullseye Turf Sprinter'
            elif cardio_cluster == 9:
                cardio_type = 'On-pace Turf Sprinter/Miler'
        return cardio_type


    def score_dna_cardio_biomechanics(self):
        """Score cardio-biomechanics and/or dna-cardio-biomechanics in case these values are not set.
        It validates if all necessary fields are set and in such case it calls external API to get probability
        Method just sets values to the fields, it doesn't save
        """

        if self.prob_dna_cardio_bio_model and self.prob_cardio_bio_model:  # measure was scored so exit
            return

        cardio_biomechanics_fields = [
            'cardio_type', 'cardio_cluster', 'cardio_video_probability', 'biomechanics_cluster',
            'biomechanics_gaf_probability', 'biomechanics_keypoint_probability',
            'biomechanics_video_probability', 'dlc_jrg_probability', 'measure_type']

        horse_dna_cardio_biomechanics_fields = ('sex', 'distance1', 'distance2', 'size1', 'class1', 'class2', 'class3',)
        horse_cardio_biomechanics_fields = ('sex',)

        dna_cardio_biomechanics_input_data = dict()
        cardio_biomechanics_input_data = dict()

        empty_cardio_biomechanics_fields = []
        empty_horse_cardio_biomechanics_fields = []
        empty_horse_dna_cardio_biomechanics_fields = []

        # check/get fields for both cardio-biomechanics and dna-cardio-biomechanics prediction
        for field in cardio_biomechanics_fields:
            field_val = getattr(self, field, None)
            if field_val is None or field_val == '':
                empty_cardio_biomechanics_fields.append(field)
                continue
            dna_cardio_biomechanics_input_data[field] = str(
                field_val)  # all numeric values should be represented as strings
            cardio_biomechanics_input_data[field] = str(field_val)

        # check/get horse fields for cardio_biomechanics
        for field in horse_cardio_biomechanics_fields:
            field_val = getattr(self.horse, field, None)
            if field_val is None or field_val == '':
                empty_horse_cardio_biomechanics_fields.append(field)
                continue
            cardio_biomechanics_input_data[field] = str(field_val)

        # check/get horse fields for dna-cardio_biomechanics
        for field in horse_dna_cardio_biomechanics_fields:
            field_val = getattr(self.horse, field, None)
            if field_val is None or field_val == '':
                empty_horse_dna_cardio_biomechanics_fields.append(field)
                continue
            dna_cardio_biomechanics_input_data[field] = str(field_val)

        if empty_cardio_biomechanics_fields and empty_horse_dna_cardio_biomechanics_fields and \
                empty_horse_cardio_biomechanics_fields:
            return

        CARDIO_BIOMECHANICS_SERVICE_URL = 'https://cardio-biomechanics-prediction-ezvwl7dg6a-uc.a.run.app/predict'
        DNA_CARDIO_BIOMECHANICS_SERVICE_URL = 'https://dna-cardio-biomechanics-prediction-ezvwl7dg6a-uc.a.run.app/predict'

        cardio_biomechanics_prob = None
        dna_cardio_biomechanics_prob = None
        if not self.prob_cardio_bio_model and not (
                empty_cardio_biomechanics_fields or empty_horse_cardio_biomechanics_fields):  # score cardio-biomechanics model if it's not yet scored
            logging.info(f'scoring cardio-biomechanics for {self.id}')
            cardio_biomechanics_prob = score_tabular_prediction(CARDIO_BIOMECHANICS_SERVICE_URL,
                                                                cardio_biomechanics_input_data)
            if cardio_biomechanics_prob:
                self.prob_cardio_bio_model = cardio_biomechanics_prob

        if not self.prob_dna_cardio_bio_model and not (
                empty_cardio_biomechanics_fields or empty_horse_dna_cardio_biomechanics_fields
        ):  # score dna-cardio-biomechanics model if it's not yet scored
            logging.info(f'scoring cardio-biomechanics for {self.id}')
            dna_cardio_biomechanics_prob = score_tabular_prediction(DNA_CARDIO_BIOMECHANICS_SERVICE_URL,
                                                                    dna_cardio_biomechanics_input_data)
            if dna_cardio_biomechanics_prob:
                self.prob_dna_cardio_bio_model = dna_cardio_biomechanics_prob

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.date_of_measure and self.horse.date_of_birth:
            days_old = self.date_of_measure - self.horse.date_of_birth
            self.days_old = days_old.days

        gcs_gs_uri = self.get_gcs_gs_uri()
        self.gcs_gs_uri = gcs_gs_uri
        set_scores(self)
        self.measure_type = f'{self.horse.type} {self.measure_age}'
        self.cardio_type = self.get_cardio_type(self.cardio_cluster)
        self.score_dna_cardio_biomechanics()
        super().save(force_insert, force_update, using, update_fields)


class ImageMeasurement(CommonData):
    score_prob_fields = (
        ('prob_conform_model_score', 'prob_conform_model'),
    )

    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='image_measurements')
    date_of_measure = models.DateField()
    image = GCSField('Image', null=True, blank=True)
    morph_data = models.JSONField(null=True, blank=True)
    calculated_data = models.JSONField(null=True, blank=True)

    prob_image = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)
    prob_conform_model = models.DecimalField(max_digits=11, decimal_places=10, null=True, blank=True)
    prob_conform_model_score = models.CharField(max_length=10, null=True, blank=True)

    back_length = models.FloatField(null=True, blank=True)
    body_length = models.FloatField(null=True, blank=True)
    cannon = models.FloatField(null=True, blank=True)
    femur = models.FloatField(null=True, blank=True)
    femur_angle = models.FloatField(null=True, blank=True)
    fetlock = models.FloatField(null=True, blank=True)
    fetlock_angle = models.FloatField(null=True, blank=True)
    forearm_angle = models.FloatField(null=True, blank=True)
    forelimb = models.FloatField(null=True, blank=True)
    front_pastern = models.FloatField(null=True, blank=True)
    hind_fetlock_angle = models.FloatField(null=True, blank=True)
    hind_cannon = models.FloatField(null=True, blank=True)
    hip_angle = models.FloatField(null=True, blank=True)
    hock_angle = models.FloatField(null=True, blank=True)
    humerus = models.FloatField(null=True, blank=True)
    imbalance = models.FloatField(null=True, blank=True)
    ischium_hock = models.FloatField(null=True, blank=True)
    neck = models.FloatField(null=True, blank=True)
    pelvis = models.FloatField(null=True, blank=True)
    pelvis_horizontal = models.FloatField(null=True, blank=True)
    pelvis_femur = models.FloatField(null=True, blank=True)
    proportion = models.FloatField(null=True, blank=True)
    scope = models.FloatField(null=True, blank=True)
    shoulder = models.FloatField(null=True, blank=True)
    shoulder_angle = models.FloatField(null=True, blank=True)
    shoulder_horizontal = models.FloatField(null=True, blank=True)
    thrust = models.FloatField(null=True, blank=True)
    tibia = models.FloatField(null=True, blank=True)
    triangle = models.CharField(max_length=50, null=True, blank=True)
    procrustes_distance = models.FloatField(null=True, blank=True)
    leg_length = models.FloatField(null=True, blank=True)
    forelimb_length = models.FloatField(null=True, blank=True)
    hind_length_distance = models.FloatField(null=True, blank=True)
    neck_length_ratio = models.FloatField(null=True, blank=True)
    forelimb_hind_ratio = models.FloatField(null=True, blank=True)
    leg_back_ratio = models.FloatField(null=True, blank=True)
    body_hind_ratio = models.FloatField(null=True, blank=True)

    @property
    def image_url(self):
        if self.image:
            url = self.image.url
            return url
        else:
            return ''

    @property
    def image_uri(self):
        if self.image:
            url = self.image.uri
            return url
        else:
            return ''

    def __str__(self):
        return f'horse {self.horse_id} - {self.id}'

    @retriable()
    def get_landmarks_prediction(self, image_content):
        data = base64.b64encode(image_content).decode()
        url = 'https://morph-landmarks-prediction-ezvwl7dg6a-uc.a.run.app/predict'
        r = requests.post(url, json={'image_data': data})
        if r.status_code == 200:
            response_data = json.loads(r.text)
            return response_data['result']
        else:
            error_msg = f'error while making morph-landmarks prediction {r.status_code} {r.text}'
            logging.error(error_msg)
            raise Exception(error_msg)

    def calculate_landmarks(self):
        image = self.image
        if image:
            if isinstance(self.image, str):  # when first object is saved, image is passed as string
                image = GCSBlob(**json.loads(self.image))
            image_content = image.download_as_bytes()
            morp_res = self.get_landmarks_prediction(image_content)
            self.morph_data = morp_res

    def get_conformation_field_values(self) -> dict:
        if not self.calculated_data:
            return dict()
        else:
            angels = self.calculated_data.get('angels')
            bones = self.calculated_data.get('bones')
            factors = self.calculated_data.get('factors')
            procrustes_distance = self.calculated_data.get('procrustesDistance')

            data = dict()

            for _, angel_data in enumerate(angels):
                angle_name = angel_data['angleName']
                angle = angel_data['angle']
                data[angle_name] = angle

            for _, bone_data in enumerate(bones):
                bone_name = bone_data['boneName']
                bone_distance = bone_data['distance']
                data[bone_name] = bone_distance
            for _, factor_data in enumerate(factors):
                factor_name = factor_data['factorName']
                factor_value = factor_data['value']
                data[factor_name] = factor_value

            out = dict()
            out['back_length'] = data['Backlength']
            out['body_length'] = data['Bodylength']
            out['cannon'] = data['Cannon']
            out['femur'] = data['Femur']
            out['femur_angle'] = data['Femur Angle']
            out['fetlock'] = data['Fetlock']
            out['fetlock_angle'] = data['Fetlock Angle']
            out['forearm_angle'] = data['Forearm Angle']
            out['forelimb'] = data['Forelimb']
            out['front_pastern'] = data['Front Pastern']
            out['hind_fetlock_angle'] = data['Hind Fetlock Angle']
            out['hind_cannon'] = data['HindCannon']
            out['hip_angle'] = data['Hip Angle']
            out['hock_angle'] = data['Hock Angle']
            out['humerus'] = data['Humerus']
            out['imbalance'] = data['Imblance']
            out['ischium_hock'] = data['Ischium-Hock']
            out['neck'] = data['Neck']
            out['pelvis'] = data['Pelvis']
            out['pelvis_horizontal'] = data['Pelvis Horizontal']
            out['pelvis_femur'] = data['Pelvis-Femur']
            out['proportion'] = data['Proportion']
            out['scope'] = data['Scope']
            out['shoulder'] = data['Shoulder']
            out['shoulder_angle'] = data['Shoulder Angle']
            out['shoulder_horizontal'] = data['Shoulder Horizontal']
            out['thrust'] = data['Thrust']
            out['tibia'] = data['Tibia']
            out['triangle'] = data['Triangle']
            out['procrustes_distance'] = procrustes_distance
            out['leg_length'] = data['Leg Length']
            out['forelimb_length'] = data['Forelimb Length']
            out['hind_length_distance'] = data['Hindlimb Length']
            out['neck_length_ratio'] = data['Neck/Leg Ratio']
            out['forelimb_hind_ratio'] = data['Forelimb/Hindlimb Ratio']
            out['leg_back_ratio'] = data['Leg/Backlength Ratio']
            out['body_hind_ratio'] = data['Bodylength/Hindlimb Ratio']
            return out

    def set_conformation_field_values(self):
        if not self.calculated_data:
            return

        field_values = self.get_conformation_field_values()
        for k, v in field_values.items():
            setattr(self, k, v)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.morph_data and self.image:
            self.calculate_landmarks()

        set_scores(self)
        self.set_conformation_field_values()
        super().save(force_insert, force_update, using, update_fields)
        if self.image and self.prob_image is None and config.run_online_morph_prediction:
            url = reverse('morph-image-online-prediction')
            if isinstance(self.image, str):
                image_json = json.loads(self.image)
                image = GCSBlob(image_json['bucket'], image_json['filename'], image_json['path'])
                image_uri = image.uri
            else:
                image_uri = self.image.uri
            data = {'gcs_uri': image_uri, 'image_measurement_id': self.pk}
            full_url = f'{settings.HOSTNAME}{url}'
            create_task(full_url, 'online-prediction', data)
        if self.procrustes_distance and self.prob_image is not None and not self.prob_conform_model and \
                config.run_online_morph_prediction:
            url = reverse('morph-image-conformation-prediction')
            full_url = f'{settings.HOSTNAME}{url}'
            data = {'image_measurement_id': self.pk}
            create_task(full_url, 'online-prediction', data)


class CountryWeight(CommonData):
    starts_country = models.CharField('Starts Country', max_length=18, primary_key=True)
    country = models.CharField(max_length=18, null=True, blank=True, choices=COUNTRIES)
    country_fullname = models.CharField(max_length=200, null=True, blank=True)
    country_weight = models.FloatField(null=True, blank=True, default=1.0)

    def __str__(self):
        return f'{self.starts_country} - {self.country_fullname} - {self.country} - {self.country_weight}'


class MLModel(CommonData):
    dataset_type = models.CharField(max_length=30)
    dataset_name = models.CharField(max_length=255)
    dataset_id = models.CharField(max_length=255)
    dataset_number_horses = models.IntegerField()
    dataset_number_positive = models.IntegerField()
    dataset_number_negative = models.IntegerField()
    dataset_creation_date = models.DateTimeField()

    model_type = models.CharField(max_length=30)
    model_name = models.CharField(max_length=255)
    model_id = models.CharField(max_length=255)
    model_creation_date = models.DateTimeField()
    number_training = models.IntegerField()
    number_test = models.IntegerField()
    data_split = models.CharField(max_length=50)
    average_precision = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    auc_pr = models.FloatField(null=True, blank=True)
    auc_roc = models.FloatField(null=True, blank=True)
    log_loss = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    algorithm = models.CharField(max_length=255, null=True, blank=True)
    optimized_for = models.CharField(max_length=255, null=True, blank=True)
    objective = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'model: {self.model_name} / dataset: {self.dataset_name} / date: {self.model_creation_date}'


class MLModelMetadata(CommonData):
    model_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    resource_name = models.CharField(max_length=500)
    creation_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    confusion_matrix = models.JSONField(null=True, blank=True)
    annotations = models.JSONField(null=True, blank=True)
    feature_attributions = models.JSONField(null=True, blank=True)
    log_loss = models.FloatField(null=True, blank=True)
    au_prc = models.FloatField(null=True, blank=True)
    au_roc = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ('-creation_time',)

    def __str__(self):
        return f'model: {self.name} {self.model_id} {self.creation_time}'


class ScoreBins(CommonData):
    """
    bins should have a structure of dictionary with keys as scores and values as lists with boundaries for example
    {
        'A': [0.2505566478, 0.4478050768],
        'A+': [0.4478050768, 1.0],
        'B': [0.1255440116, 0.1556581855],
        'B+': [0.1556581855, 0.2505566478],
        'C': [0.094587855, 0.1255440116],
        'D': [0.0, 0.094587855]
    }
    """

    prob_field_name = models.CharField(max_length=100)
    bins = models.JSONField()

    @classmethod
    def create_bins(cls, model: Type[models.Model], probability_field_name: str) -> ScoreBins:
        """Create bins for probability field"""
        try:
            score_bin = cls.objects.get(prob_field_name=probability_field_name)
        except cls.DoesNotExist:
            score_bin = ScoreBins(prob_field_name=probability_field_name)
        objects = model.objects.all()
        objects_dict = [m.__dict__ for m in objects]
        df_objects = pd.DataFrame(objects_dict)
        df_objects.drop(columns=['_state'], inplace=True)
        df_objectsx = df_objects[~df_objects[probability_field_name].isna()]
        df_objectsx = df_objectsx[probability_field_name].apply(lambda x: float(str(x)))
        res = pd.qcut(df_objectsx.unique(), q=6, retbins=True)
        bins_values = res[1]
        bins_data = {
            'D': [0.0, bins_values[1]],
            'C': [bins_values[1], bins_values[2]],
            'B': [bins_values[2], bins_values[3]],
            'B+': [bins_values[3], bins_values[4]],
            'A': [bins_values[4], bins_values[5]],
            'A+': [bins_values[5], 1.0],
        }
        logging.info(f'bins info for {probability_field_name} {res[0].value_counts()}')
        logging.info(f'bins values for {probability_field_name} {bins_data}')
        score_bin.bins = bins_data
        score_bin.save()
        return score_bin

    def get_score(self, probability: Union[float, Decimal]):
        """Get score based on bin values"""
        probability = Decimal(probability)
        for score, boundaries in self.bins.items():
            bin_min = Decimal(boundaries[0])
            bin_max = Decimal(boundaries[1])
            if bin_max >= probability > bin_min:
                return score

    def __str__(self):
        return self.prob_field_name


class UserAction(CommonData):
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE)
    horse_name = models.CharField(max_length=50, null=True, blank=True)
    action = models.CharField(max_length=50, choices=USER_ACTION_CHOICES)
    metadata = models.JSONField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.horse:
            self.horse_name = self.horse.name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.user.email} - {self.horse_name} - {self.action} - {self.created_at.date()}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

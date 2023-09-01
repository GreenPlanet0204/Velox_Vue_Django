import os
import json
import logging
import datetime
from enum import Enum

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.cloud import firestore
from .models import Horse, MLModelMetadata, ScoreBins, Measure, ImageMeasurement
from .vertex_online_prediction import online_morph_image_prediction
from .common import score_tabular_prediction

db = firestore.Client(project=settings.GCP_PROJECT)


@csrf_exempt
def update_stats(request):
    """Goes through all horses and updates/calculates stats"""
    logging.info('starting with updating stats')
    horses = Horse.objects.all()
    for horse in horses:
        horse.update_status_new()
    logging.info('updating stats completed')
    return HttpResponse('ok')


@csrf_exempt
def set_live(request):
    """Sets live status for horses with tf_reg"""
    logging.info('starting with updating stats')
    horses = Horse.objects.all()
    for horse in horses:
        horse.status = 'Unnamed'
        horse.save()
    logging.info('updating status completed')
    return HttpResponse('ok')


@csrf_exempt
def calculate_batch_elite(request):
    """For all horses, calculate race_rating and elite"""

    horses = Horse.objects.all()
    for horse in horses:
        starts_country = horse.starts_country
        if starts_country and horse.cpi_rating is not None:
            country_weight = starts_country.country_weight
            race_rating = country_weight * horse.cpi_rating
            horse.race_rating = race_rating
            horse.save()
    return HttpResponse('ok')


@csrf_exempt
def reset_stats(request):
    """"Resets stats for all horse"""
    horses = Horse.objects.all()
    for horse in horses:
        horse.starts = 0
        horse.race_rating = None
        horse.active = 'No'
        horse.elite = 'No'
        horse.status = 'Unnamed'
        horse.cpi_rating = None
        horse.save()
    return HttpResponse('ok')


@csrf_exempt
def sync_ml_models(request):
    """Load Model from Vertex AI"""
    from .vertex_ai import get_all_ml_models_metadata

    no_models = 10  # default number to get
    if request.GET:
        no_models = request.GET.get('number_of_models', no_models)
        no_models = int(no_models)
    ml_models = get_all_ml_models_metadata(no_models)
    for ml_model_data in ml_models:
        resource_name = ml_model_data['resource_name']
        try:
            MLModelMetadata.objects.get(resource_name=resource_name)
        except MLModelMetadata.DoesNotExist:
            logging.info(f'creating MLModelMetadata object {ml_model_data}')
            MLModelMetadata.objects.create(**ml_model_data)
    return HttpResponse('ok')


@csrf_exempt
def calculate_score_bins(request):
    """Recalculates Score Bins"""

    for _, prob_field in Measure.score_prob_fields:
        ScoreBins.create_bins(Measure, prob_field)

    for _, prob_field in ImageMeasurement.score_prob_fields:
        ScoreBins.create_bins(ImageMeasurement, prob_field)

    return HttpResponse('ok')


@csrf_exempt
def save_measures(request):
    measures = Measure.objects.all()
    for measure in measures:
        measure.save()
    return HttpResponse('ok')


@csrf_exempt
def sync_ml_models_firestore(request):
    from .vertex_ai import sync_ml_models_firestore
    sync_ml_models_firestore()
    return HttpResponse('ok')


class OnlinePredictionStatus(Enum):
    RUNNING = 'running'
    COMPLETED = 'completed'


@csrf_exempt
def morph_image_online_prediction(request):
    """Cloud Task that handles async online prediction for morph image"""
    env = os.environ['ENV']
    jobs_collection_name = f'online_prediction_jobs_{env}'

    if request.method == 'POST':
        request_body = request.body
        try:
            data = json.loads(request_body)
        except ValueError:
            logging.error(f"Couldn't decode request body to json: {request_body}")
            return HttpResponse('')
        gcs_uri = data.get('gcs_uri', None)
        if not gcs_uri:
            msg = f'missing parameter gcs_uri'
            logging.error(msg)
            return HttpResponse(msg)

        image_measurement_id = data.get('image_measurement_id', None)
        if not image_measurement_id:
            msg = f'missing parameter image_measurement_id'
            logging.error(msg)
            return HttpResponse(msg)

        doc = db.collection(jobs_collection_name).document(str(image_measurement_id)).get()
        if doc.exists:
            doc_data = doc.to_dict()
            status = doc_data.get('status', '')
            if status == OnlinePredictionStatus.RUNNING.value:
                logging.info(f'there is ongoing online prediction for image_measurement_id {image_measurement_id}, '
                             f'image uri: {gcs_uri}')
                return HttpResponse('')

        doc_data = {
            'status': OnlinePredictionStatus.RUNNING.value,
            'start_ts': datetime.datetime.utcnow()
        }

        db.collection(jobs_collection_name).document(str(image_measurement_id)).set(doc_data)

        model_name = 'morph-images'
        online_morph_image_prediction(model_name, gcs_uri, image_measurement_id)

        doc_data = {
            'status': OnlinePredictionStatus.COMPLETED.value,
            'end_ts': datetime.datetime.utcnow()
        }
        db.collection(jobs_collection_name).document(str(image_measurement_id)).set(doc_data, merge=True)

    return HttpResponse('ok')


@csrf_exempt
def set_tf_reg(request):
    horses = Horse.objects.all()
    for horse in horses:
        if horse.tf_reg == "":
            horse.tf_reg = None
            horse.save()
    return HttpResponse('ok')


@csrf_exempt
def save_image_measures(request):
    ims = ImageMeasurement.objects.all()
    for im in ims:
        im.save()
    return HttpResponse('ok')


@csrf_exempt
def morph_image_conformation_prediction(request):
    """Cloud Task that handles async online prediction for conformation online prediction"""

    if request.method == 'POST':
        request_body = request.body
        try:
            data = json.loads(request_body)
        except ValueError:
            logging.error(f"Couldn't decode request body to json: {request_body}")
            return HttpResponse('')
        im_id = data.get('image_measurement_id', '')
        if not im_id:
            msg = f'missing image measurement id'
            logging.error(msg)
            return HttpResponse(msg)

        try:
            im = ImageMeasurement.objects.get(pk=im_id)
        except Exception as e:
            msg = f"couldn't find Image Measurement with id: {im_id}"
            logging.error(msg)
            return HttpResponse(msg)

        logging.info(f"doing morph image conformation tabular prediction for {im_id}")

        prediction_data = im.get_conformation_field_values()
        prediction_data['prob_image'] = str(im.prob_image)

        prediction_service_url = 'https://morph-images-conformation-tabular-prediction-ezvwl7dg6a-uc.a.run.app/predict'
        prob_conformation = score_tabular_prediction(prediction_service_url, prediction_data)
        im.prob_conform_model = prob_conformation
        im.save()
        logging.info(f"completed morph image conformation tabular prediction for {im_id}")

    return HttpResponse('ok')

@csrf_exempt
def delete_horses(request):
    import csv
    from io import StringIO
    from .common import send_email

    horses = Horse.objects.filter(measures=None, image_measurements=None)
    horse_delete = []
    for h in horses:
        distance1 = h.distance1
        if h.days_old >= 1000 and not distance1:
            horse_delete.append(h)

    f = StringIO()
    fields = (
    'id', 'name', 'type', 'sex', 'date_of_birth', 'starts', 'date_last_start', 'country', 'tf_reg', 'race_rating',
    'active', 'elite', 'distance1', 'distance2', 'size1', 'class1', 'class2', 'class3')
    csv_writer = csv.DictWriter(f, fieldnames=fields)
    csv_writer.writeheader()
    for h in horse_delete:
        out = {}
        for field in fields:
            out[field] = getattr(h, field)
        csv_writer.writerow(out)

    csv_content = f.getvalue()
    f.close()

    subject = 'List of horses without measurements to be deleted'
    body = f'Deleting {len(horse_delete)} horses'
    logging.info(body)
    send_email(body, subject, csv_content)
    to_delete = Horse.objects.filter(pk__in=[h.id for h in horse_delete])
    to_delete.delete()
    return HttpResponse('ok')

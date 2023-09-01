import datetime
import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.db import connection

import pandas as pd
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound

import django_filters.rest_framework

from google.cloud import storage

from .serializers import SignedUrlSerializer, HorseSerializer, MeasureSerializer, MeasureCreateSerializer
from .serializers import MeasureMLUpdateSerializer, MeasureMLGCSUpdateSerializer
from .serializers import TabularMLUpdate
from .serializers import UserSerializer, UserLoginSerializer, UserCreateSerializer
from .serializers import ImageMeasurementSerializer, MeasureFileSerializer, CountryWeightSerializer
from .serializers import MLModelMetadataSerializer
from .serializers import MorphImageMLUpdateSerializer
from .serializers import ShortlistSerializer
from .models import Horse, Measure, GCSBlob, User, ImageMeasurement, CountryWeight, MLModelMetadata, UserAction
from .common import gcs

import google.auth
from google.auth.transport import requests


# credentials, _ = google.auth.default()
# credentials = settings.GCP_CREDENTIALS
def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GCSUploadView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False, methods=['post'])
    def get_signed_url(self, request):
        # input_data = SignedUrlSerializer(data=request.query_params)
        input_data = SignedUrlSerializer(data=request.data)
        input_data.is_valid(raise_exception=True)
        filename = input_data.data['filename']
        content_type = input_data.data['content_type']
        video_type = input_data.data.get('video_type', '')
        file_type = input_data.data.get('file_type', '')
        if not file_type:
            file_type = video_type
        date_of_measure = input_data.data['date_of_measure']
        if not date_of_measure:
            date_of_measure = datetime.date.today().strftime('%Y-%m-%d')
        gcs_filename = f'{date_of_measure}_{filename}'
        if file_type == 'cardio':
            gcs_path = f'raw/cardio_files/{gcs_filename}'
        elif file_type == 'image_measurement':
            gcs_path = f'raw/image_measurements/{gcs_filename}'
        elif file_type == 'video':
            gcs_path = f'raw/files/{gcs_filename}'
        else:
            gcs_path = f'raw/{gcs_filename}'
        # service_account_email = "velox-webapp@velox-horse1.iam.gserviceaccount.com"
        # r = requests.Request()
        # credentials.refresh(r)
        bucket = storage.Bucket(gcs, settings.GCS_BUCKET)
        file_blob = bucket.blob(gcs_path, chunk_size=262144 * 5)
        # If you use a service account credential, you can use the embedded email
        # if hasattr(credentials, "service_account_email"):
        #     service_account_email = credentials.service_account_email

        url = file_blob.generate_signed_url(expiration=datetime.timedelta(hours=2), method='PUT',
                                            content_type=content_type,
                                            version="v4",
                                            # service_account_email=service_account_email,
                                            # access_token=credentials.token,
                                            # credentials=credentials
                                            )
        out = {
            'url': url,
            'gcs_path': gcs_path,
            'gcs_bucket': bucket.name,
            'gcs_filename': gcs_filename
        }
        return Response(out)


class HorseAPIView(viewsets.ModelViewSet):
    queryset = Horse.objects.all()
    serializer_class = HorseSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['elite', 'country', 'status', 'active']
    search_fields = ['name', ]
    ordering_fields = '__all__'
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return HorseSerializer
        else:
            return HorseSerializer

    @action(detail=False, serializer_class=TabularMLUpdate, methods=['post'])
    def update_ml_tabular(self, request):
        request_data = request.data
        serializer = TabularMLUpdate(data=request_data)
        serializer.is_valid(raise_exception=True)
        update_fields = serializer.data['update_fields']
        search_fields = serializer.data['search_fields']
        horses = Horse.objects.filter(**search_fields)
        for horse in horses:
            logging.debug(f'updating horse {horse.id} with data {update_fields}')
            for field_name, field_value in update_fields.items():
                setattr(horse, field_name, field_value)
            horse.save()
        if horses:
            updated_horses = [horse.id for horse in horses]
            return Response({'updated_horses': updated_horses})
        else:
            raise NotFound(code=404)

    @action(detail=False, methods=['get'])
    def counts(self, request):
        horses_count = Horse.objects.count()
        active_count = Horse.objects.filter(active='Yes').count()
        elite_count = Horse.objects.filter(elite='Yes').count()

        data = {
            'count': horses_count,
            'active': active_count,
            'elite': elite_count
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def shortlisttab(self, request):

        with connection.cursor() as cursor:
            cursor.execute("""SELECT h.id as horse_id, h.name, h.sire, h.active, h.date_of_birth, m.date_of_measure, m.prob_bio_model, im.prob_conform_model, h.active, h.elite,
            CAST(m.prob_bio_model AS FLOAT) + CAST(im.prob_conform_model AS FLOAT) AS cum_prob
            FROM velox_app_horse AS h
            JOIN velox_app_imagemeasurement AS im ON h.id = im.horse_id
            JOIN velox_app_measure AS m ON h.id = m.horse_id
            WHERE m.prob_bio_model >= '0.5'
            AND im.prob_conform_model >= '0.5'
            AND im.date_of_measure = m.date_of_measure""")
            res = dictfetchall(cursor)
        with connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(*)      
            FROM velox_app_horse AS h
            JOIN velox_app_imagemeasurement AS im ON h.id = im.horse_id
            JOIN velox_app_measure AS m ON h.id = m.horse_id WHERE 
            h.active = 'Yes'
            AND im.date_of_measure = m.date_of_measure
            AND m.prob_bio_model IS NOT NULL 
            AND im.prob_conform_model IS NOT NULL""")
            total_number_active_res = dictfetchall(cursor)
        with connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(*)      
            FROM velox_app_horse AS h
            JOIN velox_app_imagemeasurement AS im ON h.id = im.horse_id
            JOIN velox_app_measure AS m ON h.id = m.horse_id WHERE 
            im.date_of_measure = m.date_of_measure
            AND m.prob_bio_model IS NOT NULL 
            AND im.prob_conform_model IS NOT NULL""")
            total_number_res = dictfetchall(cursor)
        ser = ShortlistSerializer({'items': res,
                                   'total_number_active': total_number_active_res[0]['count'],
                                   'total_number': total_number_res[0]['count']
                                   })
        output_data = ser.data

        return Response(output_data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        def calculate_type(row):
            days_old = row['days_old']
            sex = row['sex']
            horse_age_type = ''
            if 365 >= days_old >= 0:
                horse_age_type = 'Weanling'
            elif 670 >= days_old >= 366:
                horse_age_type = 'Yearling'
            elif 990 >= days_old >= 671:
                horse_age_type = '2YO'
            elif days_old >= 991:
                horse_age_type = 'Older'

            horse_type = f'{sex} {horse_age_type}'
            row['horse_type'] = horse_type
            row['horse_age_type'] = horse_age_type
            return row

        horses = Horse.objects.only('active', 'sex', 'type', 'date_of_birth', 'elite')
        measures = Measure.objects.only('gcs_bucket', 'horse_id', 'cardio_video', 'cardio_video_score',
                                        'cardio_cluster', 'prob_bio_model_score', 'biomechanics_cluster',
                                        'prob_cardio_bio_model_score', 'prob_dna_cardio_bio_model_score',
                                        'date_of_measure', 'days_old')
        # measures_dict = []
        # for m in measures:
        #     m_data = m.__dict__
        #     m_data['days_old'] = m.days_old
        #     measures_dict.append(m_data)
        measures_dict = [m.__dict__ for m in measures]
        horses_dict = [h.__dict__ for h in horses]
        df_horses = pd.DataFrame(horses_dict)
        df_measures = pd.DataFrame(measures_dict)
        df_measures.drop(columns=['_state'], inplace=True)
        df_horses.drop(columns=['_state'], inplace=True)
        merged_df = df_measures.merge(df_horses, how='left', left_on='horse_id', right_on='id', suffixes=('_m', '_h'))

        merged_df = merged_df.apply(calculate_type, axis=1)
        merged_df['biomechanics'] = merged_df['gcs_bucket'].apply(lambda x: False if x is None else True)
        merged_df['cardio'] = merged_df['cardio_video'].apply(lambda x: False if x is None else True)
        merged_df = merged_df[merged_df['active'] == 'Yes']

        # image measurement stats
        image_measurements = ImageMeasurement.objects.only('horse_id', 'prob_conform_model_score')
        image_measurements_dict = [im.__dict__ for im in image_measurements]
        df_image_measurements = pd.DataFrame(image_measurements_dict)
        df_image_measurements.drop(columns=['_state'], inplace=True)
        merged_im_df = df_image_measurements.merge(df_horses, how='left', left_on='horse_id', right_on='id',
                                                   suffixes=('_m', '_h'))
        merged_im_df = merged_im_df[merged_im_df['active'] == 'Yes']

        def get_image_measurements_type_stats(df: pd.DataFrame, prob_field_name: str, field_type: str) -> list[dict]:
            dfx = df[[field_type, 'elite', 'horse_id', prob_field_name]]
            dfx = dfx[~dfx[prob_field_name].isnull()].drop(columns=['horse_id'])
            dfx = dfx.groupby([field_type, prob_field_name, 'elite'], as_index=False).value_counts()
            dfx = pd.DataFrame(dfx)
            df_out = dfx.rename(columns={'count': 'counts'}).reset_index().rename(
                columns={prob_field_name: 'score'}).drop(columns=['index', ])
            return df_out.to_dict(orient='records')

        def get_image_measurements_stats(df: pd.DataFrame, prob_field_name: str) -> list[dict]:
            dfx = df[['elite', 'horse_id', prob_field_name]]
            dfx = dfx[~dfx[prob_field_name].isnull()].drop(columns=['horse_id'])
            dfx = dfx.groupby([prob_field_name, 'elite'], as_index=False).value_counts()
            dfx = pd.DataFrame(dfx)
            df_out = dfx.rename(columns={'count': 'counts'}).reset_index().rename(
                columns={prob_field_name: 'score'}).drop(columns=['index', ])
            return df_out.to_dict(orient='records')

        image_measurements_scores_data = get_image_measurements_stats(merged_im_df, 'prob_conform_model_score')
        image_measurements_horse_types_data = get_image_measurements_type_stats(merged_im_df,
                                                                                'prob_conform_model_score',
                                                                                'type')

        def get_population_stats(df: pd.DataFrame) -> dict:
            counts_s = df[['horse_type']].value_counts()
            stats_df = pd.DataFrame(counts_s).reset_index().rename(columns={0: 'counts'})
            return stats_df.to_dict(orient='records')

        def get_scores_by_age(df: pd.DataFrame, score_field: str):
            dfx = df[['horse_type', score_field, 'elite']].value_counts()
            df_out = dfx.reset_index().rename(columns={0: 'counts', score_field: 'score'})
            return df_out.to_dict(orient='records')

        def get_scores_by_clusters(df: pd.DataFrame, cluster_column: str, score_column: str) -> dict:
            dfx2 = df.groupby([cluster_column, 'elite'])[score_column].value_counts()
            dfx = pd.DataFrame(dfx2)
            df_out = dfx.rename(columns={score_column: 'counts', }).reset_index().rename(
                columns={score_column: 'score', cluster_column: 'cluster'})
            df_out['cluster'] = df_out['cluster'].astype(int)
            return df_out.to_dict(orient='records')

        def get_scores_by_type(df: pd.DataFrame, score_column: str) -> list[dict]:
            dfx2 = df.groupby(['type', 'elite'])[score_column].value_counts()
            dfx = pd.DataFrame(dfx2)
            df_out = dfx.rename(columns={score_column: 'counts', }).reset_index().rename(
                columns={score_column: 'score'})
            return df_out.to_dict(orient='records')

        def get_stats(df: pd.DataFrame, grouped_field, score_field):
            """returns data in nested/drill down format
            :param df:
            :param type_field: horse_age_type for example
            :param score_field: biomechanics_video_score for example
            :return:
            """
            dfx = df.drop_duplicates(subset=['horse_id'])[[grouped_field, score_field, 'elite']]
            dfx = dfx.set_index([grouped_field, score_field]).groupby(level=[0, 1]).value_counts()
            data = {}
            for l1 in dfx.index.levels[0]:
                if not l1:
                    continue
                l2_data = {}
                for l2 in dfx.index.levels[1]:
                    try:
                        d = dfx.xs(l1).xs(l2).to_dict()
                        l2_data[l2] = d
                    except KeyError as e:
                        pass
                data[l1] = l2_data
            return data

        # create dataframes that will be used for stats
        biomechanics_df = merged_df[merged_df['biomechanics'] == True]
        cardio_df = merged_df[merged_df['cardio'] == True]
        biomechanics_elite_df = merged_df[(merged_df['biomechanics'] == True) & (merged_df['elite'] == 'Yes')]
        biomechanics_non_elite_df = merged_df[(merged_df['biomechanics'] == True) & (merged_df['elite'] == 'No')]
        cardio_elite_df = merged_df[(merged_df['cardio'] == True) & (merged_df['elite'] == 'Yes')]
        cardio_non_elite_df = merged_df[(merged_df['cardio'] == True) & (merged_df['elite'] == 'No')]

        # population biomechanics
        population_biomechanics_all = get_population_stats(biomechanics_df)
        population_biomechanics_elite = get_population_stats(biomechanics_elite_df)
        population_biomechanics_non_elite = get_population_stats(biomechanics_non_elite_df)

        # population cardio
        population_cardio_all = get_population_stats(cardio_df)
        population_cardio_elite = get_population_stats(cardio_elite_df)
        population_cardio_non_elite = get_population_stats(cardio_non_elite_df)

        # cardio tab
        cardio_score_age = get_scores_by_age(cardio_df, 'cardio_video_score')
        cardio_score_cluster = get_scores_by_clusters(cardio_df, 'cardio_cluster', 'cardio_video_score')
        cardio_score_type = get_scores_by_type(cardio_df, 'cardio_video_score')

        # biomechanics tab
        biomechanics_score_age = get_scores_by_age(biomechanics_df, 'prob_bio_model_score')
        biomechanics_score_cluster = get_scores_by_clusters(biomechanics_df, 'biomechanics_cluster',
                                                            'prob_bio_model_score')
        biomechanics_score_type = get_scores_by_type(biomechanics_df, 'prob_bio_model_score')

        # tabular ML results, cardio-biomechanics, dna-cardio-biomechanics by Age & by Horse Type
        def get_tabular_measures_stats(df: pd.DataFrame, prob_field_name, field_type) -> list[dict]:
            dfx = df[[field_type, 'elite', 'date_of_measure', 'horse_id', prob_field_name]]
            dfx = dfx[~dfx[prob_field_name].isnull()].drop_duplicates(subset=['horse_id', 'date_of_measure']).drop(
                columns=['horse_id', 'date_of_measure'])
            dfx = dfx.groupby([field_type, 'elite', prob_field_name], as_index=False).value_counts()
            dfx = pd.DataFrame(dfx)
            df_out = dfx.rename(columns={'count': 'counts'}).reset_index().rename(
                columns={prob_field_name: 'score'}).drop(columns=['index', ])
            return df_out.to_dict(orient='records')

        # biomechanics_age_tabular_data = get_tabular_measures_stats(merged_df, 'prob_bio_model_score', 'horse_type')
        # biomechanics_horse_tabular_data = get_tabular_measures_stats(merged_df, 'prob_bio_model_score', 'type')

        cardio_biomechanics_age_tabular_data = get_tabular_measures_stats(merged_df, 'prob_cardio_bio_model_score',
                                                                          'horse_type')
        cardio_biomechanics_type_tabular_data = get_tabular_measures_stats(merged_df, 'prob_cardio_bio_model_score',
                                                                           'type')
        dna_cardio_biomechanics_age_tabular_data = get_tabular_measures_stats(merged_df,
                                                                              'prob_dna_cardio_bio_model_score',
                                                                              'horse_type')
        dna_cardio_biomechanics_type_tabular_data = get_tabular_measures_stats(merged_df,
                                                                               'prob_dna_cardio_bio_model_score',
                                                                               'type')

        # Tabular ML Models Metadata
        optimal_distance_model = MLModelMetadata.objects.filter(name='optimal-distance').order_by(
            '-creation_time').first()
        biomechanics_model = MLModelMetadata.objects.filter(name='biomechanics').order_by('-creation_time').first()
        cardio_biomechanics_model = MLModelMetadata.objects.filter(name='cardio-biomechanics').order_by(
            '-creation_time').first()
        dna_cardio_biomechanics_model = MLModelMetadata.objects.filter(name='dna-cardio-biomechanics').order_by(
            '-creation_time').first()
        conformation_model = MLModelMetadata.objects.filter(name='morph-images-conformation-tabular').order_by(
            '-creation_time').first()
        optimal_distance_model_data = {}
        biomechanics_model_data = {}
        cardio_biomechanics_model_data = {}
        dna_cardio_biomechanics_model_data = {}
        conformation_model_data = {}
        if optimal_distance_model:
            optimal_distance_model_data = optimal_distance_model.__dict__
            optimal_distance_model_data.pop('_state', None)
        if biomechanics_model:
            biomechanics_model_data = biomechanics_model.__dict__
            biomechanics_model_data.pop('_state', None)
        if cardio_biomechanics_model:
            cardio_biomechanics_model_data = cardio_biomechanics_model.__dict__
            cardio_biomechanics_model_data.pop('_state', None)
        if dna_cardio_biomechanics_model:
            dna_cardio_biomechanics_model_data = dna_cardio_biomechanics_model.__dict__
            dna_cardio_biomechanics_model_data.pop('_state', None)
        if conformation_model:
            conformation_model_data = conformation_model.__dict__
            conformation_model_data.pop('_state', None)

        out = {
            'population': {
                'biomechanics': {
                    'all': population_biomechanics_all,
                    'elite': population_biomechanics_elite,
                    'non_elite': population_biomechanics_non_elite
                },
                'cardio': {
                    'all': population_cardio_all,
                    'elite': population_cardio_elite,
                    'non_elite': population_cardio_non_elite
                }
            },
            'cardio': {
                'age': cardio_score_age,
                'cluster': cardio_score_cluster,
                'type': cardio_score_type
            },
            'biomechanics': {
                'age': biomechanics_score_age,
                'cluster': biomechanics_score_cluster,
                'type': biomechanics_score_type
            },
            'cardio_biomechanics': {
                'age': cardio_biomechanics_age_tabular_data,
                'type': cardio_biomechanics_type_tabular_data
            },
            'dna_cardio_biomechanics': {
                'age': dna_cardio_biomechanics_age_tabular_data,
                'type': dna_cardio_biomechanics_type_tabular_data
            },
            'conformation': {
                'age': image_measurements_scores_data,
                'type': image_measurements_horse_types_data
            },
            'ml_models_metadata': {
                'optimal_distance': optimal_distance_model_data,
                'biomechanics': biomechanics_model_data,
                'cardio_biomechanics': cardio_biomechanics_model_data,
                'dna_cardio_biomechanics': dna_cardio_biomechanics_model_data,
                'conformation': conformation_model_data,
            }
        }
        return Response(out)


class MeasureAPIView(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', ]
    ordering_fields = '__all__'
    permission_classes = (permissions.IsAuthenticated,)

    def get_user_action_data(self, request_data: dict, response_data: dict):
        horse_id = request_data.get('horse', '')
        if not horse_id:  # for partial update, horse is not in the request data
            horse_id = response_data.get('horse')
        gcs_path = request_data.get('gcs_path', '')
        measure_id = response_data.get('id')
        cardio_video = request_data.get('cardio_video', {})
        action = ''
        metadata = {}
        if gcs_path:
            action = 'biomechanics_video_upload'
            metadata['gcs_path'] = gcs_path
        if cardio_video:
            action = 'cardio_video_upload'
            metadata['gcs_path'] = cardio_video['path']
        return {
            'horse_id': horse_id,
            'action': action,
            'metadata': metadata,
            'measure_id': measure_id
        }

    def create(self, request, *args, **kwargs):

        resp = super().create(request, *args, **kwargs)
        user = request.user
        user_action_data = self.get_user_action_data(self.request.data, resp.data)
        user_action_data['user'] = user
        UserAction.objects.create(**user_action_data)

        return resp

    def partial_update(self, request, *args, **kwargs):
        resp = super().partial_update(request, *args, **kwargs)
        user = request.user
        user_action_data = self.get_user_action_data(self.request.data, resp.data)
        user_action_data['user'] = user
        UserAction.objects.create(**user_action_data)
        return resp

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def score(self, request, pk):
        """scores cardio-biomechanics and dna-cardio-biomechanics"""

        measure = self.get_object()
        measure.score_dna_cardio_biomechanics()
        measure.save()

        out = {'results': {
            'prob_cardio_bio_model': measure.prob_cardio_bio_model,
            'prob_dna_cardio_bio_model': measure.prob_dna_cardio_bio_model
        }
        }

        return Response(out)

    @action(detail=False, methods=['post'], serializer_class=MeasureFileSerializer)
    def get_measure_by_file(self, request):
        """Find measure by file (video, image) stored in GCS"""
        serializer = MeasureFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_gcs_uri = serializer.data['gcs_uri']
        gcs_blob = GCSBlob.create_from_uri(file_gcs_uri)

        fields = ['dlc_gaf_image', 'gcs_gs_uri', 'cardio_video', 'dlc_video']
        measure = None
        for field in fields:
            query_filter = {field: gcs_blob}
            try:
                measure = Measure.objects.get(**query_filter)
                break
            except Measure.DoesNotExist:
                pass
        if measure:
            measure = MeasureSerializer(measure).data
            return Response(measure)
        else:
            raise NotFound(code=404)

    @action(detail=False, serializer_class=TabularMLUpdate, methods=['post'])
    def update_ml_tabular(self, request):

        request_data = request.data
        serializer = TabularMLUpdate(data=request_data)
        serializer.is_valid(raise_exception=True)
        update_fields = serializer.data['update_fields']
        search_fields = serializer.data['search_fields']

        horse_fields = [f.name for f in Horse._meta.get_fields()]
        measure_fields = [f.name for f in Measure._meta.get_fields()]

        measure_filters = {}
        cardio_filters = {}
        for field_name, field_val in search_fields.items():
            if field_name in horse_fields:
                measure_filters[f'horse__{field_name}'] = field_val
                cardio_filters[f'horse__{field_name}'] = field_val
            elif field_name in measure_fields:
                if 'cardio' in field_name:
                    cardio_filters[field_name] = field_val
                else:
                    measure_filters[field_name] = field_val
        cardio_fields = any(['cardio' in c for c in cardio_filters.keys()])
        if cardio_fields:  # check if there are really cardio fields
            measures = Measure.objects.filter(Q(**measure_filters) | Q(**cardio_filters))
        else:
            measures = Measure.objects.filter(Q(**measure_filters))

        for measure in measures:
            logging.debug(f'updating measure {measure.id} horse {measure.horse_id} date {measure.date_of_measure}')
            for fn, fv in update_fields.items():
                setattr(measure, fn, fv)
            measure.save()

        if measures:
            updates_measures = [m.id for m in measures]
            return Response({'updated_measures': updates_measures})
        else:
            raise NotFound(code=404)

    @action(detail=False, methods=['post'], serializer_class=MeasureMLUpdateSerializer)
    def update_ml_data(self, request):
        serializer = MeasureMLUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gcs_gs_uri = serializer.data['gcs_gs_uri']
        confidence = serializer.data['biomechanics_video_probability']
        measures = Measure.objects.filter(gcs_gs_uri=gcs_gs_uri).all()
        updated_ids = []
        for measure in measures:
            measure.biomechanics_video_probability = confidence
            measure.save()
            updated_ids.append(measure.id)
        return Response({'updated_objects': updated_ids})

    @action(detail=False, methods=['post'], serializer_class=MeasureMLGCSUpdateSerializer)
    def update_ml_gcs_data(self, request):
        serializer = MeasureMLGCSUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dlc_gaf_image_uri = serializer.data.get('dlc_gaf_image_uri', '')
        dlc_jrg_image_uri = serializer.data.get('dlc_jrg_image_uri')
        dlc_video_gs_uri = serializer.data.get('dlc_video_gs_uri', '')
        cardio_video_uri = serializer.data.get('cardio_video_uri', '')
        biomechanics_raw_video_uri = serializer.data.get('gcs_gs_uri')

        print(f"received data: {dict(serializer.data.items())}")
        measures = None
        if dlc_gaf_image_uri:
            dlc_gaf_gcs_blob = GCSBlob.create_from_uri(dlc_gaf_image_uri)
            measures = Measure.objects.filter(dlc_gaf_image=dlc_gaf_gcs_blob)

        if not measures and dlc_video_gs_uri:
            dlc_video_gs_blob = GCSBlob.create_from_uri(dlc_video_gs_uri)
            measures = Measure.objects.filter(dlc_video=dlc_video_gs_blob)

        if not measures and cardio_video_uri:
            cardio_video_gs_blob = GCSBlob.create_from_uri(cardio_video_uri)
            measures = Measure.objects.filter(cardio_video=cardio_video_gs_blob)

        if not measures and dlc_jrg_image_uri:
            dlc_jrg_gcs_blob = GCSBlob.create_from_uri(dlc_jrg_image_uri)
            measures = Measure.objects.filter(dlc_jrg_image=dlc_jrg_gcs_blob)

        if not measures and biomechanics_raw_video_uri:
            measures = Measure.objects.filter(gcs_gs_uri=biomechanics_raw_video_uri)

        if not measures:
            return Response({
                f"Couldn't find measure with {dlc_gaf_image_uri} {dlc_video_gs_uri} {cardio_video_uri} {dlc_jrg_image_uri}"},
                status=404)

        fields_for_update = (
            'biomechanics_gaf_probability', 'biomechanics_gaf_score', 'biomechanics_keypoint_probability',
            'biomechanics_keypoint_score', 'cardio_video_probability', 'cardio_cluster', 'dlc_jrg_probability',
            'biomechanics_video_probability'
        )
        for measure in measures:
            for field_name in fields_for_update:
                field_value = serializer.data[field_name]
                if field_value:
                    setattr(measure, field_name, field_value)
            measure.save()
        measure_ids = [m.id for m in measures]
        return Response({'updated_object': measure_ids})

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'partial_update'):
            return MeasureSerializer
        else:
            return MeasureCreateSerializer


class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user_create_serializer = UserCreateSerializer(data=request.data)
        user_create_serializer.is_valid(raise_exception=True)
        user = user_create_serializer.save()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        password = validated_data.get('password', '')
        validated_data.pop('password', None)
        user = serializer.update(user, validated_data)
        if password:
            user.set_password(password)
            user.save()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return UserCreateSerializer
        else:
            return UserSerializer

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny],
            serializer_class=UserLoginSerializer)
    def login(self, request):
        user_credentials = UserLoginSerializer(data=request.data)
        user_credentials.is_valid(raise_exception=True)
        username = user_credentials.data['email']
        password = user_credentials.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email
            })

        return Response(status=403, data={'error': "Not authenticated"})

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated],
            authentication_classes=(TokenAuthentication,)
            )
    def logout(self, request):
        logout(request)
        return Response({'resp': 'ok'})


class ImageMeasurementAPIView(viewsets.ModelViewSet):
    queryset = ImageMeasurement.objects.all()
    serializer_class = ImageMeasurementSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False, methods=['post'], serializer_class=MorphImageMLUpdateSerializer)
    def update_ml_gcs_data(self, request):
        serializer = MorphImageMLUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_gcs_uri = serializer.data.get('image')
        prob_image = serializer.data.get('prob_image')
        image = GCSBlob.create_from_uri(image_gcs_uri)
        image_measurements = ImageMeasurement.objects.filter(image=image)
        for im in image_measurements:
            im.prob_image = prob_image
            im.save()
        measure_ids = [m.id for m in image_measurements]
        return Response({'updated_object': measure_ids})

    @action(detail=False, serializer_class=TabularMLUpdate, methods=['post'])
    def update_ml_tabular(self, request):

        request_data = request.data
        serializer = TabularMLUpdate(data=request_data)
        serializer.is_valid(raise_exception=True)
        update_fields = serializer.data['update_fields']
        search_fields = serializer.data['search_fields']

        measures = ImageMeasurement.objects.filter(Q(**search_fields))

        for measure in measures:
            logging.debug(f'updating image measurement {measure.id} with the data {update_fields}')
            for fn, fv in update_fields.items():
                setattr(measure, fn, fv)
            measure.save()

        if measures:
            updated_measures = [m.id for m in measures]
            return Response({'updated_measures': updated_measures})
        else:
            raise NotFound(code=404)


class CountryWeightAPIView(viewsets.ModelViewSet):
    queryset = CountryWeight.objects.all()
    serializer_class = CountryWeightSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MLModelMetadataAPIView(viewsets.ModelViewSet):
    queryset = MLModelMetadata.objects.all()
    serializer_class = MLModelMetadataSerializer

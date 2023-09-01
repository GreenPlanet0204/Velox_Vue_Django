import json
from rest_framework import serializers
from .models import Horse, Measure, User, ImageMeasurement, CountryWeight, MLModelMetadata


class GCSBlobSerializer(serializers.Field):
    """Serializer for GCS Blob object"""

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError('data needs to be in the form of dictionary')
        if 'bucket' not in data.keys():
            raise serializers.ValidationError('Missing required field "bucket"')
        if 'filename' not in data.keys():
            raise serializers.ValidationError('Missing required field "filename"')
        obj = {
            'bucket': data.get('bucket', ''),
            'filename': data.get('filename', ''),
            'path': data.get('path', ''),
        }
        return json.dumps(obj)

    def to_representation(self, value):
        if not value:
            return None
        if isinstance(value, str):
            try:
                data = json.loads(value)
                return data
            except ValueError:
                print(value)
                return {}
        else:
            return value.to_dict()


class MeasureFileSerializer(serializers.Serializer):
    gcs_uri = serializers.CharField(required=True)


class SignedUrlSerializer(serializers.Serializer):
    filename = serializers.CharField(required=True)
    content_type = serializers.CharField(required=True)
    video_type = serializers.ChoiceField(choices=(('video', 'video'), ('cardio', 'cardio'),
                                                  ('image_measurement', 'image_measurement')), required=False)
    file_type = serializers.ChoiceField(choices=(('video', 'video'), ('cardio', 'cardio'),
                                                 ('image_measurement', 'image_measurement')), required=False)
    date_of_measure = serializers.CharField(required=True)


class MeasureCreateSerializer(serializers.ModelSerializer):
    dlc_video = GCSBlobSerializer(required=False)
    dlc_h5_file = GCSBlobSerializer(required=False)
    dlc_gaf_image = GCSBlobSerializer(required=False)
    cardio_video = GCSBlobSerializer(required=False)

    class Meta:
        model = Measure
        fields = ('id', 'horse', 'date_of_measure', 'video_qc', 'gcs_bucket', 'gcs_path', 'gcs_filename', 'dlc_video',
                  'dlc_h5_file', 'dlc_gaf_image', 'cardio_video', 'cardio_type',
                  'biomechanics_video_probability', 'biomechanics_video_score', 'biomechanics_operation_id'
                  )


class MeasureSerializer(serializers.ModelSerializer):
    dlc_video = GCSBlobSerializer(required=False, allow_null=True)
    dlc_h5_file = GCSBlobSerializer(required=False, allow_null=True)
    dlc_gaf_image = GCSBlobSerializer(required=False, allow_null=True)
    dlc_jrg_image = GCSBlobSerializer(required=False, allow_null=True)
    cardio_video = GCSBlobSerializer(required=False, allow_null=True)

    class Meta:
        model = Measure
        fields = ('id', 'horse', 'date_of_measure', 'days_old',
                  'biomechanics_video_probability', 'biomechanics_video_score', 'biomechanics_operation_id',
                  'biomechanics_gaf_probability', 'biomechanics_gaf_score',
                  'biomechanics_keypoint_probability', 'biomechanics_keypoint_score', 'biomechanics_cluster',
                  'measure_age', 'measure_type',
                  'dlc_video', 'dlc_h5_file', 'dlc_gaf_image',
                  'gcs_bucket', 'gcs_path', 'gcs_filename', 'gcs_gs_uri',
                  'dlc_video_url', 'dlc_video_gs_uri', 'dlc_h5_file_url', 'dlc_h5_file_uri', 'dlc_gaf_image_url',
                  'dlc_gaf_image_uri', 'video_url',
                  'dlc_jrg_image', 'dlc_jrg_image_url', 'dlc_jrg_image_uri',
                  'cardio_video', 'cardio_type',
                  'cardio_video_probability', 'cardio_video_score', 'cardio_video_url', 'cardio_video_uri',
                  'cardio_cluster', 'dlc_jrg_score', 'dlc_jrg_probability',
                  'prob_bio_model', 'prob_bio_model_score',
                  'prob_cardio_bio_model', 'prob_cardio_bio_model_score',
                  'prob_dna_cardio_bio_model', 'prob_dna_cardio_bio_model_score',
                  'gcs_url', 'created_at', 'updated_at',
                  )


class ImageMeasurementSerializer(serializers.ModelSerializer):
    image = GCSBlobSerializer(required=False, allow_null=True)

    class Meta:
        model = ImageMeasurement
        fields = '__all__'


class MeasureMLUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = (
            'biomechanics_video_probability', 'biomechanics_video_score', 'biomechanics_operation_id', 'gcs_gs_uri')


class MeasureMLGCSUpdateSerializer(serializers.ModelSerializer):
    """Accepts updates for GCS fields"""
    dlc_gaf_image_uri = serializers.CharField(required=False)
    dlc_video_gs_uri = serializers.CharField(required=False)
    cardio_video_uri = serializers.CharField(required=False)
    dlc_jrg_image_uri = serializers.CharField(required=False)
    gcs_gs_uri = serializers.CharField(required=False)

    class Meta:
        model = Measure
        fields = (
            'biomechanics_gaf_probability', 'biomechanics_gaf_score', 'biomechanics_keypoint_probability',
            'biomechanics_keypoint_score', 'dlc_gaf_image_uri', 'dlc_video_gs_uri',
            'dlc_jrg_image_uri', 'dlc_jrg_probability',
            'cardio_video_uri', 'cardio_cluster', 'cardio_video_probability', 'cardio_video_score',
            'gcs_gs_uri', 'biomechanics_video_probability'
        )


class TabularMLUpdate(serializers.Serializer):
    update_fields = serializers.DictField(required=True)
    search_fields = serializers.DictField(required=True)


class HorseSerializer(serializers.ModelSerializer):
    measures = MeasureSerializer(many=True, read_only=True)
    image_measurements = ImageMeasurementSerializer(many=True, read_only=True)

    class Meta:
        model = Horse
        fields = ('id', 'name', 'type', 'sex', 'date_of_birth', 'starts', 'date_last_start', 'country', 'tf_reg',
                  'race_rating', 'active', 'elite', 'status', 'optimal_distance', 'distance1', 'distance2', 'size1',
                  'class1', 'class2', 'class3', 'update_days', 'start_days', 'days_old',
                  'measures', 'image_measurements', 'sire', 'dam', 'broodmare_sire', 'country_code', 'starts_country',
                  'avg_distance_raced', 'hurdle', 'cpi_rating',
                  'pred_opt_dist',
                  'created_at', 'updated_at',
                  )


class HorseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horse
        fields = ('id', 'name', 'type', 'sex', 'date_of_birth', 'starts', 'date_last_start', 'country', 'tf_reg',
                  'race_rating', 'active', 'elite', 'status', 'optimal_distance', 'distance1', 'distance2', 'size1',
                  'class1', 'class2', 'class3', 'update_days', 'start_days', 'days_old',
                  'measures', 'image_measurements', 'sire', 'dam', 'broodmare_sire', 'country_code', 'starts_country',
                  'avg_distance_raced', 'hurdle', 'cpi_rating',
                  'created_at', 'updated_at'
                  )

class ShortlistSerializerTable(serializers.Serializer):
    horse_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    sire = serializers.CharField(read_only=True)
    active = serializers.CharField(read_only=True)
    elite = serializers.CharField(read_only=True)
    date_of_birth = serializers.CharField(read_only=True)
    date_of_measure = serializers.CharField(read_only=True)
    prob_bio_model = serializers.DecimalField(read_only=True, max_digits=4, decimal_places=3)
    prob_conform_model = serializers.DecimalField(read_only=True, max_digits=4, decimal_places=3)
    cum_prob = serializers.DecimalField(read_only=True, max_digits=4, decimal_places=3)

class ShortlistSerializer(serializers.Serializer):
    items = ShortlistSerializerTable(many=True, read_only=True)
    total_number = serializers.IntegerField(read_only=True)
    total_number_active = serializers.IntegerField(read_only=True)

class MorphImageMLUpdateSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=True)

    class Meta:
        model = ImageMeasurement
        fields = ('prob_image', 'image')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=5)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserPasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class CountryWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryWeight
        fields = '__all__'


class MLModelMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModelMetadata
        fields = '__all__'

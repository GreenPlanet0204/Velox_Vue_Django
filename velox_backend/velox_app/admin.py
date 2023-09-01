from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin

from .models import Horse, Measure, User, ImageMeasurement, CountryWeight, MLModelMetadata, ScoreBins, UserAction


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


@admin.register(Horse)
class HorseAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields = ('start_days', 'update_days', 'created_at', 'updated_at')


def get_url(instance, field_name):
    val = getattr(instance, field_name)
    return format_html(
        '<a href="{0}" target="_blank">{1}</a>',
        val,
        val,
    )


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    fields = ('horse', 'date_of_measure', 'days_old', 'measure_age', 'measure_type',
              # 'gcs_bucket', 'gcs_path', 'gcs_filename',
              'gcs_url', 'gcs_gs_uri', 'biomechanics_video_probability', 'biomechanics_video_score',
              'biomechanics_operation_id', 'biomechanics_cluster',
              'biomechanics_gaf_probability', 'biomechanics_gaf_score',
              'biomechanics_keypoint_probability', 'biomechanics_keypoint_score',
              'cardio_video_probability', 'cardio_video_score',
              'cardio_type', 'cardio_cluster',
              'video_url',
              'dlc_video_url', 'dlc_video_gs_uri', 'dlc_h5_file_url', 'dlc_h5_file_uri', 'dlc_gaf_image_url',
              'dlc_gaf_image_uri', 'cardio_video_uri', 'cardio_video_url',
              'dlc_jrg_score', 'dlc_jrg_probability',
              'prob_bio_model', 'prob_bio_model_score',
              'prob_cardio_bio_model', 'prob_cardio_bio_model_score',
              'prob_dna_cardio_bio_model', 'prob_dna_cardio_bio_model_score',
              # 'dlc_video', 'dlc_h5_file', 'dlc_gaf_image',
              'created_at', 'updated_at')
    readonly_fields = ('gcs_url', 'gcs_gs_uri', 'dlc_video_url', 'dlc_video_gs_uri', 'dlc_h5_file_url',
                       'dlc_gaf_image_url', 'dlc_gaf_image_uri', 'dlc_h5_file_uri',
                       'cardio_video_uri', 'cardio_video_url', 'video_url',
                       'dlc_jrg_image_url', 'dlc_jrg_image_uri',
                       'measure_age', 'measure_type', 'created_at', 'updated_at')

    def gcs_url(self, instance):
        return get_url(instance, 'gcs_url')

    def dlc_video_url(self, instance):
        return get_url(instance, 'dlc_video_url')

    def dlc_h5_file_url(self, instance):
        return get_url(instance, 'dlc_h5_file_url')

    def dlc_gaf_image_url(self, instance):
        return get_url(instance, 'dlc_gaf_image_url')

    def cardio_video_url(self, instance):
        return get_url(instance, 'cardio_video_url')

    search_fields = (
        "gcs_gs_uri",
    )


@admin.register(MLModelMetadata)
class MLModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageMeasurement)
class ImageMeasurementAdmin(admin.ModelAdmin):
    fields = ('horse', 'date_of_measure', 'morph_data', 'calculated_data', 'prob_image', 'prob_conform_model',
              'prob_conform_model_score',
              'image_uri', 'image_url',
              'back_length', 'body_length', 'cannon', 'femur', 'femur_angle', 'fetlock', 'fetlock_angle',
              'forearm_angle', 'forelimb', 'front_pastern', 'hind_fetlock_angle', 'hind_cannon', 'hip_angle',
              'hock_angle', 'humerus', 'imbalance', 'ischium_hock', 'neck', 'pelvis', 'pelvis_horizontal',
              'pelvis_femur', 'proportion', 'scope', 'shoulder', 'shoulder_angle', 'shoulder_horizontal', 'thrust',
              'tibia', 'triangle', 'procrustes_distance', 'leg_length', 'forelimb_length', 'hind_length_distance',
              'neck_length_ratio', 'forelimb_hind_ratio', 'leg_back_ratio', 'body_hind_ratio'
              )
    readonly_fields = ('image_uri', 'image_url', 'back_length',
                       'back_length', 'body_length', 'cannon', 'femur', 'femur_angle', 'fetlock', 'fetlock_angle',
                       'forearm_angle', 'forelimb', 'front_pastern', 'hind_fetlock_angle', 'hind_cannon', 'hip_angle',
                       'hock_angle', 'humerus', 'imbalance', 'ischium_hock', 'neck', 'pelvis', 'pelvis_horizontal',
                       'pelvis_femur', 'proportion', 'scope', 'shoulder', 'shoulder_angle', 'shoulder_horizontal',
                       'thrust',
                       'tibia', 'triangle', 'procrustes_distance',
                       'leg_length', 'forelimb_length', 'hind_length_distance', 'neck_length_ratio',
                       'forelimb_hind_ratio', 'leg_back_ratio', 'body_hind_ratio'
                       )

    def image_url(self, instance):
        return get_url(instance, 'image_url')


@admin.register(CountryWeight)
class CountryWeightAdmin(admin.ModelAdmin):
    pass


@admin.register(ScoreBins)
class ScoreBinsAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_filter = ('user', 'action')
    readonly_fields = ('created_at', 'updated_at')

import logging
from django.db import migrations, models
from ..models import ImageMeasurement


def set_field_values(im: ImageMeasurement):
    if not im.calculated_data:
        return

    try:
        angels = im.calculated_data.get('angels')
        bones = im.calculated_data.get('bones')
        factors = im.calculated_data.get('factors')
        procrustes_distance = im.calculated_data.get('procrustesDistance')

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

        im.back_length = data['Backlength']
        im.body_length = data['Bodylength']
        im.cannon = data['Cannon']
        im.femur = data['Femur']
        im.femur_angle = data['Femur Angle']
        im.fetlock = data['Fetlock']
        im.fetlock_angle = data['Fetlock Angle']
        im.forearm_angle = data['Forearm Angle']
        im.forelimb = data['Forelimb']
        im.front_pastern = data['Front Pastern']
        im.hind_fetlock_angle = data['Hind Fetlock Angle']
        im.hind_cannon = data['HindCannon']
        im.hip_angle = data['Hip Angle']
        im.hock_angle = data['Hock Angle']
        im.humerus = data['Humerus']
        im.imbalance = data['Imblance']
        im.ischium_hock = data['Ischium-Hock']
        im.neck = data['Neck']
        im.pelvis = data['Pelvis']
        im.pelvis_horizontal = data['Pelvis Horizontal']
        im.pelvis_femur = data['Pelvis-Femur']
        im.proportion = data['Proportion']
        im.scope = data['Scope']
        im.shoulder = data['Shoulder']
        im.shoulder_angle = data['Shoulder Angle']
        im.shoulder_horizontal = data['Shoulder Horizontal']
        im.thrust = data['Thrust']
        im.tibia = data['Tibia']
        im.triangle = data['Triangle']
        im.procrustes_distance = procrustes_distance
    except Exception as e:
        logging.error(f"skipping due to the error: {im.id} {e}")
        return
    return im


def update_image_measurements(apps, schema_editor):
    """set cardio_type for all relevant Measures"""
    logging.info('starting migration')
    ImageMeasurement = apps.get_model('velox_app', 'ImageMeasurement')
    measures = ImageMeasurement.objects.all()
    for im in measures:
        im = set_field_values(im)
        if im:
            im.save()
            logging.info(f"updating ImageMeasurement {im.id}")
    logging.info('migration completed')


class Migration(migrations.Migration):
    dependencies = [
        ('velox_app', '0042_auto_20230327_1513'),
    ]

    operations = [
        migrations.RunPython(update_image_measurements, migrations.RunPython.noop)
    ]

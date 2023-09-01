"""This script does 2 things:
1. swap values in bones for fields Cannon and Front Pastern
2. rename second field Cannon for Hind Cannon
"""

import json
import logging
from django.db import migrations, models

def update_calculated_data(calculated_data):
    bones = calculated_data['bones']
    cannon_value = None
    front_pastern_value = None
    hind_cannon_value = None
    for i, item in enumerate(bones):
        bone_name = item['boneName']
        distance = item['distance']
        if bone_name == 'Cannon':
            if not front_pastern_value:
                front_pastern_value = distance  # swap values with Cannon and Front Pastern
            else:
                hind_cannon_value = distance  # second Cannon field that we are now renaming
        elif bone_name == 'Front Pastern':
            cannon_value = distance

    updated_cannon = False
    for i, item in enumerate(bones):
        bone_name = item['boneName']
        if bone_name == 'Cannon':
            if not updated_cannon:
                bones[i]['distance'] = cannon_value
                updated_cannon = True
            else:
                bones[i]['distance'] = hind_cannon_value
                bones[i]['boneName'] = 'HindCannon'
        elif bone_name == 'Front Pastern':
            bones[i]['distance'] = front_pastern_value
    calculated_data['bones'] = bones
    return calculated_data


def update_image_measurements(apps, schema_editor):
    """set cardio_type for all relevant Measures"""
    logging.info('starting migration')
    ImageMeasurement = apps.get_model('velox_app', 'ImageMeasurement')
    measures = ImageMeasurement.objects.all()
    for measure in measures:
        calculated_data = measure.calculated_data
        if not calculated_data:
            continue
        calculated_data_updated = update_calculated_data(calculated_data)
        measure.calculated_data = calculated_data_updated
        measure.save()
        logging.info(f"updating ImageMeasurement {measure.id} old data: {calculated_data}, new data: {calculated_data_updated} ")
    logging.info('migration completed')


class Migration(migrations.Migration):
    dependencies = [
        ('velox_app', '0039_useraction'),
    ]

    operations = [
        migrations.RunPython(update_image_measurements, migrations.RunPython.noop)
    ]

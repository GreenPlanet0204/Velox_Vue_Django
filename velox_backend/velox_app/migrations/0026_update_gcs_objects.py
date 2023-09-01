"""Due to an error in API, when uploading video (biomechanics and cardio)
wrong filename was set in DB (bucket and path are ok) (basically not including timestamp prefix)
This script sets correct filename based on path field
"""
import logging
from django.db import migrations


def update_gcs_fields(apps, schema_editor):
    logging.info('starting migration')
    Measure = apps.get_model('velox_app', 'Measure')
    measures = Measure.objects.all()
    for measure in measures:
        cardio_video = measure.cardio_video
        # update cardio video
        if cardio_video:
            filename = cardio_video.filename
            path = cardio_video.path
            filename_path = path.split('/')[-1]
            if filename_path != filename:
                logging.info(f"updating {measure.id} cardio old filename: {filename}, new {filename_path}")
                cardio_video.filename = filename_path
                measure.cardio_video = cardio_video
                measure.save()
        # update biomechanics video
        gcs_path = measure.gcs_path
        gcs_filename = measure.gcs_filename
        if gcs_path and gcs_filename:
            gcs_filename_path = gcs_path.split('/')[-1]
            if gcs_filename_path != gcs_filename:
                logging.info(f"updating {measure.id} gcs old filename: {gcs_filename}, new {gcs_filename_path}")
                measure.gcs_filename = gcs_filename_path
                measure.save()
    logging.info('migration completed')


class Migration(migrations.Migration):
    dependencies = [
        ('velox_app', '0025_auto_20220303_1440'),
    ]

    operations = [
        migrations.RunPython(update_gcs_fields)
    ]

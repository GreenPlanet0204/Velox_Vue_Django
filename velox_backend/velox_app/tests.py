import json
import datetime
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APITestCase

from .models import GCSBlob, Measure, Horse, User, ScoreBins, ImageMeasurement


def setup_test_data():
    horse = Horse.objects.create(name='test_horse', type='Flat', sex='Male',
                                 race_rating=10,
                                 date_of_birth=datetime.date(2018, 3, 23),
                                 )
    data = {
        "bucket": "velox-biomechanics-data",
        "filename": "Aravingbeauty2DLC_resnet50_veloxDec16shuffle1_590000_GAF.png",
        "path": "deeplabcut_outputs/5/Aravingbeauty2DLC_resnet50_veloxDec16shuffle1_590000_GAF.png",
    }
    gcs_uri = 'gs://velox-biomechanics-data/deeplabcut_outputs/5/Aravingbeauty2DLC_resnet50_veloxDec16shuffle1_590000_GAF.png'
    gcs_gaf = GCSBlob(**data)
    measure = Measure.objects.create(
        horse=horse, date_of_measure=datetime.date(2020, 1, 1), days_old=100, video_qc='OK', dlc_gaf_image=gcs_gaf
    )

    user = User.objects.create_user('user@test.com', 'pass')
    return horse, measure, data, gcs_uri, user


class QueryGCSTest(TestCase):

    def setUp(self) -> None:
        horse, measure, data, gcs_uri, user = setup_test_data()
        self.horse = horse
        self.data = data
        self.measure = measure
        self.gcs_uri = gcs_uri
        self.client.force_login(user)

    def test_query(self):
        gcs = GCSBlob(**self.data)
        measure = Measure.objects.get(dlc_gaf_image=gcs)
        self.assertEqual(measure.id, self.measure.id)
        self.assertEqual(measure.dlc_gaf_image.uri, gcs.uri)


class TestUpdateMLData(APITestCase):

    def setUp(self) -> None:
        horse, measure, data, gcs_uri, user = setup_test_data()
        self.horse = horse
        self.data = data
        self.measure = measure
        self.gcs_uri = gcs_uri
        self.client.force_login(user)

    def test_post_updates(self):
        biomechanics_gaf_probability = Decimal('0.12345')
        biomechanics_gaf_score = 'D'
        biomechanics_keypoint_probability = Decimal('0.999999')
        biomechanics_keypoint_score = 'A+'
        gaf_gcs_uri = self.gcs_uri
        input_data = {
            'biomechanics_gaf_probability': biomechanics_gaf_probability,
            'biomechanics_gaf_score': biomechanics_gaf_score,
            'biomechanics_keypoint_probability': biomechanics_keypoint_probability,
            'biomechanics_keypoint_score': biomechanics_keypoint_score,
            'dlc_gaf_image_uri': gaf_gcs_uri
        }
        url = f'/velox/api/measures/update_ml_gcs_data/'
        response = self.client.post(url, input_data, format='json')
        self.assertEqual(response.status_code, 200)

        measure = Measure.objects.get(pk=self.measure.pk)
        self.assertEqual(measure.biomechanics_gaf_probability, biomechanics_gaf_probability)
        self.assertEqual(measure.biomechanics_gaf_score, biomechanics_gaf_score)
        self.assertEqual(measure.biomechanics_keypoint_probability, biomechanics_keypoint_probability)
        self.assertEqual(measure.biomechanics_keypoint_score, biomechanics_keypoint_score)


class TestRawVideoMLUpdate(APITestCase):

    def setUp(self) -> None:
        horse = Horse.objects.create(name='test_horse', type='Flat', sex='Male',
                                     date_of_birth=datetime.date(2019, 1, 1),
                                     )

        bucket = "velox-biomechanics-data-test"
        filename = "Aravingbeauty2DLC_resnet50_veloxDec16shuffle1_590000_GAF.png"
        path = f"deeplabcut_outputs/5/{filename}"

        gcs_uri = f'gs://{bucket}/{path}'
        measure = Measure.objects.create(
            horse=horse,
            date_of_measure=datetime.date(2020, 1, 1), days_old=100, video_qc='OK',
            gcs_bucket=bucket,
            gcs_filename=filename,
            gcs_path=path,
            # gcs_gs_uri=gcs_uri
        )

        user = User.objects.create_user('user@test.com', 'pass')
        self.horse = horse
        self.measure = measure
        self.gcs_uri = gcs_uri
        self.client.force_login(user)

    def test_raw_video_ml_update(self):
        probability = Decimal('0.12345')
        input_data = {
            'gcs_gs_uri': self.gcs_uri,
            'biomechanics_video_probability': probability
        }
        url = '/velox/api/measures/update_ml_gcs_data/'
        response = self.client.post(url, input_data, format='json')
        self.assertEqual(response.status_code, 200)

        measure = Measure.objects.get(pk=self.measure.pk)
        self.assertEqual(measure.biomechanics_video_probability, probability)
        self.assertEqual(measure.gcs_gs_uri, self.gcs_uri)


class TestCardioUpdate(APITestCase):

    def setUp(self) -> None:
        horse = Horse.objects.create(name='test_horse', type='Flat', sex='Male',
                                     date_of_birth=datetime.date(2019, 1, 1),
                                     )
        data = {
            "bucket": "velox-biomechanics-dev",
            "filename": "Aravingbeauty2.mp4",
            "path": "raw/cardio_videos/Aravingbeauty2.mp4",
        }
        gcs_uri = 'gs://velox-biomechanics-dev/raw/cardio_videos/Aravingbeauty2.mp4'
        gcs_blob = GCSBlob(**data)
        measure = Measure.objects.create(
            horse=horse, date_of_measure=datetime.date(2020, 1, 1), days_old=100, video_qc='OK', cardio_video=gcs_blob
        )
        user = User.objects.create_user('user@test.com', 'pass')
        self.horse = horse
        self.data = data
        self.measure = measure
        self.gcs_uri = gcs_uri
        self.client.force_login(user)

    def test_update_cardio(self):
        cardio_cluster = 1
        cardio_video_probability = Decimal('0.2631312')
        gcs_uri = self.gcs_uri
        input_data = {
            'cardio_cluster': cardio_cluster,
            'cardio_video_probability': cardio_video_probability,
            'cardio_video_uri': gcs_uri
        }
        url = f'/velox/api/measures/update_ml_gcs_data/'
        response = self.client.post(url, input_data, format='json')
        self.assertEqual(response.status_code, 200)

        measure = Measure.objects.get(pk=self.measure.pk)
        self.assertEqual(measure.cardio_cluster, cardio_cluster)
        self.assertEqual(measure.cardio_video_probability, cardio_video_probability)
        self.assertEqual(measure.cardio_video_score, 'C')


class TestMeasureFileSearch(TestCase):

    def setUp(self) -> None:
        horse, measure, data, gcs_uri, user = setup_test_data()
        self.horse = horse
        self.data = data
        self.measure = measure
        self.gcs_uri = gcs_uri
        self.client.force_login(user)

    def test_measure_file_search(self):
        url = f'/velox/api/measures/get_measure_by_file/'
        input_data = {'gcs_uri': self.gcs_uri}
        response = self.client.post(url, data=input_data)
        self.assertEqual(response.status_code, 200)
        response_data = response.data
        self.assertEqual(self.measure.id, response_data['id'])

    def test_measure_file_search_not_found(self):
        url = f'/velox/api/measures/get_measure_by_file/'
        input_data = {'gcs_uri': 'gs://bucket/non-exist'}
        response = self.client.post(url, data=input_data)
        self.assertEqual(response.status_code, 404)


class TestTabularMLUpdate(APITestCase):

    def setUp(self) -> None:
        horse, measure, data, gcs_uri, user = setup_test_data()
        self.horse = horse
        self.data = data
        self.measure = measure
        self.gcs_uri = gcs_uri
        self.client.force_login(user)

    def test_update(self):

        fields = {'class3': 'AC', 'class1': 'CC', 'size1': 'TT', 'class2': 'GG', 'distance1': 'CC', 'distance2': 'CC'}
        for k, v in fields.items():
            setattr(self.horse, k, v)
        self.horse.save()
        update_field = 'optimal_distance'
        search_fields = fields
        result = '6-8f'
        input_data = {
            'update_fields': {update_field: result},
            'search_fields': search_fields,
        }
        url = '/velox/api/horses/update_ml_tabular/'
        response = self.client.post(url, data=input_data, format='json')
        self.assertEqual(response.status_code, 200)
        horse_updated = Horse.objects.get(id=self.horse.id)
        updated_val = getattr(horse_updated, update_field)
        self.assertEqual(result, updated_val)

    def test_update_empty_search_fields(self):
        fields = {'class3': 'AC', 'class1': 'CC', 'size1': 'TT', 'class2': 'GG', 'distance1': 'CC', 'distance2': 'CC'}
        for k, v in fields.items():
            setattr(self.horse, k, v)
        self.horse.save()
        update_field = 'optimal_distance'
        search_fields = fields
        result = '6-8f'
        input_data = {
            'update_fields': {update_field: result},
            'search_fields': None,
        }
        url = '/velox/api/horses/update_ml_tabular/'
        response = self.client.post(url, data=input_data, format='json')
        self.assertEqual(response.status_code, 200)
        horse_updated = Horse.objects.get(id=self.horse.id)
        updated_val = getattr(horse_updated, update_field)
        self.assertEqual(result, updated_val)


class TestTabularMeasuresMLUpdate(APITestCase):
    def setUp(self) -> None:
        horse, measure, data, gcs_uri, user = setup_test_data()
        self.horse = horse
        self.data = data
        self.measure = measure
        self.gcs_uri = gcs_uri
        self.client.force_login(user)

    def test_update_one_measure(self):
        from decimal import Decimal

        prediction_data = {"instance": {
            "dlc_jrg_probability": "0.192919510",
            "cardio_type": "Euro Bullseye Turf Sprinter",
            "cardio_video_probability": "0.591892240",
            "biomechanics_video_probability": "0.004605739",
            "cardio_cluster": "8",
            "race_rating": "10",
            "biomechanics_keypoint_probability": "0.175895260",
            "measure_type": "Flat Yearling",
            "biomechanics_gaf_probability": "0.248811740",
            "biomechanics_cluster": "5"
        },
            "prediction": {"scores": [0.7387619018554688, 0.26123806834220886],
                           "classes": ["No", "Yes"]}}

        self.horse.race_rating = 10
        self.horse.save()
        mes1 = Measure.objects.create(horse=self.horse,
                                      date_of_measure=datetime.date(2019, 7, 8),
                                      biomechanics_video_probability="0.0046057390",
                                      biomechanics_gaf_probability="0.2488117400",
                                      biomechanics_keypoint_probability="0.1758952600",
                                      biomechanics_cluster=5,
                                      cardio_video_probability="0.5918922400",
                                      cardio_cluster=8,
                                      cardio_type="Euro Bullseye Turf Sprinter",
                                      dlc_jrg_probability="0.192919510"
                                      )

        update_field = 'prob_cardio_bio_model'
        result = '0.7372244000'
        search_fields = prediction_data['instance']

        input_data = {
            'update_fields': {update_field: result},
            'search_fields': search_fields,
        }
        url = '/velox/api/measures/update_ml_tabular/'
        response = self.client.post(url, data=input_data, format='json')
        self.assertEqual(response.status_code, 200)

        updated_measures = []
        measures = Measure.objects.all()
        for measure in measures:
            val = getattr(measure, update_field)
            if val == Decimal(result):
                updated_measures.append(measure)

        self.assertEqual(len(updated_measures), 1)

    def test_update_multiple(self):
        prediction_data = {"instance": {
            "dlc_jrg_probability": "0.192919510",
            "cardio_type": "Euro Bullseye Turf Sprinter",
            "cardio_video_probability": "0.591892240",
            "biomechanics_video_probability": "0.004605739",
            "cardio_cluster": "8",
            "race_rating": "10",
            "biomechanics_keypoint_probability": "0.175895260",
            "measure_type": "Flat Yearling",
            "biomechanics_gaf_probability": "0.248811740",
            "biomechanics_cluster": "5"
        },
            "prediction": {"scores": [0.7387619018554688, 0.26123806834220886],
                           "classes": ["No", "Yes"]}}

        self.horse.race_rating = 10
        self.horse.save()
        mes1 = Measure.objects.create(horse=self.horse,
                                      date_of_measure=datetime.date(2019, 7, 8),
                                      biomechanics_video_probability="0.0046057390",
                                      biomechanics_gaf_probability="0.2488117400",
                                      biomechanics_keypoint_probability="0.1758952600",
                                      biomechanics_cluster=5,
                                      dlc_jrg_probability="0.192919510"
                                      )
        mes2 = Measure.objects.create(horse=self.horse,
                                      date_of_measure=datetime.date(2019, 7, 8),
                                      cardio_video_probability="0.5918922400",
                                      cardio_cluster=8,
                                      cardio_type="Euro Bullseye Turf Sprinter"
                                      )
        update_field = 'prob_cardio_bio_model'
        result = '0.7372244000'
        search_fields = prediction_data['instance']

        input_data = {
            'update_fields': {update_field: result},
            'search_fields': search_fields,
        }
        url = '/velox/api/measures/update_ml_tabular/'
        response = self.client.post(url, data=input_data, format='json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        updated_measures_resp = response_data['updated_measures']
        updated_measures = []
        measures = Measure.objects.all()
        for measure in measures:
            val = getattr(measure, update_field)
            if val == Decimal(result):
                updated_measures.append(measure)

        self.assertEqual(len(updated_measures), 2)
        self.assertListEqual(updated_measures_resp, [m.id for m in updated_measures])

    def test_update_multiple_dna(self):
        prediction_data = {"instance": {
            "dlc_jrg_probability": "0.192919510",
            "cardio_type": "Euro Bullseye Turf Sprinter",
            "cardio_video_probability": "0.591892240",
            "biomechanics_video_probability": "0.004605739",
            "cardio_cluster": "8",
            "race_rating": "10",
            "biomechanics_keypoint_probability": "0.175895260",
            "measure_type": "Flat Yearling",
            "biomechanics_gaf_probability": "0.248811740",
            "biomechanics_cluster": "5",
            "distance1": "ZX",
            "distance2": "XY"
        },
            "prediction": {"scores": [0.7387619018554688, 0.26123806834220886],
                           "classes": ["No", "Yes"]}}

        self.horse.race_rating = 10
        self.horse.distance1 = 'ZX'
        self.horse.distance2 = 'XY'
        self.horse.save()
        Horse.objects.create(date_of_birth=datetime.datetime(2019, 5, 5), name='another horse', type='Flat',
                             sex='Female')
        mes1 = Measure.objects.create(horse=self.horse,
                                      date_of_measure=datetime.date(2019, 7, 8),
                                      biomechanics_video_probability="0.0046057390",
                                      biomechanics_gaf_probability="0.2488117400",
                                      biomechanics_keypoint_probability="0.1758952600",
                                      biomechanics_cluster=5,
                                      dlc_jrg_probability="0.192919510"
                                      )
        mes2 = Measure.objects.create(horse=self.horse,
                                      date_of_measure=datetime.date(2019, 7, 8),
                                      cardio_video_probability="0.5918922400",
                                      cardio_cluster=8,
                                      cardio_type="Euro Bullseye Turf Sprinter"
                                      )
        update_field = 'prob_cardio_bio_model'
        result = '0.7372244000'
        search_fields = prediction_data['instance']

        input_data = {
            'update_fields': {update_field: result},
            'search_fields': search_fields,
        }
        url = '/velox/api/measures/update_ml_tabular/'
        response = self.client.post(url, data=input_data, format='json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        updated_measures_resp = response_data['updated_measures']
        updated_measures = []
        measures = Measure.objects.all()
        for measure in measures:
            val = getattr(measure, update_field)
            if val == Decimal(result):
                updated_measures.append(measure)

        self.assertEqual(len(updated_measures), 2)
        self.assertListEqual(updated_measures_resp, [m.id for m in updated_measures])

    def test_update_biomechanics(self):
        prediction_data = {"instance": {
            "dlc_jrg_probability": "0.192919510",
            "biomechanics_video_probability": "0.004605739",
            "race_rating": "10",
            "biomechanics_keypoint_probability": "0.175895260",
            "measure_type": "Flat Yearling",
            "biomechanics_gaf_probability": "0.248811740",
            "biomechanics_cluster": "5",
        },
            "prediction": {"scores": [0.7387619018554688, 0.26123806834220886],
                           "classes": ["No", "Yes"]}}

        self.horse.race_rating = 10
        self.horse.distance1 = 'ZX'
        self.horse.distance2 = 'XY'
        self.horse.save()
        Horse.objects.create(date_of_birth=datetime.datetime(2019, 5, 5), name='another horse', type='Flat',
                             sex='Female')
        mes1 = Measure.objects.create(horse=self.horse,
                                      date_of_measure=datetime.date(2019, 7, 8),
                                      biomechanics_video_probability="0.0046057390",
                                      biomechanics_gaf_probability="0.2488117400",
                                      biomechanics_keypoint_probability="0.1758952600",
                                      biomechanics_cluster=5,
                                      dlc_jrg_probability="0.192919510"
                                      )
        mes2 = Measure.objects.create(horse=self.horse,
                                      date_of_measure=datetime.date(2019, 7, 8),
                                      cardio_video_probability="0.5918922400",
                                      cardio_cluster=8,
                                      cardio_type="Euro Bullseye Turf Sprinter"
                                      )
        update_field = 'prob_bio_model'
        result = '0.7372244000'
        search_fields = prediction_data['instance']

        input_data = {
            'update_fields': {update_field: result},
            'search_fields': search_fields,
        }
        url = '/velox/api/measures/update_ml_tabular/'
        response = self.client.post(url, data=input_data, format='json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        updated_measures_resp = response_data['updated_measures']
        updated_measures = []
        measures = Measure.objects.all()
        for measure in measures:
            val = getattr(measure, update_field)
            if val == Decimal(result):
                updated_measures.append(measure)

        self.assertEqual(len(updated_measures), 1)
        self.assertListEqual(updated_measures_resp, [m.id for m in updated_measures])


class TestScoreBins(TestCase):

    def setUp(self) -> None:
        probabilities = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        horse = Horse.objects.create(name='test_horse', type='Flat', sex='Male', race_rating=10,
                                     date_of_birth=datetime.date(2018, 3, 23),
                                     )
        probability_fields = Measure.score_prob_fields

        for prob in probabilities:
            measure_data = {
                'horse': horse,
                'date_of_measure': datetime.date(2020, 1, 1)
            }
            for _, prob_field in probability_fields:
                measure_data[prob_field] = prob
            Measure.objects.create(**measure_data)

        self.probability_fields = probability_fields

    def test_score_bins(self):

        # check calculation of scores
        for _, prob_field in self.probability_fields:
            score_bin = ScoreBins.create_bins(Measure, prob_field)
            self.assertEqual(score_bin.prob_field_name, prob_field)
            self.assertIsNotNone(score_bin.bins)

            # scores based on input probabilities
            self.assertEqual(score_bin.get_score(Decimal('0.8')), 'A+')
            self.assertEqual(score_bin.get_score(Decimal('0.05')), 'D')
            self.assertEqual(score_bin.get_score(Decimal('0.25')), 'B')

    def test_new_measure_scoring(self):

        for _, prob_field in self.probability_fields:
            ScoreBins.create_bins(Measure, prob_field)

        horse = Horse.objects.create(name='another_test_horse', type='Flat', sex='Male', race_rating=10,
                                     date_of_birth=datetime.date(2018, 3, 23),
                                     )

        prop_field_value = Decimal('0.8')

        for score_field, prob_field in self.probability_fields:
            measure_data = {
                'horse': horse,
                'date_of_measure': datetime.date(2020, 1, 1),
                prob_field: prop_field_value
            }
            measure = Measure.objects.create(**measure_data)
            for sf, pf in self.probability_fields:
                score_val = getattr(measure, sf)
                print(score_field, sf, score_val)
                if score_field == sf:  # for set probability field score field should be set
                    self.assertEqual(score_val, 'A+')
                else:  # other fields should not be set
                    self.assertIsNone(score_val)


class MorphImageMLUpdate(TestCase):

    def setUp(self) -> None:
        horse, measure, image_data, gcs_uri, user = setup_test_data()
        im = ImageMeasurement.objects.create(image=GCSBlob(**image_data), horse=horse,
                                             morph_data={'just': 'data'},
                                             date_of_measure=datetime.date(2022, 1, 1))
        self.image_measurement = im
        self.gcs_uri = gcs_uri
        self.image_data = image_data
        self.client.force_login(user)

    def test_update(self):
        image_prob = Decimal('0.83241432')
        input_data = {
            'prob_image': image_prob,
            'image': self.gcs_uri
        }
        url = '/velox/api/image-measurements/update_ml_gcs_data/'
        response = self.client.post(url, data=input_data, format='json')
        self.assertEqual(response.status_code, 200)
        im = ImageMeasurement.objects.get(pk=self.image_measurement.pk)
        self.assertEqual(im.prob_image, image_prob)


class ImageMeasurementTabularMLUpdate(APITestCase):

    def setUp(self) -> None:
        horse, measure, image_data, gcs_uri, user = setup_test_data()
        calculated_data = {"bones": [{"pointA": 1, "pointB": 2, "boneName": "Neck", "distance": "176.76"},
                                     {"pointA": 2, "pointB": 4, "boneName": "Shoulder", "distance": "132.99"},
                                     {"pointA": 4, "pointB": 5, "boneName": "Humerus", "distance": "63.90"},
                                     {"pointA": 5, "pointB": 6, "boneName": "Forelimb", "distance": "91.23"},
                                     {"pointA": 7, "pointB": 8, "boneName": "Cannon", "distance": "58.32"},
                                     {"pointA": 8, "pointB": 9, "boneName": "Front Pastern", "distance": "32.37"},
                                     {"pointA": 10, "pointB": 2, "boneName": "Backlength", "distance": "172.04"},
                                     {"pointA": 12, "pointB": 3, "boneName": "Bodylength", "distance": "333.22"},
                                     {"pointA": "", "pointB": "", "boneName": "Scope", "distance": "1.87"},
                                     {"pointA": "", "pointB": "", "boneName": "Proportion", "distance": "0.13"},
                                     {"pointA": 10, "pointB": 21, "boneName": "Pelvis", "distance": "91.61"},
                                     {"pointA": 21, "pointB": 22, "boneName": "Femur", "distance": "103.98"},
                                     {"pointA": 22, "pointB": 23, "boneName": "Tibia", "distance": "94.60"},
                                     {"pointA": 23, "pointB": 24, "boneName": "HindCannon", "distance": "108.19"},
                                     {"pointA": 24, "pointB": 25, "boneName": "Fetlock", "distance": "39.50"},
                                     {"pointA": 10, "pointB": 22, "boneName": "Pelvis-Femur", "distance": "84.23"},
                                     {"pointA": 21, "pointB": 23, "boneName": "Ischium-Hock", "distance": "43.65"}],
                           "morph": {"box": {"top": "1", "left": "1", "width": "498", "height": "398"},
                                     "parts": {"0": {"x": 48, "y": 59}, "1": {"x": 192, "y": 101},
                                               "2": {"x": 157, "y": 139}, "3": {"x": 121, "y": 180},
                                               "4": {"x": 152, "y": 217}, "5": {"x": 155, "y": 289},
                                               "6": {"x": 156, "y": 317}, "7": {"x": 156, "y": 361},
                                               "8": {"x": 140, "y": 386}, "9": {"x": 322, "y": 116},
                                               "10": {"x": 388, "y": 103}, "11": {"x": 416, "y": 135},
                                               "12": {"x": 406, "y": 218}, "13": {"x": 361, "y": 213},
                                               "14": {"x": 431, "y": 268}, "15": {"x": 410, "y": 291},
                                               "16": {"x": 444, "y": 357}, "17": {"x": 427, "y": 357},
                                               "18": {"x": 438, "y": 391}, "19": {"x": 422, "y": 383}}},
                           "angels": [{"angle": "53", "angleName": "Shoulder Horizontal"},
                                      {"angle": "104", "angleName": "Shoulder Angle"},
                                      {"angle": "139", "angleName": "Forearm Angle"},
                                      {"angle": "152", "angleName": "Fetlock Angle"},
                                      {"angle": "13", "angleName": "Pelvis Horizontal"},
                                      {"angle": "100", "angleName": "Hip Angle"},
                                      {"angle": "146", "angleName": "Femur Angle"},
                                      {"angle": "157", "angleName": "Hock Angle"},
                                      {"angle": "160", "angleName": "Hind Fetlock Angle"}],
                           "factors": [{"value": "SHORT PELVIS", "factorName": "Triangle"},
                                       {"value": "7.68", "factorName": "Imblance"},
                                       {"value": "38.35", "factorName": "Thrust"}],
                           "edited_landmarks": [{"x": 50, "y": 56, "id": 1}, {"x": 184, "y": 95, "id": 2},
                                                {"x": 155, "y": 133, "id": 3}, {"x": 121, "y": 179, "id": 4},
                                                {"x": 153, "y": 218, "id": 5}, {"x": 151, "y": 290, "id": 6},
                                                {"x": 151, "y": 319, "id": 7}, {"x": 149, "y": 365, "id": 8},
                                                {"x": 136, "y": 387, "id": 9}, {"x": 319, "y": 110, "id": 10},
                                                {"x": 390, "y": 95, "id": 11}, {"x": 418, "y": 126, "id": 12},
                                                {"x": 407, "y": 209, "id": 13}, {"x": 364, "y": 207, "id": 14},
                                                {"x": 433, "y": 262, "id": 15}, {"x": 415, "y": 282, "id": 16},
                                                {"x": 446, "y": 356, "id": 17}, {"x": 427, "y": 357, "id": 18},
                                                {"x": 438, "y": 391, "id": 19}, {"x": 422, "y": 383, "id": 20}],
                           "procrustesDistance": "789.54"}
        im = ImageMeasurement.objects.create(image=GCSBlob(**image_data), horse=horse,
                                             calculated_data=calculated_data,
                                             date_of_measure=datetime.date(2022, 1, 1))
        self.image_measurement = im
        self.gcs_uri = gcs_uri
        self.image_data = image_data
        self.client.force_login(user)

    def test_update(self):
        prob = Decimal('0.83241432')
        conform_values = self.image_measurement.get_conformation_field_values()
        input_data = {
            'update_fields': {'prob_conform_model': prob},
            'search_fields': conform_values
        }
        url = '/velox/api/image-measurements/update_ml_tabular/'
        response = self.client.post(url, data=input_data, format='json')
        self.assertEqual(response.status_code, 200)
        im = ImageMeasurement.objects.get(pk=self.image_measurement.pk)
        self.assertEqual(im.prob_conform_model, prob)

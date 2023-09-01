import datetime
import decimal
import os
import time
import base64
import logging
from decimal import Decimal

import gcsfs
import requests
from redo import retriable
from google.cloud import aiplatform as aip
from google.cloud import aiplatform_v1
from typing import Dict, Optional, Sequence, Tuple
from google.cloud.aiplatform.gapic.schema import predict

from django.conf import settings

from .models import ImageMeasurement
from .vertex_ai import get_ml_model

GCP_PROJECT = settings.GCP_PROJECT
REGION = 'us-central1'

aip.init(project=settings.GCP_PROJECT, location=REGION)

api_endpoint = "us-central1-aiplatform.googleapis.com"
client_options = {"api_endpoint": api_endpoint}


@retriable()
def create_endpoint(project: str, display_name: str, location: str):
    """Creates Vertex Endpoint
    :param project - GCP project name
    :param display_name - a name of the Endpoint to be created
    :param location - a location/region where Endpoint will be created
    """
    logging.info(f'creating an endpoint {display_name}')
    endpoint = aip.Endpoint.create(display_name=display_name, project=project, location=location)
    logging.info(f'deploying endpoint completed {display_name}')
    return endpoint


@retriable()
def deploy_model(
        model_name: str,
        endpoint: aip.Endpoint,
        deployed_model_display_name: Optional[str] = None,
        traffic_percentage: Optional[int] = 0,
        traffic_split: Optional[Dict[str, int]] = None,
        min_replica_count: int = 1,
        max_replica_count: int = 1,
        metadata: Optional[Sequence[Tuple[str, str]]] = (),
        sync: bool = True,
):
    """Deploys Vertex Model to an existing Vertex Endpoint. code taken from GCP documentation.
    :param model_name - A fully-qualified model resource name or model ID. Example: "projects/123/locations/us-central1/models/456"
    :param endpoint - Endpoint object to which model will be deployed
    """
    logging.info(f'deploying model {model_name}')
    model = aip.Model(model_name=model_name)

    model.deploy(
        endpoint=endpoint,
        deployed_model_display_name=deployed_model_display_name,
        traffic_percentage=traffic_percentage,
        traffic_split=traffic_split,
        min_replica_count=min_replica_count,
        max_replica_count=max_replica_count,
        metadata=metadata,
        sync=sync,
        deploy_request_timeout=7200
    )

    logging.info(f'deploying model completed {model_name}')
    return model


@retriable()
def undeploy_model(
        model_id: str,
        end_point: str,
        project: str,
        location: str = "us-central1"
):
    """
    Undeploys a Model from an existing Endpoint
    :param model_id - Model id (just ID like 1234567, not full resource name)
    :param end_point - Endpoint name/id not full resource name
    :param project - GCP project name
    :param location - a location/region where Endpoint lives
    """
    model_name = f'projects/{project}/locations/{location}/models/{model_id}'
    logging.info(f'starting undeploying model {model_name}')
    client_model = aiplatform_v1.services.model_service.ModelServiceClient(client_options=client_options)

    # Get deployed_model_id
    model_request = aiplatform_v1.types.GetModelRequest(name=model_name)
    model_info = client_model.get_model(request=model_request)
    deployed_model_id = None
    for deployed_model in model_info.deployed_models:
        deployed_model_endpoint = deployed_model.endpoint
        if end_point in deployed_model_endpoint:
            deployed_model_id = deployed_model.deployed_model_id
            break

    name = f'projects/{project}/locations/{location}/endpoints/{end_point}'

    undeploy_request = aiplatform_v1.UndeployModelRequest(endpoint=name, deployed_model_id=deployed_model_id)

    client = aip.gapic.EndpointServiceClient(client_options=client_options)
    try:
        client.undeploy_model(request=undeploy_request)
    except Exception as e:
        logging.error(f'caught exception {e}')
    logging.info(f'undeploying model completed {model_name}')


@retriable()
def predict_image_classification_sample(image_gcs_uri: str, project: str, endpoint_id: str, image_measurement_id: int,
                                        location: str = "us-central1"):
    """Reads image file from GCS and does online prediction (via Vertex Endpoint) and updates Measure on the backend
    :param image_gcs_uri - full GCS file uri, in format gs://bucketname/filename
    :param file_field_name - name of the field from Measure based on which Measure should be searched for when updating.
            Usually from that field it's input for prediction
    :param prediction_field_name - name of the field from Measure to which resulting probability will be set
    :param project - GCP project name
    :param endpoint_id - Vertex Endpoint ID/name (not full resource name)
    :param image_measurement_id
    :param location - a location/region where Endpoint lives
    """

    logging.info(f'prediction started for {image_gcs_uri}')

    gcs = gcsfs.GCSFileSystem(project=GCP_PROJECT)
    with gcs.open(image_gcs_uri, "rb") as f:
        file_content = f.read()
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageClassificationPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    parameters = predict.params.ImageClassificationPredictionParams(
        confidence_threshold=0.5, max_predictions=5,
    ).to_value()
    client = aip.gapic.PredictionServiceClient(client_options=client_options)
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    predictions = response.predictions
    for prediction in predictions:
        data = dict(prediction)
        logging.info(f'results for online prediction: {data}')
        display_name = data['displayNames'][0]
        confidence = data['confidences'][0]
        if display_name == 'No':
            confidence = Decimal("1") - Decimal(str(confidence))
            places_rounding = Decimal(10) ** (-10)
            confidence = confidence.quantize(places_rounding, decimal.ROUND_DOWN)

        image_measurement = ImageMeasurement.objects.get(pk=image_measurement_id)
        image_measurement.prob_image = confidence
        image_measurement.save()
        time.sleep(0.5)
    logging.info(f'prediction completed for {image_gcs_uri}')


@retriable()
def delete_endpoint(
        endpoint_id: str,
        project: str,
        location: str = "us-central1",
        timeout: int = 7200,
):
    """Deletes existing Vertex Endpoint
    :param endpoint_id - Endpoint id/name (not full resource name)
    :param project - GCP project name
    :param location - location/region where Endpoint is created
    :param timeout - timeout for a request/operation
    """
    logging.info(f'deleting endpoint {endpoint_id}')
    client = aip.gapic.EndpointServiceClient(client_options=client_options)
    name = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.delete_endpoint(name=name)

    delete_endpoint_response = response.result(timeout=timeout)
    logging.info(f'delete endpoint response {delete_endpoint_response}')
    logging.info(f'endpoint deleted {endpoint_id}')


def online_morph_image_prediction(model_name, image_gcs_uri, image_measurement_id):
    """Makes online prediction for an image file stored on GCS and updates Measure with result

    :param model_name - Vertex Model name - display name, not ID or full resource name
    :param image_gcs_uri - full GCS file uri, in format gs://bucketname/filename
    :param file_field_name - name of the field from Measure based on which Measure should be searched for when updating.
        Usually from that field, it was input for prediction
    :param probability_field_name - name of the field from Measure to which resulting probability will be set
    :param image_measurement_id
    """
    logging.info(f'starting online image prediction for {image_gcs_uri}')
    model = get_ml_model(model_name)
    model_id = model['name']
    endpoint_display_name = f'{model_name}_prediction_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
    endpoint = create_endpoint(GCP_PROJECT, endpoint_display_name, REGION)
    deploy_model(model_id, endpoint)
    predict_image_classification_sample(image_gcs_uri, GCP_PROJECT, endpoint.name, image_measurement_id)
    undeploy_model(model_id, endpoint.name, GCP_PROJECT)
    delete_endpoint(endpoint.name, GCP_PROJECT)
    logging.info(f'online image prediction for {image_gcs_uri} completed')


def deploy_endpoint(model_name):
    """for local development/testing purposes"""
    model = get_ml_model(model_name)
    model_id = model['name']
    endpoint_display_name = f'{model_name}_prediction_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
    endpoint = create_endpoint(GCP_PROJECT, endpoint_display_name, REGION)
    deploy_model(model_id, endpoint)
    time.sleep(10)
    undeploy_model(model_id, endpoint.name, GCP_PROJECT)
    delete_endpoint(endpoint.name, GCP_PROJECT)

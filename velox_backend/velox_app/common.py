import os
import json
import time
import logging
import datetime

import requests

from google.cloud import storage
from django.conf import settings

gcs = storage.Client(project=settings.GCP_PROJECT).from_service_account_json(settings.GCP_SERVICE_ACCOUNT_FILE)


def score_tabular_prediction(service_url: str, input_data: dict) -> str:
    """Making request to a service that serves tabular model
    :param service_url - full url for the service
    :param input_data - dictionary of input data, corresponding to the prediction service
    """
    data = {'instances': [input_data]}
    logging.info(f'sending prediction data {data}')
    while True:
        r = requests.post(service_url, json=data)
        response_data = r.json()
        if r.status_code == 200:
            predictions = response_data.get('predictions', [])
            probability = None
            if len(predictions):
                result = predictions[0]
                classes = result['classes']
                scores = result['scores']
                index = classes.index('Yes')
                probability = scores[index]
                probability = str(probability)[0:11]
                return probability
            else:
                logging.error('no predictions')
                break
        elif r.status_code == 400:
            error = response_data.get('error', '')
            if error == "failed to connect to all addresses":
                time.sleep(1)
            else:
                break
        else:
            logging.error(f'error from prediction service {service_url} {r.status_code} {r.text}')
            break


def score_tabular_classification_prediction(service_url: str, input_data: dict) -> str:
    """Making request to a service that serves tabular classification model
    :param service_url - full url for the service
    :param input_data - dictionary of input data, corresponding to the prediction service
    """
    data = {'instances': [input_data]}
    logging.info(f'sending prediction data {data}')
    while True:
        r = requests.post(service_url, json=data)
        response_data = r.json()
        logging.info(f'prediction input data {data} response {r.text}')
        if r.status_code == 200:
            predictions = response_data.get('predictions', [])
            if len(predictions):
                result = predictions[0]
                classes = result['classes']
                scores = result['scores']
                max_val = max(scores)
                max_index = scores.index(max_val)
                res = classes[max_index]
                return res
            else:
                logging.error('no predictions')
                break
        elif r.status_code == 400:
            error = response_data.get('error', '')
            if error == "failed to connect to all addresses":
                time.sleep(1)
            else:
                break
        else:
            logging.error(f'error from prediction service {service_url} {r.status_code} {r.text}')
            break


def create_task(url: str, tasks_queue_name, data: dict):
    """Creates a Cloud Task
    :param url - absolute url to where task will be processed
    :param tasks_queue_name - name of the Task Queue
    :param data - dictionary with input data (json serializable) for the Task
    """
    from google.cloud import tasks_v2
    tasks_client = tasks_v2.CloudTasksClient()
    tasks_region = 'us-central1'
    if 'https' not in url:
        url = url.replace('http', 'https')  # force https url
    task = {
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,  # The full url path that the task will be sent to.
        }
    }

    payload = json.dumps(data)
    task["http_request"]["headers"] = {"Content-type": "application/json"}
    converted_payload = payload.encode()
    task["http_request"]["body"] = converted_payload

    ts = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    task["name"] = tasks_client.task_path(settings.GCP_PROJECT, tasks_region, tasks_queue_name,
                                          f'{tasks_queue_name}-{ts}')
    tasks_queue = tasks_client.queue_path(settings.GCP_PROJECT, tasks_region, tasks_queue_name)
    response = tasks_client.create_task(request={"parent": tasks_queue, "task": task})

    return response

def send_email(email_body: str, email_subject, attachment_file_content: str):
    """Send an email with attachment"""

    import base64
    from mailjet_rest import Client

    mj_api_key = os.environ['MJ_API_KEY']
    mj_api_secret = os.environ['MJ_API_SECRET']
    sender_email = 'byron@performancegenetics.com'
    to_email = 'byronrogersracing@gmail.com'

    mailjet = Client(auth=(mj_api_key, mj_api_secret), version='v3.1')

    messages = [
            {
                "From": {
                    "Email": sender_email,
                },
                "To": [
                    {
                        "Email": to_email,
                    },
                    {
                        "Email": "zdenulo@gmail.com"
                    }

                ],
                "Subject": email_subject,
                'Htmlpart': email_body,
            }
        ]
    if attachment_file_content:
        attachment_encoded = base64.b64encode(attachment_file_content.encode()).decode()
        messages[0]['Attachments'] = [
            {
                "ContentType": "text/txt",
                "Filename": "attachment.txt",
                "Base64Content": attachment_encoded
            }
        ]

    data = {
        'Messages': messages
    }
    result = mailjet.send.create(data=data)
    logging.info(f'Mailjet {result.status_code}')
    logging.info(f'Mailjet {json.loads(result.content.decode())}')
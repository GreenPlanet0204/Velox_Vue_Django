import re
import logging

from google.protobuf import json_format
import google.cloud.aiplatform as aip
from google.cloud import aiplatform_v1
from google.cloud import firestore

from redo import retriable

from django.conf import settings

gcp_project = settings.GCP_PROJECT
location = 'us-central1'
API_ENDPOINT = f"{location}-aiplatform.googleapis.com"

aip.init(project=gcp_project, location=location)

db = firestore.Client(project=settings.GCP_PROJECT)


IGNORE_MODELS_FOR_SYNC = ['morph-landmarks', ]  # don't sync model with these display names

ml_models_collection_name = 'vertex-ai-models'


def get_model_metadata(model):
    model_dict = model.to_dict()
    model_metadata = model_dict['metadata']

    model_name = model_dict['displayName']
    regex_res = re.search("|".join(IGNORE_MODELS_FOR_SYNC), model_name)
    if regex_res:
        return
    # model_creation_date = model_dict['createTime']
    # model_type = model_metadata.get('modelType', '')
    # number_training = model_metadata.get('trainingDataItemsCount', '')

    client_options = {
        "api_endpoint": API_ENDPOINT
    }
    model_path = model.resource_name
    client_model = aiplatform_v1.services.model_service.ModelServiceClient(client_options=client_options)
    list_eval_request = aiplatform_v1.types.ListModelEvaluationsRequest(parent=model_path)
    list_eval = client_model.list_model_evaluations(request=list_eval_request)

    eval_name = ''
    for val in list_eval:
        eval_name = val.name
    get_eval_request = aiplatform_v1.types.GetModelEvaluationRequest(name=eval_name)
    model_eval = client_model.get_model_evaluation(request=get_eval_request)
    model_eval_data = json_format.MessageToDict(model_eval._pb)
    eval_data = extract_evaluation_data(model_eval_data)
    eval_data['creation_time'] = model.create_time.isoformat()
    eval_data['update_time'] = model.update_time.isoformat()
    eval_data['model_id'] = model.name
    eval_data['name'] = model.display_name
    eval_data['resource_name'] = model.resource_name
    return eval_data


def extract_evaluation_data(data: dict):
    metrics = data['metrics']
    confusion_matrix = metrics.get('confusionMatrix', {})
    model_explanation = data.get('modelExplanation', {})
    mean_attributions = model_explanation.get('meanAttributions', [])
    feature_attributions_per = {}
    if mean_attributions:
        feature_attributions = mean_attributions[0]['featureAttributions']
        # feature attributions
        total = 0.0
        for k, v in feature_attributions.items():
            total += v
        for k, v in feature_attributions.items():
            feature_attributions_per[k] = round((v / total) * 100, 2)
    # confusion matrix
    confusion_matrix_per = []
    annotations = []
    if confusion_matrix:
        for row in confusion_matrix['rows']:
            row_total = sum(row)
            row_per = []
            for item in row:
                item_per = int(round((item * 1.0 / row_total) * 100, 0))
                row_per.append(item_per)
            confusion_matrix_per.append(row_per)

        for annotation_spec in confusion_matrix['annotationSpecs']:
            annotation_name = annotation_spec['displayName']
            annotations.append(annotation_name)

    log_loss = metrics.get('logLoss', -1)
    au_prc = metrics.get('auPrc', -1)
    au_roc = metrics.get('auRoc', -1)
    out = {
        'confusion_matrix': confusion_matrix_per,
        'annotations': annotations,
        'feature_attributions': feature_attributions_per,
        'log_loss': log_loss,
        'au_prc': au_prc,
        'au_roc': au_roc
    }
    return out


def get_all_ml_models_metadata(models_no: int) -> list:
    """gets metadata for all Vertex Models
    :param models_no - number of models to sync, i.e. we don't sync all models since it's time consuming
    """

    out_data = []
    models = aip.Model.list(order_by='update_time desc')
    c = 0
    for model in models:
        data = get_model_metadata(model)
        if data:
            out_data.append(data)
        c += 1
        if c >= models_no:
            break
    return out_data


@retriable(sleeptime=30)
def get_ml_model(model_name: str) -> dict:
    logging.info(f'getting model data for {model_name}')
    doc = db.collection(ml_models_collection_name).document(model_name).get()
    doc_data = doc.to_dict()
    if not doc_data:
        raise Exception(f"Couldn't find vertex model: {model_name}")
    logging.info(f'found model data {doc_data}')
    return doc_data


def sync_ml_models_firestore():
    models = aip.Model.list()
    models_ordered = sorted(models, key=lambda m: m.update_time)
    for m in models_ordered:
        display_name = m.display_name
        name = m.name
        update_time = m.update_time
        data = {
            'name': name,
            'updated_time': update_time
        }
        db.collection(ml_models_collection_name).document(display_name).set(data)

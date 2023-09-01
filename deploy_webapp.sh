#!/bin/bash


gcloud builds submit --config=deploy.yaml --substitutions=_SERVICE_NAME="velox" --project velox-horse1

gsutil -m cp -r velox_backend/velox_app/static/velox/ gs://velox_webapp_static/

#!/bin/bash

rm dist/*
npm run build

cp dist/* ../velox_backend/velox_app/static/velox/js/

#gsutil -m cp -r dist/* gs://cmmc_static_test/cmmc/js/
#gsutil iam -r ch allUsers:objectViewer gs://cmmc_static_test/cmmc/js
echo "done"
exit 0

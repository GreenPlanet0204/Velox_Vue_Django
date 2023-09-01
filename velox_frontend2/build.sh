#!/bin/bash

set -e

rm -r dist/

npm run build-local

cp ./dist/index.html ../velox_backend/velox/templates/vue_index.html

rm -r ../velox_backend/velox_app/static/velox/
mkdir -p ../velox_backend/velox_app/static/velox/

cp -r ./dist/static/velox/* ../velox_backend/velox_app/static/velox/

rm -r ../velox_backend/velox_app/static/model/
mkdir -p ../velox_backend/velox_app/static/model/

cp -r ./dist/model/* ../velox_backend/velox_app/static/model/

echo "done"
exit 0

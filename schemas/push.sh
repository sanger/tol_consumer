#!/bin/bash
if [ $# -ne 2 ]; then
  echo "Syntax:"
  echo "  push.sh <SCHEMAS_FOLDER> <REDPANDA_URL>"
  echo "where:"
  echo "  <SCHEMAS_FOLDER>: folder that contains the schemas (schemas filename must end with -schema.txt)"
  echo "  <REDPANDA_URL>: Url to connect to Redpanda where the schemas will be uploaded"
  exit 1
fi
LOCAL_PATH=$1
URL=$2

CONTENT_TYPE="Content-Type: application/vnd.schemaregistry.v1+json"

pushd $LOCAL_PATH 1>/dev/null

for schema in `find . -name "*-schema.txt"`; do
  curl -X POST -d @$schema -H "$CONTENT_TYPE" $URL/subjects/create-labware/versions
done

popd 1>/dev/null
#!/bin/bash
if [ $# -ne 2 ]; then
  echo "Syntax:"
  echo "  push.sh <SCHEMAS_FOLDER> <REDPANDA_URL>"
  echo "where:"
  echo "  <SCHEMAS_FOLDER>: folder that contains the subfolders with the schemas (schemas filename must end with -schema.txt)"
  echo "  <REDPANDA_URL>: URL to connect to RedPanda where the schemas will be uploaded"
  exit 1
fi
SCHEMAS_FOLDER=$1
REDPANDA_URL=$2

CONTENT_TYPE="Content-Type: application/vnd.schemaregistry.v1+json"

pushd $SCHEMAS_FOLDER 1>/dev/null

for schema in `find $SCHEMAS_FOLDER -name "*-schema.txt"`; do
  echo "Uploading schema $schema"
  schema_name=`dirname $schema | sed 's/\.//g' | sed 's/\///g'`
  curl -X POST -d @$schema -H "$CONTENT_TYPE" "$REDPANDA_URL/subjects/$schema_name/versions"
  #curl -X GET -H "$CONTENT_TYPE" "$REDPANDA_URL/subjects/$schema_name/versions/1"
done

popd 1>/dev/null

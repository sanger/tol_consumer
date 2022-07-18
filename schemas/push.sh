#!/bin/bash
if [ $# -ne 1 ]; then
  echo "Syntax:"
  echo "  push.sh <REDPANDA_URL>"
  echo "where:"
  echo "  <REDPANDA_URL>: Url to connect to Redpanda where the schemas will be uploaded"
  exit 1
fi
REDPANDA_URL=$1

CONTENT_TYPE="Content-Type: application/vnd.schemaregistry.v1+json"

pushd "$(dirname "$0")"

for schema in `find . -name "*-schema.txt"`; do
  echo "Uploading schema $schema"
  schema_name=`dirname $schema | sed 's/\.//g' | sed 's/\///g'`
  curl -X POST -d @$schema -H "$CONTENT_TYPE" "$REDPANDA_URL/subjects/$schema_name/versions"
done

popd 1>/dev/null

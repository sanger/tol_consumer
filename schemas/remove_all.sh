#!/bin/bash
if [ $# -ne 2 ]; then
  echo "Syntax:"
  echo "  remove_all.sh <REDPANDA_URL> <API_KEY>"
  echo "where:"
  echo "  <REDPANDA_URL>: URL to connect to RedPanda where the schemas will be removed"
  echo "  <API_KEY>: secret key with write permission for redpanda"
  exit 1
fi
REDPANDA_URL=$1
API_KEY=$2
 
CONTENT_TYPE="Content-Type: application/vnd.schemaregistry.v1+json"
API_KEY_HEADER="X-API-KEY: $API_KEY"

pushd "$(dirname "$0")"

for schema in `find . -name "*-schema.txt"`; do
  schema_name=`dirname $schema | sed 's/\.//g' | sed 's/\///g'`
  echo "Deleting all schemas from $schema_name"
  curl -X DELETE -H "$CONTENT_TYPE" -H "$API_KEY_HEADER" "$REDPANDA_URL/subjects/$schema_name/versions/latest"
  echo 
done

popd 1>/dev/null

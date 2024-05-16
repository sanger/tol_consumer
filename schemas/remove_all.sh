#!/bin/bash
if [ $# -ne 1 ]; then
  echo "Syntax:"
  echo "  remove_all.sh <REDPANDA_URL>"
  echo "where:"
  echo "  <REDPANDA_URL>: URL to connect to RedPanda where the schemas will be removed"
  exit 1
fi
REDPANDA_URL=$1

CONTENT_TYPE="Content-Type: application/vnd.schemaregistry.v1+json"

pushd "$(dirname "$0")"

for schema in `find . -name "*.avsc"`; do
  schema_name=`dirname $schema | sed 's/\.//g' | sed 's/\///g'`
  echo "Deleting all schemas from $schema_name"
  curl -X DELETE -H "$CONTENT_TYPE" "$REDPANDA_URL/subjects/$schema_name/versions/latest"
  echo
done

popd 1>/dev/null

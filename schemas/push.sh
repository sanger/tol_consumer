#!/bin/bash
if [ $# -ne 1 ]; then
  echo "Syntax:"
  echo "  push.sh <REDPANDA_URL>"
  echo "where:"
  echo "  <REDPANDA_URL>: URL to connect to RedPanda where the schemas will be uploaded"
  echo ""
  echo "Note that the RedPanda APIs on OpenStack do not allow POST methods, so this script will"
  echo "not work unless that restriction is temporarily removed in the nginx config."
  echo "A better option is to use the RedPanda Web Console instead."
  echo "Note: jq command line utility is a prerequisite for this. Make sure you have it installed."
  echo "If not, use brew install jq to install it"
  exit 1
fi
REDPANDA_URL=$1

CONTENT_TYPE="Content-Type: application/vnd.schemaregistry.v1+json"

pushd "$(dirname "$0")"

for schema in `find . -name "*.avsc"`; do
  schema_name=`dirname $schema | sed 's/\.//g' | sed 's/\///g'`

  # Convert to schema
  echo "{\"schema\":" > $schema.tmp
  jq -c 'tojson' $schema >> $schema.tmp
  echo "}" >> $schema.tmp

  echo "Uploading schema $schema_name"
  curl -X POST -d @$schema.tmp -H "$CONTENT_TYPE" "$REDPANDA_URL/subjects/$schema_name/versions"

  # Remove temp file
  rm $schema.tmp
  echo
done

popd 1>/dev/null

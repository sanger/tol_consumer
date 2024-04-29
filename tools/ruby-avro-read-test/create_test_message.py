#!/bin/env python

import json
import fastavro
from expected_message import EXPECTED_MESSAGE

def read_file(file, mode):
  with open(file, mode) as f:
    return f.read()

class BinaryAvroWriter:
  def __init__(self, schema):
    self._schema_str = schema

  @property
  def _schema(self):
    schema_obj = json.loads(self._schema_str)
    return fastavro.parse_schema(schema_obj)

  def write(self, data_obj):
    with open('schemaless_message.avro', 'wb') as f:
      fastavro.schemaless_writer(f, self._schema, data_obj)


if __name__ == '__main__':
  schema = read_file('schema.avsc', 'r')
  writer = BinaryAvroWriter(schema)
  writer.write(EXPECTED_MESSAGE)

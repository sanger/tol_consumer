#!/bin/env python

from expected_message import EXPECTED_MESSAGE
from io import BytesIO
import json
import fastavro

def read_file(file, mode):
  with open(file, mode) as f:
    return f.read()

class BinaryAvroReader:
  def __init__(self, schema):
    self._schema_str = schema

  @property
  def _schema(self):
    schema_obj = json.loads(self._schema_str)
    return fastavro.parse_schema(schema_obj)

  def parse(self, message):
    bytes_reader = BytesIO(message)
    return fastavro.schemaless_reader(bytes_reader, self._schema)


if __name__ == '__main__':
  schema = read_file('schema.avsc', 'r')
  reader = BinaryAvroReader(schema)

  message_in = read_file('ruby_message.avro', 'rb')
  decoded = reader.parse(message_in)

  if EXPECTED_MESSAGE == decoded:
    print('Decoded message contents matches the expected contents.')
  else:
    print('Message was not identical.\n')
    print(f'Expected: {EXPECTED_MESSAGE}\n')
    print(f'Decoded: {decoded}')

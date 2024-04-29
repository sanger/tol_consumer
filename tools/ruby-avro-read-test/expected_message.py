from datetime import datetime, timezone

EXPECTED_MESSAGE = {
  'messageUuid': b'f1b3b3b4-4b3b-4b3b-4b3b-4b3b3b3b3b3b',
  'messageCreateDateUtc': datetime(2021, 1, 14, 8, 0, tzinfo=timezone.utc),
  'tubeBarcode': 'TRAC-123456',
  'library': {
    'volume': 1.0,
    'concentration': 1.0,
    'boxBarcode': 'TRAC-123456',
    'insertSize': 300
  },
  'request': {
    'costCode': 'TRAC-123456',
    'genomeSize': '3.0',
    'libraryType': 'DNA',
    'studyUuid': b'f1b3b3b4-4b3b-4b3b-4b3b-4b3b3b3b3b3b'
  },
  'sample': {
    'sampleName': 'TRAC-123456',
    'sampleUuid': b'f1b3b3b4-4b3b-4b3b-4b3b-4b3b3b3b3b3b',
    'speciesName': 'human'
  }
}

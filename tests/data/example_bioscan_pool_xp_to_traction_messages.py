from datetime import datetime, UTC
from typing import Any

TEST_VALID_BIOSCAN_POOL_XP_TO_TRACTION_MSG_OBJECT: dict[str, Any] = {
    "messageUuid": "01234567-89ab-cdef-0123-456789abcdef".encode(),
    "messageCreateDateUtc": datetime.now(UTC),
    "tubeBarcode": "TUBE001",
    "library": {
        "volume": 23.4,
        "concentration": 45.6,
        "boxBarcode": "BOX001",
        "insertSize": 100,
    },
    "request": {
        "costCode": "S1234",
        "genomeSize": "123456 bp",
        "libraryType": "Pacbio_HiFi",
        "studyUuid": "456789ab-cdef-0123-4567-89abcdef0123".encode(),
    },
    "sample": {
        "sampleName": "SampleName",
        "sampleUuid": "89abcdef-0123-4567-89ab-cdef01234567".encode(),
        "speciesName": "Mus Musculus",
    },
}

TEST_INVALID_BIOSCAN_POOL_XP_TO_TRACTION_MSG_OBJECT: dict[str, Any] = {
    "messageUuid": "0123456789ab-cdef-0123-456789abcdef".encode(),
    "messageCreateDateUtc": datetime.now(UTC),
    "library": {
        "volume": "23.4",
        "boxBarcode": None,
        "insertSize": 100.0,
    },
    "request": {
        "costCode": 1234,
        "libraryType": None,
        "studyUuid": "456789ab-cdef-0123-4567890abcdef0123".encode(),
    },
    "sample": {
        "sampleUuid": "89abcdef-0123-4567-89ab-cdef01234567",
        "speciesName": None,
    },
}

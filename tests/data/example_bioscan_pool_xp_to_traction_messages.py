from datetime import datetime, UTC
from typing import Any

VALID_LIBRARY_PAYLOAD: dict[str, Any] = {
    "volume": 23.4,
    "concentration": 45.6,
    "boxBarcode": "BOX001",
    "insertSize": 100,
}

VALID_REQUEST_PAYLOAD: dict[str, Any] = {
    "costCode": "S1234",
    "genomeSize": "123456 bp",
    "libraryType": "Pacbio_HiFi",
    "studyUuid": "456789ab-cdef-0123-4567-89abcdef0123".encode(),
}

VALID_SAMPLE_PAYLOAD: dict[str, Any] = {
    "sampleName": "SampleName",
    "sampleUuid": "89abcdef-0123-4567-89ab-cdef01234567".encode(),
    "speciesName": "Mus Musculus",
}

VALID_BIOSCAN_POOL_XP_TO_TRACTION_PAYLOAD: dict[str, Any] = {
    "messageUuid": "01234567-89ab-cdef-0123-456789abcdef".encode(),
    "messageCreateDateUtc": datetime.now(UTC),
    "tubeBarcode": "TUBE001",
    "library": VALID_LIBRARY_PAYLOAD,
    "request": VALID_REQUEST_PAYLOAD,
    "sample": VALID_SAMPLE_PAYLOAD,
}

# The following message object has been annotated with what is wrong with it.
INVALID_BIOSCAN_POOL_XP_TO_TRACTION_PAYLOAD: dict[str, Any] = {
    "messageUuid": "0123456789ab-cdef-0123-456789abcdef".encode(),  # badly formatted UUID
    "messageCreateDateUtc": datetime.now(UTC),
    # tubeBarcode is not optional but missing
    "library": {
        # concentration is not optional but is missing
        "volume": "23.4",  # should be a float
        "boxBarcode": None,  # not optional
        "insertSize": 100.0,  # should be an integer
    },
    "request": {
        "costCode": 1234,  # should be a string
        # genome size is not optional but is missing
        "libraryType": None,  # not optional
        "studyUuid": "456789ab-cdef-0123-4567890abcdef0123".encode(),  # badly formatted UUID
    },
    "sample": {
        # sampleName is not optional but is missing
        "sampleUuid": "89abcdef-0123-4567-89ab-cdef01234567",  # badly formatted UUID
        "speciesName": None,  # not optional
    },
}

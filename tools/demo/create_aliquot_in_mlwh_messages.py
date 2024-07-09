from datetime import datetime, UTC
from uuid import uuid4


def build_create_aliquot_message():
    return {
        "messageUuid": str(uuid4()),
        "messageCreateDateUtc": datetime.now(UTC).timestamp() * 1000,
        "limsId": "LabWhere",
        "limsUuid": str(uuid4()),
        "aliquotType": "primary",
        "sourceType": "sample",
        "sourceBarcode": "SQPP-111111",
        "sampleName": "3457STDY6034749",
        "usedByType": "run",
        "usedByBarcode": "SQPP-111112",
        "volume": 1.0,
        "concentration": 2.0,
        "recordedAt": datetime.now(UTC).timestamp() * 1000,
    }

from datetime import datetime, UTC
from typing import Any

VALID_TRACTION_TO_WAREHOUSE_MESSAGE: "dict[str, Any]" = {
    "limsId": "Traction",
    "messageCreateDateUtc": datetime.now(UTC),
    "messageUuid": "4b6b9444-8935-4376-929d-06dae7b775f3".encode(),
    "recordedAt": datetime.now(UTC),
    "volume": 1.5,
    "concentration": 10.0,
    "insertSize": 100,
    "aliquotType": "primary",
    "limsUuid": "4b6b9444-8935-4376-129d-06dae7b775f3".encode(),
    "sourceType": "library",
    "sourceBarcode": "TRAC-2-1572",
    "sampleName": "DTOL8334991",
    "usedByBarcode": "SQPU-86258-I",
    "usedByType": "none",
}

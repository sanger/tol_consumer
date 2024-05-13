from datetime import datetime, UTC
from uuid import uuid4

# Pacbio_HiFi, Saphyr_v1, ONT_Ultralong
LIBRARY_TYPE = "Pacbio_HiFi"

def barcode_for_unique_id(labtype, unique_id, msg_idx):
    return f"BARCODE-{labtype}-{unique_id}-{msg_idx}"

def build_bioscan_pool_xp_msg(unique_id, msg_idx):
    return {
        "messageUuid": str(uuid4()).encode(),
        "messageCreateDateUtc": datetime.now(UTC).timestamp() * 1000,
        "tubeBarcode": barcode_for_unique_id("TUBE", unique_id, msg_idx),
        "library": {
            "volume": 23.4,
            "concentration": 45.6,
            "boxBarcode": barcode_for_unique_id("BOX", unique_id, msg_idx),
            "insertSize": 100,
        },
        "request": {
            "costCode": "S1234",
            "genomeSize": "123456 bp",
            "libraryType": LIBRARY_TYPE,
            "studyUuid": str(uuid4()).encode(),
        },
        "sample": {
            "sampleName": f"Sample-{unique_id}-{msg_idx}",
            "sampleUuid": str(uuid4()).encode(),
            "speciesName": "Mus Musculus",
        },
    }

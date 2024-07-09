from datetime import datetime, UTC, timezone
from uuid import uuid4


def build_create_aliquot_message():
    dt = datetime.now(UTC)
    date_string = dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    return {
        "lims": "traction",
        "aliquot": {
            "id_lims": "LIMS123456",
            "lims_uuid": str(uuid4()),
            "aliquot_type": "derived",
            "source_type": "primary",
            "source_barcode": "SRC123456",
            "sample_name": "SampleA",
            "used_by_type": "Research",
            "used_by_barcode": "USR123456",
            "volume": 50.50,
            "concentration": 200.10,
            "last_updated": date_string,
            "recorded_at": date_string,
            "created_at": date_string,
            "insert_size": 350
    }
}

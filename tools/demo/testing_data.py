from datetime import datetime
from uuid import uuid4


def barcode_for_unique_id(unique_id):
    return f"BARCODE{unique_id}"


def build_create_labware_96_msg(unique_id, labware_uuid):
    return {
        "messageUuid": str(uuid4()).encode(),
        "messageCreateDateUtc": datetime.now().timestamp() * 1000,
        "labware": {
            "labwareType": "Plate12x8",
            "barcode": barcode_for_unique_id(unique_id),
            "samples": [
                {
                    "sampleUuid": str(uuid4()).encode(),
                    "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
                    "sangerSampleId": f"sangerId-{unique_id}-{(letter-ord('A'))*pos}",
                    "location": f"{chr(letter) + ('0' if len(str(pos)) == 1 else '') + str(pos)}",
                    "supplierSampleName": f"SampleSupplied-{unique_id}-{(letter-ord('A'))*pos}",
                    "volume": "5",
                    "concentration": "5",
                    "publicName": f"SamplePublicName-{unique_id}-{(letter-ord('A'))*pos}",
                    "taxonId": "10090",
                    "commonName": "Mus Musculus",
                    "donorId": f"donor{(letter-ord('A'))*pos}",
                    "libraryType": "Library1",
                    "countryOfOrigin": "United Kingdom",
                    "sampleCollectionDateUtc": datetime.now().timestamp() * 1000,
                }
                for letter in range(ord("A"), ord("A") + 1)
                for pos in range(1, 2)
            ],
        },
    }


def build_update_labware_msg(sample_msg):
    return {
        "messageUuid": str(uuid4()).encode(),
        "messageCreateDateUtc": datetime.now().timestamp() * 1000,
        "sampleUpdates": [
            {
                "sampleUuid": sample_msg["labware"]["samples"][3]["sampleUuid"],
                "name": "sangerSampleId",
                "value": f"MODIFIEDSANGERSAMPLEID-{sample_msg['labware']['barcode']}-3",
            },
            {
                "sampleUuid": sample_msg["labware"]["samples"][14]["sampleUuid"],
                "name": "supplierSampleName",
                "value": f"MODIFIEDSUPLIED-{sample_msg['labware']['barcode']}-14",
            },
            {
                "sampleUuid": sample_msg["labware"]["samples"][95]["sampleUuid"],
                "name": "commonName",
                "value": f"MODIFIEDCOMMONNAME-{sample_msg['labware']['barcode']}-95",
            },
        ],
    }

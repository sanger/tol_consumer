from datetime import datetime
from uuid import uuid4

# Pacbio_HiFi, Saphyr_v1, ONT_Ultralong
LIBRARY_TYPE = "ONT_Ultralong"


def barcode_for_unique_id(labtype, unique_id, num_msg):
    return f"BARCODE-{labtype}-{unique_id}-{num_msg}"


def unique_pos(letter, pos):
    return f"{letter}-{pos}"


def build_create_labware_96_msg(unique_id, num_msg):
    unique_id_lab = f"TOLTESTING-PLATE-{unique_id}-{num_msg}"
    return {
        "messageUuid": str(uuid4()).encode(),
        "messageCreateDateUtc": datetime.now().timestamp() * 1000,
        "labware": {
            "labwareType": "Plate12x8",
            "barcode": barcode_for_unique_id("PLATE", unique_id, num_msg),
            "samples": [
                {
                    "sampleUuid": str(uuid4()).encode(),
                    "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
                    "sangerSampleId": f"sangerId-{unique_id_lab}-{unique_pos(letter, pos)}",
                    "location": f"{chr(letter) + ('0' if len(str(pos)) == 1 else '') + str(pos)}",
                    "supplierSampleName": f"SampleSupplied-{unique_id_lab}-{unique_pos(letter, pos)}",
                    "volume": "5",
                    "concentration": "5",
                    "publicName": f"SamplePublicName-{unique_id_lab}-{unique_pos(letter, pos)}",
                    "taxonId": "10090",
                    "commonName": "Mus Musculus",
                    "donorId": f"donor-{unique_id_lab}-{unique_pos(letter, pos)}",
                    "libraryType": LIBRARY_TYPE,
                    "countryOfOrigin": "United Kingdom",
                    "sampleCollectionDateUtc": datetime.now().timestamp() * 1000,
                }
                for letter in range(ord("A"), ord("H") + 1)
                for pos in range(1, 13)
            ],
        },
    }


def build_create_tube_msg(unique_id, num_msg):
    unique_id_lab = f"TOLTESTING-TUBE-{unique_id}-{num_msg}"
    return {
        "messageUuid": str(uuid4()).encode(),
        "messageCreateDateUtc": datetime.now().timestamp() * 1000,
        "labware": {
            "labwareType": "Tube",
            "barcode": barcode_for_unique_id("TUBE", unique_id, num_msg),
            "samples": [
                {
                    "sampleUuid": str(uuid4()).encode(),
                    "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
                    "sangerSampleId": f"sangerId-{unique_id_lab}",
                    "supplierSampleName": f"SampleSupplied-{unique_id_lab}",
                    "location": None,
                    "volume": "5",
                    "concentration": "5",
                    "publicName": f"SamplePublicName-{unique_id_lab}",
                    "taxonId": "10090",
                    "commonName": "Mus Musculus",
                    "donorId": f"donor-{unique_id_lab}",
                    "libraryType": LIBRARY_TYPE,
                    "countryOfOrigin": "United Kingdom",
                    "sampleCollectionDateUtc": datetime.now().timestamp() * 1000,
                }
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

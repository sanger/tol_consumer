from datetime import datetime
from typing import Dict, Any

TEST_CREATE_LABWARE_MSG_OBJECT: Dict[str, Any] = {
    "messageUuid": "b01aa0ad-7b19-4f94-87e9-70d74fb8783c".encode(),
    "messageCreateDateUtc": datetime.now(),
    "labware": {
        "labwareType": "Plate12x8",
        "barcode": "BARCODE001",
        "samples": [
            {
                "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f6".encode(),
                "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
                "sangerSampleId": "cichlid_pacbio8196429",
                "location": "A01",
                "supplierSampleName": "SampleSupplied1",
                "volume": "5",
                "concentration": "5",
                "publicName": "SamplePublicName1",
                "taxonId": "10090",
                "commonName": "Mus Musculus",
                "donorId": "cichlid_pacbio8196429",
                "libraryType": "Saphyr_v1",
                "countryOfOrigin": "United Kingdom",
                "sampleCollectionDateUtc": datetime.now(),
            },
            {
                "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f7".encode(),
                "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
                "sangerSampleId": "cichlid_pacbio8196430",
                "location": "B01",
                "supplierSampleName": "SampleSupplied2",
                "volume": "5",
                "concentration": "5",
                "publicName": "SamplePublicName2",
                "taxonId": "10090",
                "commonName": "Mus Musculus",
                "donorId": "cichlid_pacbio8196430",
                "libraryType": "Saphyr_v1",
                "countryOfOrigin": "United Kingdom",
                "sampleCollectionDateUtc": datetime.now(),
            },
        ],
    },
}


TEST_INVALID_CREATE_LABWARE_MSG_OBJECT: Dict[str, Any] = {
    "messageUuid": "b01aa0ad7b19-4f94-87e9-70d74fb8783c".encode(),
    "messageCreateDateUtc": datetime.now(),
    "labware": {
        "labwareType": "Plate12x8",
        "barcode": "BARCODE001",
        "samples": [
            {
                "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f6".encode(),
                "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
                "sangerSampleId": "cichlid_pacbio8196429",
                "location": "A1",
                "supplierSampleName": "SampleSupplied1",
                "volume": "ee5",
                "concentration": "ee5",
                "publicName": "SamplePublicName1",
                "taxonId": "ee10090",
                "commonName": "Mus Musculus",
                "donorId": "cichlid_pacbio8196429",
                "libraryType": "Saphyr_v1",
                "countryOfOrigin": "United Kingdom",
                "sampleCollectionDateUtc": datetime.now(),
            },
            {
                "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f7".encode(),
                "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
                "sangerSampleId": "cichlid_pacbio8196430",
                "location": "B1",
                "supplierSampleName": "SampleSupplied2",
                "volume": "ee5",
                "concentration": "ee5",
                "publicName": "SamplePublicName2",
                "taxonId": "ee10090",
                "commonName": "Mus Musculus",
                "donorId": "cichlid_pacbio8196430",
                "libraryType": "Saphyr_v1",
                "countryOfOrigin": "United Kingdom",
                "sampleCollectionDateUtc": datetime.now(),
            },
        ],
    },
}

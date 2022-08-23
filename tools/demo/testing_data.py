from datetime import datetime

CREATE_LABWARE_MSG = {
    "messageUuid": "b01aa0ad-7b19-4f94-87e9-70d74fb8783c".encode(),
    "messageCreateDateUtc": datetime.now().timestamp() * 1000,
    "labware": {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "barcode": "BARCODE001",
        "samples": [
            {
                "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f6".encode(),
                "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
                "sangerSampleId": "cichlid_pacbio8196429",
                "location": "A1",
                "supplierSampleName": "SampleSupplied1",
                "volume": "5",
                "concentration": "5",
                "publicName": "SamplePublicName1",
                "taxonId": 10090,
                "commonName": "Mus Musculus",
                "donorId": "cichlid_pacbio8196429",
                "libraryType": "Library1",
                "countryOfOrigin": "United Kingdom",
                "sampleCollectionDateUtc": datetime.now().timestamp() * 1000
            },
            {
                "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f7".encode(),
                "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
                "sangerSampleId": "cichlid_pacbio8196430",
                "location": "B1",
                "supplierSampleName": "SampleSupplied2",
                "volume": "5",
                "concentration": "5",
                "publicName": "SamplePublicName2",
                "taxonId": 10090,
                "commonName": "Mus Musculus",
                "donorId": "cichlid_pacbio8196430",
                "libraryType": "Library1",
                "countryOfOrigin": "United Kingdom",
                "sampleCollectionDateUtc": datetime.now().timestamp() * 1000

            }
        ]
    }
}

UPDATE_LABWARE_MSG = {
    "messageUuid": "78fedc85-fa9d-494d-951e-779d208e8c0g".encode(),
    "messageCreateDateUtc": datetime.now().timestamp() * 1000,
    "labwareUpdates": [{
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "name": "barcode", 
        "value": "BARCODE0002",
    }],
    "sampleUpdates": [
        {
            "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f7".encode(),
            "name": "sangerSampleId", 
            "value": "cichlid_pacbio8196429"
        },
        {
            "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f7".encode(),
            "name": "supplierSampleName", 
            "value": "SampleSupplied1"
        },
        {
            "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f6".encode(),
            "name": "commonName", 
            "value": "Mus Musculus"
        },
    ],
}

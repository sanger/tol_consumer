from tol_lab_share.message_properties.sample import Sample
from tol_lab_share.message_properties.labware_type import LabwareType
from datetime import datetime
from tol_lab_share.message_properties.input import Input


def test_sample_is_valid():
    lt = LabwareType(Input("Plate12x8"))

    sample = {
        "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f6".encode(),
        "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
        "sangerSampleId": "cichlid_pacbio8196429",
        "location": "A01",
        "supplierSampleName": "SampleSupplied1",
        "volume": "5",
        "concentration": 5,
        "publicName": "SamplePublicName1",
        "taxonId": 10090,
        "commonName": "Mus Musculus",
        "donorId": "cichlid_pacbio8196429",
        "libraryType": "Library1",
        "countryOfOrigin": "United Kingdom",
        "sampleCollectionDateUtc": datetime.now().timestamp() * 1000,
    }

    instance = Sample(lt, sample)
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_sample_is_invalid():
    lt = LabwareType(Input("Plate12x8"))
    instance = Sample(lt, {"publicName": 1234})
    assert instance.validate() is False
    assert len(instance.errors) > 0

    sample = {
        "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f6",
        "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
        "sangerSampleId": 1234,
        "location": "A001",
        "supplierSampleName": "1234",
        "volume": "5",
        "concentration": "5",
        "publicName": "1234",
        "taxonId": "10090",
        "commonName": 1234,
        "donorId": 1234,
        "libraryType": 1234,
        "countryOfOrigin": 1234,
        "sampleCollectionDateUtc": str(datetime.now().timestamp() * 1000),
    }

    instance = Sample(lt, sample)
    assert instance.validate() is False
    assert len(instance.errors) > 0

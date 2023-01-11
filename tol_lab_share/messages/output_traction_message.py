from typing import Dict, Optional


class OutputTractionMessageRequest:
    def __init__(self):
        self._library_type = None
        self._study_uuid = None
        self._sample_name = None
        self._sample_uuid = None
        self._container_barcode = None
        self._container_location = None
        self._container_type = None

    @property
    def container_type(self) -> Optional[str]:
        return self._container_type

    @container_type.setter
    def container_type(self, value: Optional[str]) -> None:
        self._container_type = value

    @property
    def container_location(self) -> Optional[str]:
        return self._container_location

    @container_location.setter
    def container_location(self, value: Optional[str]) -> None:
        self._container_location = value

    @property
    def container_barcode(self) -> Optional[str]:
        return self._container_barcode

    @container_barcode.setter
    def container_barcode(self, value: Optional[str]) -> None:
        self._container_barcode = value

    @property
    def sample_uuid(self) -> Optional[str]:
        return self._sample_uuid

    @sample_uuid.setter
    def sample_uuid(self, value: Optional[str]) -> None:
        self._sample_uuid = value

    @property
    def sample_name(self) -> Optional[str]:
        return self._sample_name

    @sample_name.setter
    def sample_name(self, value: Optional[str]) -> None:
        self._sample_name = value

    @property
    def library_type(self) -> Optional[str]:
        return self._library_type

    @library_type.setter
    def library_type(self, value: Optional[str]) -> None:
        self._library_type = value

    @property
    def study_uuid(self) -> Optional[str]:
        return self._study_uuid

    @study_uuid.setter
    def study_uuid(self, value: Optional[str]) -> None:
        self._study_uuid = value

    def serializer(self):
        for serializerClass in SERIALIZERS:
            if serializerClass.match(self):
                return serializerClass(self)


class RequestSerializer:
    def __init__(self, instance: OutputTractionMessageRequest):
        self.instance = instance

    @staticmethod
    def match(instance: OutputTractionMessageRequest) -> bool:
        return False


class SaphyrRequestSerializer(RequestSerializer):
    @staticmethod
    def match(instance: OutputTractionMessageRequest) -> bool:
        return instance.library_type == "Saphyr_v1"

    def request_payload(self):
        return {"library_type": self.instance.library_type, "external_study_id": self.instance.study_uuid}

    def sample_payload(self):
        return {"name": self.instance.sample_name, "external_id": self.instance.sample_uuid, "species": "human"}

    def container_payload(self):
        if self.instance.container_type == "tubes":
            return {"type": self.instance.container_type, "barcode": self.instance.container_barcode}
        else:
            return {
                "type": self.instance.container_type,
                "barcode": self.instance.container_barcode,
                "position": self.instance.container_location,
            }

    def payload(self):
        return {
            "request": self.request_payload(),
            "sample": self.sample_payload(),
            "container": self.container_payload(),
        }


SERIALIZERS = [SaphyrRequestSerializer]


class OutputTractionMessage:
    def __init__(self):
        self._requests: Dict[int, OutputTractionMessageRequest] = {}

    def requests(self, position: int) -> OutputTractionMessageRequest:
        if position not in self._requests:
            self._requests[position] = OutputTractionMessageRequest()

        return self._requests[position]

    def request_attributes(self):
        return [self.requests(position).serializer().payload() for position in range(len(self._requests))]

    def payload(self):
        return {
            "data": {
                "type": "receptions",
                "attributes": {"source": "traction-ui.sequencescape", "request_attributes": self.request_attributes()},
            }
        }

    def validate(self):
        return True

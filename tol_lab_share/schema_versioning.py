class SchemaVersioning:
    def __init__(self, schema_name, version):
        self._schema_name = schema_name
        self._version = version

    def supports(self, schema_versioning):
        if schema_versioning is None:
            return True

        return (schema_versioning.schema_name == self.schema_name) and (
            int(self.version) >= int(schema_versioning.version)
        )

    @property
    def schema_name(self):
        return self._schema_name

    @property
    def version(self):
        return self._version


CREATE_LABWARE_SUPPORTING_ACCESSIONING_AND_GENOME = SchemaVersioning("create-labware", "3")

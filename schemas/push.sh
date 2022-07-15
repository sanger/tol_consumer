curl -X POST -d @create-labware/1.txt -H "Content-Type: application/vnd.schemaregistry.v1+json" http://localhost:8081/subjects/create-labware/versions

curl -X POST -d @create-labware-feedback/1.txt -H "Content-Type: application/vnd.schemaregistry.v1+json" http://localhost:8081/subjects/create-labware-feedback/versions

curl  -X POST -d @update-labware/1.txt -H "Content-Type: application/vnd.schemaregistry.v1+json" http://localhost:8081/subjects/update-labware/versions

curl -X POST -d @update-labware-feedback/1.txt -H "Content-Type: application/vnd.schemaregistry.v1+json" http://localhost:8081/subjects/update-labware-feedback/versions

To download

curl -H "Content-Type: application/vnd.schemaregistry.v1+json" http://localhost:8081/subjects/create-labware/versions/1

To upload:

curl -X POST -d @1.txt -H "Content-Type: application/vnd.schemaregistry.v1+json" http://localhost:8081/subjects/create-labware/versions

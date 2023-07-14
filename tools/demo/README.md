How to run
----------

1. Create a docker image for the project that we will use to run the code.
This saves a lot of problems when installing dependent libraries in local.
To build you have to reference to the root folder of the project that contains the 
Dockerfile file, for example, if you run the command from inside this folder it should be:

```bash
  docker build ../../ -t tol-lab-share:develop
```

2. Create a file .env with this content (fill in the data on the entries that have ...):

```
SETTINGS_MODULE=tol_lab_share.config.defaults
LOCALHOST=host.docker.internal
REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
REDPANDA_URL=...
REDPANDA_API_KEY=...
RABBITMQ_HOST=...
RABBITMQ_USERNAME=...
RABBITMQ_PASSWORD=...
```

An example .env file for local development:

```
SETTINGS_MODULE=tol_lab_share.config.defaults
LOCALHOST=host.docker.internal
REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
REDPANDA_URL=http://host.docker.internal:8081
REDPANDA_API_KEY=redpanda-test
RABBITMQ_HOST=host.docker.internal
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=admin
RABBITMQ_PASSWORD=development
```

3. Run the previously created image using the env variables defined in
the previous step:

```bash
   docker run -ti -v $(pwd):/code -v /etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro --env-file=.env --entrypoint bash tol-lab-share:develop
```

4. Inside this new bash we can run the command using pipenv:

Note: Set the flag uses_ssl=False in tools/demo/publisher.py for local development to disable the use of ssl.

```bash
   pipenv run python tools/demo/publisher.py
```

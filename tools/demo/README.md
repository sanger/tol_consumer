How to run
----------

1. Create a docker image for the project that we will use to run the code.
This saves a lot of problems when installing dependent libraries in local.

```bash
  docker build . -t tol-lab-share:develop
```

2. Create a file .env with this content:

```
SETTINGS_MODULE=tol_lab_share.config.defaults
LOCALHOST=host.docker.internal
REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
REDPANDA_URL=...
REDPANDA_API_KEY=...
RABBITMQ_HOST=...
RABBITMQ_USERNAME=...
RABBITMQ_PASSWORD=...
```

3. Run the previously created image using the env variables defined in
the previous step:

```bash
   docker run -ti -v $(pwd):/code -v /etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro --env-file=.env --entrypoint bash tol-lab-share:develop
```

4. Inside this new bash we can run the command using pipenv:

```bash
   pipenv run python tools/demo/publisher.py
```

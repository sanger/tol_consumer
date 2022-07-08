# Getting started using Docker

To set up a local development environment in Docker, you have to build a new Docker image for
tol-lab-share. start a stack of services that include a Redpanda schema registry and Rabbitmq. 
You can do all together by running the command:

```shell
docker-compose up -d
```

With this we should have started tol-lab-share and all required services. 

After the services have started, in another terminal, you can enter start and interactive shell in the tol-lab-share container
with:

```shell
./bin/tolc_docker_exec.sh bash
```

## Local development setup 

You may want to start only the container for tol-lab-share standalone and use your local version of the
related services instead of the Docker version, in that case you can start this setup with the
command:

```shell
docker-compose -f docker-compose-standalone.yml up -d
```

## Recreating Docker images 
If you need to recreate the image built on first start (because you made modifications
to the Dockerfile file or in configuration) you can run a building process with:

```shell
docker-compose build
```

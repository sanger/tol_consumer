## Setting up a complete development environment from scratch

1. Start dependent services: RabbitMQ and RedPanda
```bash
  ./docker/dependencies/up.sh
```

2. Setup RabbitMQ configuration (queues, etc). You may need to wait 30 seconds from the previous command
to run this one as it requires Rabbitmq to have started completely:
```bash
    python setup_dev_rabbit.py
```

3. Load Redpanda schemas:
```bash
    ./schemas/push.sh http://localhost:8081 redpanda-test
```

4. Build docker image
```bash
    docker build . -t tol-lab-share:develop
```

5. Create .env file with contents
```
SETTINGS_MODULE=tol_lab_share.config.defaults
LOCALHOST=host.docker.internal
```

6. Start interactive bash in docker container
```bash
    docker run -ti -v $(pwd):/code --env-file=.env --entrypoint bash tol-lab-share:develop
```

7. Start service (inside the previous bash)
```bash
    pipenv run python main.py
```

After this you should have:

* Consumer (python main.py) running connected to Rabbitmq queue
* Rabbitmq service running in http://localhost:8080/ with user/password: admin/development
* Redpanda API service running in local in http://localhost:8081/
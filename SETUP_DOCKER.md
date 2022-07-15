## Setting up a complete development environment from scratch

1. Start dependent services: Rabbitmq and Redpanda
```bash
  cd docker
  docker-compose up -d
  cd ..
```

2. Setup Rabbitmq configuration (queues, etc)
```bash
    python setup_dev_rabbit.py
```

3. Load Redpanda schemas:
```bash
    cd schemas
    ./push.sh . http://localhost:8081
    cd ..
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
    docker run -ti -v $(pwd):/code --env-file=.env tol-lab-share:develop bash
```

7. Start service (inside the previous bash)
```bash
    pipenv run python main.py
```
#!/bin/bash
docker exec -ti $(docker ps -q -f name=tol_consumer_tol_consumer_1) $@

#!/bin/bash
if [[ $# -lt 1 ]]; then
    echo "At least 1 argument is required."
    exit 1
fi

if test -z `docker ps -q -f name=tol-lab-share_tol-lab-share_1`; then 
    echo "No tol-lab-share found"
    exit 1
fi

docker exec -ti $(docker ps -q -f name=tol-lab-share_tol-lab-share_1) $@

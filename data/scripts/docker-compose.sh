#!/bin/bash
username=$(whoami)
# Move to directory with all the data and .yml file
cd /mnt/scrap/users/dopiro/docker/data/

# Fixes error message about different versions of server and client 
export COMPOSE_API_VERSION=1.18

# Launches all containers
/usr/local/bin/docker-compose up

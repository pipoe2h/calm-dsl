#!/bin/bash

#set -ex

SCOPE=$1
DOCKER_LOCAL_VOLUME_PATH="$(pwd)"

if [ $SCOPE == "blueprint" ]; then
    BLUEPRINTS_PATH="${DOCKER_LOCAL_VOLUME_PATH}/blueprints"
    BLUEPRINT=$2
    DOCKER_MOUNT_PATH="${BLUEPRINTS_PATH}/${BLUEPRINT}"
else
    CUSTOMERS_PATH="${DOCKER_LOCAL_VOLUME_PATH}/customers"
    CUSTOMER=$2
    CALM_PROJECT=$3
    DOCKER_MOUNT_PATH="${CUSTOMERS_PATH}/${CUSTOMER}/${CALM_PROJECT}"
fi


CALM_SECRETS_DIR="${CUSTOMERS_PATH}/secrets"

mkdir -p ${CALM_SECRETS_DIR}
docker run --name calm-dsl --rm -it --mount type=bind,src="${DOCKER_LOCAL_VOLUME_PATH}"/.calm,target=/root/.calm,readonly --mount type=bind,src="${DOCKER_LOCAL_VOLUME_PATH}",dst=/root -w /root/local-repo/customers/${CUSTOMER} ntnx/calm-dsl
#!/bin/bash

read -p 'Application name: ' appName

WORKDIR=/workspaces/calm-dsl/blueprints

cd $WORKDIR
calm describe app $appName -o json | jq '.status.resources.deployment_list[].substrate_configuration.element_list[] | "\(.instance_name) \(.address)"'
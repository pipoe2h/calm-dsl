#!/bin/bash
WORKDIR=/workspaces/calm-dsl/blueprints

cd $WORKDIR
calm create project -f demo-developer/blueprint/01_Create_Project/project_devdsl.py -n $CALM_DSL_DEFAULT_PROJECT
calm update cache
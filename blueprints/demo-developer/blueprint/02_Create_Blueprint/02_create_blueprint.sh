#!/bin/bash

read -p 'Blueprint name: ' bpName

WORKDIR=/workspaces/calm-dsl/blueprints

cd $WORKDIR
calm create bp -f demo-developer/blueprint/02_Create_Blueprint/blueprint.py -fc -n $bpName
#!/bin/bash

read -p 'Blueprint name: ' bpName
read -p 'Application name: ' appName

WORKDIR=/workspaces/calm-dsl/blueprints

cd $WORKDIR
calm create bp -f demo-developer/blueprint/05_Update_Blueprint/blueprint.py -fc -n $bpName
calm launch bp -l demo-developer/blueprint/05_Update_Blueprint/variables.py -a $appName $bpName
#!/bin/bash

read -p 'Blueprint name: ' bpName
read -p 'Application name: ' appName

WORKDIR=/workspaces/calm-dsl/blueprints

cd $WORKDIR
# calm launch bp -w -a $appName $bpName
calm launch bp -a $appName $bpName
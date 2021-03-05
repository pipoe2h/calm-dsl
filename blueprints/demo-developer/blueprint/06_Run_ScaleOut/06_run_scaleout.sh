#!/bin/bash

read -p 'Application name: ' appName
read -p 'Action name: ' actionName

WORKDIR=/workspaces/calm-dsl/blueprints

cd $WORKDIR
calm run action -w -a $appName $actionName
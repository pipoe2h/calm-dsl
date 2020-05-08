BP_DIR_PATH="calm-dsl/blueprints/vm-mobility"
OS_USERNAME="@@{Cred_OS.username}@@"
OS_PASSWORD=@@{Cred_OS.secret}@@
AWS_AMI_ID="@@{AWS_AMI_ID}@@"
AWS_REGION="@@{AWS_REGION}@@"
AWS_VPC_ID="@@{AWS_VPC_ID}@@"
AWS_SG_ID="@@{AWS_SG_ID}@@"
MOVE_VAPP_IP="@@{MOVE_VAPP_IP}@@"
PE_UUID="@@{PE_UUID}@@"
SC_UUID="@@{SC_UUID}@@"
AHV_NETWORKUUID="@@{PROJECT_NETWORKUUID}@@"
MOVE_AWS_PROVIDERUUID="@@{MOVE_AWS_PROVIDERUUID}@@"
MOVE_AHV_PROVIDERUUID="@@{MOVE_AHV_PROVIDERUUID}@@"
MOVE_PASSWORD=@@{Cred_PC.secret}@@

git --work-tree $HOME/calm-dsl/ --git-dir calm-dsl/.git pull

docker run --rm -it \
    -e CALMDSL_OS_USERNAME=$OS_USERNAME \
    -e CALMDSL_OS_PASSWORD=$OS_PASSWORD \
    -e CALMDSL_AWS_AMI_ID=$AWS_AMI_ID \
    -e CALMDSL_AWS_REGION=$AWS_REGION \
    -e CALMDSL_AWS_VPC_ID=$AWS_VPC_ID \
    -e CALMDSL_AWS_SG_ID=$AWS_SG_ID \
    -e CALMDSL_MOVE_VAPP_IP=$MOVE_VAPP_IP \
    -e CALMDSL_PE_UUID=$PE_UUID \
    -e CALMDSL_SC_UUID=$SC_UUID \
    -e CALMDSL_AHV_NETWORKUUID=$AHV_NETWORKUUID \
    -e CALMDSL_MOVE_AWS_PROVIDERUUID=$MOVE_AWS_PROVIDERUUID \
    -e CALMDSL_MOVE_AHV_PROVIDERUUID=$MOVE_AHV_PROVIDERUUID \
    -e CALMDSL_MOVE_PASSWORD=$MOVE_PASSWORD \
    -v $HOME/config/.calm:/root/.calm \
    -v $HOME/$BP_DIR_PATH/:/root/vm-mobility/ ntnx/calm-dsl \
    /bin/bash -c " \
    calm create bp -n @@{calm_application_name}@@-bp-move-awsVm \
    -f vm-mobility/bps/move-aws-demo-vm.py --force \
    && calm launch bp -i \
    -a @@{calm_application_name}@@-app-move-awsVm \
    @@{calm_application_name}@@-bp-move-awsVm \
    && calm watch app @@{calm_application_name}@@-app-move-awsVm"

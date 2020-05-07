BP_DIR_PATH="calm-dsl/blueprints/vm-mobility"
MOVE_IMAGE_URL="http://@@{address}@@:8080/move-@@{Move_Version}@@/move-@@{Move_Version}@@.qcow2"
PROJECT_NETWORK="@@{PROJECT_NETWORK}@@"
MOVE_PASSWORD="@@{Cred_PC.secret}@@"


git --work-tree $HOME/calm-dsl/ --git-dir calm-dsl/.git pull

docker run --rm -it\
    -e MOVE_QCOW2_URL=$MOVE_IMAGE_URL \
    -e PROJECT_NETWORK=$PROJECT_NETWORK \
    -e CALMDSL_MOVE_PASSWORD=$MOVE_PASSWORD \
    -v $HOME/config/.calm:/root/.calm \
    -v $HOME/$BP_DIR_PATH/:/root/vm-mobility/ ntnx/calm-dsl \
    /bin/bash -c " \
    calm create bp -n @@{calm_application_name}@@-bp-move-vApp \
    -f vm-mobility/bps/move-ahv-appliance.py --force \
    && calm launch bp -i \
    -a @@{calm_application_name}@@-app-move-vApp \
    @@{calm_application_name}@@-bp-move-vApp \
    && calm watch app @@{calm_application_name}@@-app-move-vApp"

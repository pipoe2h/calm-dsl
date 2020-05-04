BP_DIR_PATH="calm-dsl/blueprints/vm-mobility"

docker run --rm --name calm-dsl \
    -v $HOME/config/.calm:/root/.calm \
    -v $HOME/$BP_DIR_PATH/:/root/vm-mobility/ ntnx/calm-dsl \
    /bin/bash -c " \
    calm create bp -n @@{calm_application_name}@@-bp-move-vApp \
    -f vm-mobility/bps/move-ahv-appliance.py; \
    calm launch bp \
    -a @@{calm_application_name}@@-app-move-vApp \
    @@{calm_application_name}@@-bp-move-vApp"

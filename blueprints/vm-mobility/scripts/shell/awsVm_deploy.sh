BP_DIR_PATH="calm-dsl/blueprints/vm-mobility"
OS_USERNAME="@@{Cred_OS.username}@@"
OS_PASSWORD=@@{Cred_OS.secret}@@

git --work-tree $HOME/calm-dsl/ --git-dir calm-dsl/.git pull

docker run --rm --name calm-dsl \
    -e CALMDSL_OS_USERNAME=$OS_USERNAME \
    -e CALMDSL_OS_PASSWORD=$OS_PASSWORD \
    -v $HOME/config/.calm:/root/.calm \
    -v $HOME/$BP_DIR_PATH/:/root/vm-mobility/ ntnx/calm-dsl \
    /bin/bash -c " \
    calm create bp -n @@{calm_application_name}@@-bp-move-awsVm \
    -f vm-mobility/bps/move-aws-demo-vm.py --force; \
    calm launch bp -i \
    -a @@{calm_application_name}@@-app-move-awsVm \
    @@{calm_application_name}@@-bp-move-awsVm"

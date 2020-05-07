PC_IP="@@{PC_IP}@@"
PC_ADMIN="@@{Cred_PC.username}@@"
PC_PASSWORD=@@{Cred_PC.secret}@@
PROJECT="@@{calm_project_name}@@"

git clone --single-branch --branch vm-mobility https://github.com/pipoe2h/calm-dsl.git

mkdir -p $HOME/config/.calm
docker run --rm \
    -v $HOME/config/.calm:/root/.calm \
    ntnx/calm-dsl \
    calm init dsl -i $PC_IP -P 9440 -u $PC_ADMIN -p $PC_PASSWORD -pj $PROJECT

MOVE_VER="@@{Move_Version}@@"
MOVE_PACKAGE="move-${MOVE_VER}.zip"
MOVE_TARBALL="http://download.nutanix.com/NutanixMove/${MOVE_VER}/${MOVE_PACKAGE}"

sudo yum install -y wget unzip git
wget -q -O $HOME/${MOVE_PACKAGE} ${MOVE_TARBALL}
mkdir -p $HOME/www
unzip $HOME/${MOVE_PACKAGE} -d $HOME/www/move-${MOVE_VER}
rm $HOME/${MOVE_PACKAGE}
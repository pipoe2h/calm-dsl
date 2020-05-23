export ISO_MOUNT_DIR=/mnt/iso
export IMG_TEMP_DIR=/data_disk
export IMG_CALM_DIR=$IMG_TEMP_DIR/calm_iso
export IMG_URL=@@{IMG_URL}@@
export IMG_URI=${IMG_URL##*/}
export IMG_NAME=$(echo "$IMG_URI" | cut -f 1 -d '.')
export ARTIFACTORY_USERNAME=admin
export ARTIFACTORY_PASSWORD=@@{ARTIFACTORY_PASSWORD}@@
export CALM_REPO=http://@@{address}@@:8082/artifactory/calm-isos
 

sudo wget $IMG_URL -O $IMG_TEMP_DIR/$IMG_URI
sudo mount -o loop $IMG_TEMP_DIR/$IMG_URI $ISO_MOUNT_DIR
sudo mkdir -p $IMG_CALM_DIR
sudo cp -R /mnt/iso/* $IMG_CALM_DIR/
sudo umount $ISO_MOUNT_DIR

# Change isolinux.cfg to auto start installation
sudo mv $IMG_CALM_DIR/boot/x86_64/loader/isolinux.cfg $IMG_CALM_DIR/boot/x86_64/loader/isolinux.cfg.bak

echo "
default Autoinstallation

# autoyast
label Autoinstallation
  kernel linux
  append initrd=initrd splash=silent instmode=cd ifcfg=eth0=dhcp autoyast=http://@@{address}@@:8082/artifactory/autoyast-profiles/ showopts

implicit	1
prompt		1
timeout		30
" | sudo tee $IMG_CALM_DIR/boot/x86_64/loader/isolinux.cfg


sudo cd $IMG_TEMP_DIR/
sudo mkisofs -o $IMG_TEMP_DIR/$IMG_NAME-CALM.iso -udf -f -r -gui -graft-points -b boot/x86_64/loader/isolinux.bin -c boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -no-emul-boot -V SLE12SP3SAPCALM $IMG_CALM_DIR/
sudo curl -u $ARTIFACTORY_USERNAME:$ARTIFACTORY_PASSWORD \
    -X PUT \
    -T $IMG_TEMP_DIR/$IMG_NAME-CALM.iso \
    $CALM_REPO/$IMG_NAME-CALM.iso
    
sudo cd /
sudo rm -fR $IMG_TEMP_DIR/$IMG_CALM_DIR
sudo rm -fR $IMG_TEMP_DIR/$IMG_NAME*

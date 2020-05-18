# Cloud-init SSH password issue in Move
sudo sed -i '/ssh_pwauth:   0/c\ssh_pwauth:   1' /etc/cloud/cloud.cfg

# GRUB boot issue in Move
sudo sed -i '/^GRUB_CMDLINE_LINUX/ s/console=ttyS0,115200/rd.debug/' /etc/default/grub
sudo grub2-mkconfig -o /boot/grub2/grub.cfg

# Remove NGT from previous migration
sudo python /usr/local/nutanix/ngt/python/bin/uninstall_ngt_core.py --force
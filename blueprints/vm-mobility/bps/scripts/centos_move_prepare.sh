# Cloud-init SSH password issue in Move
sudo sed -i '/ssh_pwauth:   0/c\ssh_pwauth:   1' /etc/cloud/cloud.cfg

# GRUB boot issue in Move
sudo sed -i '/^GRUB_CMDLINE_LINUX/ s/=0[^"]*"/=0 systemd.log_level=info"/' /etc/default/grub
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
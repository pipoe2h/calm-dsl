# sudo apt update -y
# sudo apt install -y cloud-initramfs-growroot xfce4 xfce4-goodies

sudo growpart /dev/sda 1
sudo resize2fs /dev/sda1
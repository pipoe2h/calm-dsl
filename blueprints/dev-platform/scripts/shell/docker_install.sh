sudo apt update -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update -y
apt-cache policy docker-ce
sudo apt install -y docker-ce
sudo usermod -aG docker @@{DEVELOPER_USERNAME}@@

echo '
{
 "data-root": "/home/@@{DEVELOPER_USERNAME}@@/data_disk/docker",
 "insecure-registries": ["@@{DOCKER_REGISTRIES_CIDR}@@"]
}' | sudo tee /etc/docker/daemon.json

sudo systemctl restart docker
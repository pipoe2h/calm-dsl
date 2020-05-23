# Uninstall old versions
sudo yum remove -y docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine

# Set up the repository
sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# Install the latest version of Docker Engine
sudo yum install -y docker-ce docker-ce-cli containerd.io

# Enable and start Docker
sudo systemctl enable docker
sudo systemctl start docker

# Add current user to Docker
sudo usermod -aG docker $USER
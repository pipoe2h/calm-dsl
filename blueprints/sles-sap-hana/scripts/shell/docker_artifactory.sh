export DATA_DIR=/data_disk
export JFROG_HOME=$DATA_DIR/services/jfrog

# Create your Artifactory home directory and an empty system.yaml file.
sudo mkdir -p $JFROG_HOME/artifactory/var/etc/
cd $JFROG_HOME/artifactory/var/etc/
sudo touch ./system.yaml
sudo chown -R 1030:1030 $JFROG_HOME/artifactory/var

# Start the Artifactory container
docker run --name artifactory --restart always -v $JFROG_HOME/artifactory/var/:/var/opt/jfrog/artifactory -d -p 8081:8081 -p 8082:8082 docker.bintray.io/jfrog/artifactory-oss:latest

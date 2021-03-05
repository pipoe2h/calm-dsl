# Start a Web server with the packages
echo @@{CRED_DOCKER.secret}@@ | docker login --username=@@{CRED_DOCKER.username}@@ --password-stdin
docker rm webserver --force
docker run -dit --rm --name webserver -p 80:80 -e "PLATFORM=@@{PLATFORM}@@" --hostname @@{name}@@ @@{KUBERNETES_DEPLOYMENT_CONTAINER_IMAGE}@@

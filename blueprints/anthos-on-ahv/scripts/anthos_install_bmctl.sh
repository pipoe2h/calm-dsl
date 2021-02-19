cluster_name=@@{ANTHOS_CLUSTER_NAME}@@
project_id=@@{GCP_PROJECT_ID}@@ 
tmpfile=@@{GCP_KEY}@@
os_secret='@@{CRED_OS.secret}@@'

# ============== DO NO CHANGE AFTER THIS ===============

# Install Anthos CLI (bmctl)
mkdir baremetal
cd baremetal
gsutil cp gs://anthos-baremetal-release/bmctl/1.6.1/linux-amd64/bmctl bmctl
chmod a+x bmctl

# Create Anthos configuration template
echo "$os_secret" > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa

export GOOGLE_APPLICATION_CREDENTIALS="$tmpfile"

./bmctl create config -c $cluster_name \
  --enable-apis --create-service-accounts --project-id=$project_id

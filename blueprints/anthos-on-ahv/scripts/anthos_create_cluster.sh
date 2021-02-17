export ANTHOS_TEMPLATE_PATH="/home/nutanix/baremetal/bmctl-workspace/@@{ANTHOS_CLUSTER_NAME}@@/@@{ANTHOS_CLUSTER_NAME}@@.yaml"
export ANTHOS_SSH_KEY="/home/nutanix/.ssh/id_rsa"
export ANTHOS_CLUSTER_TYPE="hybrid"
export ANTHOS_CONTROLPLANE_ADDRESSES="@@{ControlPlaneVMs.address}@@"
export ANTHOS_CONTROLPLANE_VIP=@@{ANTHOS_CONTROLPLANE_VIP}@@
export ANTHOS_PODS_NETWORK=@@{ANTHOS_PODS_NETWORK}@@
export ANTHOS_SERVICES_NETWORK=@@{ANTHOS_SERVICES_NETWORK}@@
export ANTHOS_INGRESS_VIP=@@{ANTHOS_INGRESS_VIP}@@
export ANTHOS_LB_ADDRESSPOOL=@@{ANTHOS_LB_ADDRESSPOOL}@@
export ANTHOS_LVPNODEMOUNTS="/home/nutanix/localpv-disk"
export ANTHOS_LVPSHARE="/home/nutanix/localpv-share"
export ANTHOS_LOGINUSER="nutanix"
export ANTHOS_WORKERNODES_ADDRESSES="@@{WorkerNodesVMs.address}@@"
export ANTHOS_CLUSTER_NAME="@@{ANTHOS_CLUSTER_NAME}@@"
export GOOGLE_APPLICATION_CREDENTIALS="@@{GCP_KEY}@@"
export PYTHON_ANTHOS_GENCONFIG="@@{PYTHON_ANTHOS_GENCONFIG}@@"

# ============== DO NO CHANGE AFTER THIS ===============

# Install PyYAML
sudo python2 -m pip install pyyaml

# Create Anthos configuration file
cd ~/baremetal
curl -s $PYTHON_ANTHOS_GENCONFIG | python2

# Create Anthos Kubernetes cluster
if ./bmctl create cluster -c $ANTHOS_CLUSTER_NAME ; then
    export KUBECONFIG=$HOME/baremetal/bmctl-workspace/${ANTHOS_CLUSTER_NAME}/${ANTHOS_CLUSTER_NAME}-kubeconfig
    echo "KUBECONFIG=$KUBECONFIG"
else
    exit 1
fi


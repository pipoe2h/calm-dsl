export KUBECONFIG=@@{KUBECONFIG}@@
export NTNX_CSI_URL=@@{NTNX_CSI_URL}@@
export NTNX_PE_IP=@@{NTNX_PE_IP}@@
export NTNX_PE_PORT=@@{NTNX_PE_PORT}@@
export NTNX_PE_USERNAME=@@{CRED_PE.username}@@
export NTNX_PE_PASSWORD=@@{CRED_PE.secret}@@
export NTNX_PE_DATASERVICE_IP=@@{NTNX_PE_DATASERVICE_IP}@@
export NTNX_PE_STORAGE_CONTAINER=@@{NTNX_PE_STORAGE_CONTAINER}@@

# ============== DO NO CHANGE AFTER THIS ===============

cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1beta1
kind: CSIDriver
metadata:
  name: csi.nutanix.com
spec:
  attachRequired: false
  podInfoOnMount: true
EOF

cd ~/baremetal
curl -s -o csi.tar.gz \
  ${NTNX_CSI_URL}

mkdir -p csi && tar xvf csi.tar.gz -C csi --strip-components 1

kubectl create -f csi/ntnx-csi-rbac.yaml
kubectl create -f https://raw.githubusercontent.com/pipoe2h/calm-dsl/anthos-on-ahv/blueprints/anthos-on-ahv/scripts/ntnx-csi-node.yaml
kubectl create -f csi/ntnx-csi-provisioner.yaml

export CSI_KEY=$(echo -n "${NTNX_PE_IP}:${NTNX_PE_PORT}:${NTNX_PE_USERNAME}:${NTNX_PE_PASSWORD}" | base64)

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: ntnx-secret
  namespace: kube-system
data:
  key: ${CSI_KEY}
EOF

cat <<EOF | kubectl apply -f -
allowVolumeExpansion: true
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
    annotations:
        storageclass.kubernetes.io/is-default-class: "true"
    name: nutanix-default
parameters:
   csi.storage.k8s.io/provisioner-secret-name: ntnx-secret
   csi.storage.k8s.io/provisioner-secret-namespace: kube-system
   csi.storage.k8s.io/node-publish-secret-name: ntnx-secret  
   csi.storage.k8s.io/node-publish-secret-namespace: kube-system
   csi.storage.k8s.io/controller-expand-secret-name: ntnx-secret
   csi.storage.k8s.io/controller-expand-secret-namespace: kube-system
   csi.storage.k8s.io/fstype: ext4
   dataServiceEndPoint: ${NTNX_PE_DATASERVICE_IP}:3260
   flashMode: DISABLED
   storageContainer: ${NTNX_PE_STORAGE_CONTAINER}
   chapAuth: DISABLED
   storageType: NutanixVolumes
provisioner: csi.nutanix.com
reclaimPolicy: Delete
EOF

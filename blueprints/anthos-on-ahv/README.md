# Google Anthos on Nutanix AHV


## What to expect

With this folder you can generate a Calm blueprint using DSL or just upload the compiled blueprint in JSON format directly to Calm.


## Overview

This automation project helps you to deploy an Anthos Kubernetes cluster on Nutanix AHV. The characteristics for the Kubernetes cluster are:


* Anthos version: bare metal 1.6.1 - <https://cloud.google.com/anthos/clusters/docs/bare-metal/1.6/concepts/about-bare-metal>

* Type: hybrid - <https://cloud.google.com/anthos/clusters/docs/bare-metal/1.6/installing/install-prep#hybrid_cluster_deployment>

* Number of virtual machines: 6

    * 1 x Admin

    * 3 x Control plane

    * 2 x Worker nodes


* Virtual machine OS: CentOS 8 GenericCloud - <https://cloud.centos.org/centos/8/x86_64/images/CentOS-8-GenericCloud-8.2.2004-20200611.2.x86_64.qcow2>

* High availability: yes

* Load balancing: yes

* Ingress: yes

* Persistent storage: yes

* Proxy: no

* KubeVirt: no

* OpenID Connect: no

* Application logs/metrics: no

## Prerequisites

* Nutanix:

    * Cluster:
    
        * AHV: 20201105.1045 or later
        
        * AOS: 5.19.1 or later

        * iSCSI data service IP configured

        * VLAN network with AHV IPAM configured
    
    * Prism Central: 2020.11.0.1 or later

    * Calm:
    
        * Version: 3.0.0.2 or later
        * A project with AHV provider

* Google Cloud:

    * A project with Owner role

    * A service account - <https://console.cloud.google.com/iam-admin/serviceaccounts/create>

        * Role: Project Owner

        * A private key: JSON

* Networking:

    * Internet connectivity 

    * AHV IPAM: Minimum 6 IP addresses available for the virtual machines
    
    * Kubernetes:

        * Control plane VIP: One IP address in the same network than virtual machines but not part of the AHV IPAM

        * Ingress VIP: One IP address in the same network than virtual machines but not part of the AHV IPAM. This IP must be part of the load balancing pool

        * Load balancing pool: Range of IP addresses in the same network than virtual machines but not part of the AHV IPAM. The Ingress VIP is included in this pool

        * Pods network: CIDR network with enough IP addresses, usually /16 and not sharing the same network than virtual machines or Kubernetes Services. If your containerized application must communicate with a system out of the Kubernetes cluster, make sure then this network doesn't overlap either with the external system network

        * Services network: CIDR network with enough IP addresses, usually /16 and not sharing the same network than virtual machines or Kubernetes Pods. If your containerized application must communicate with a system out of the Kubernetes cluster, make sure then this network doesn't overlap either with the external system network

* Credentials:

    * Operating system: you need a SSH key. It must start with `---BEGIN RSA PRIVATE KEY---`. To generate one in a terminal:
    
        ```console
        $ ssh-keygen -m PEM -t rsa -f <keyname>
        ```

    * Prism Element: an account, local or Active Directory, with *User Admin* role. This is for the CSI plugin configuration

## Getting Started

This blueprint has been developed using Calm DSL to provide Infrastructure as Code. If you are not familiar with DSL, you can learn with this [post series](https://www.nutanix.dev/calm-dsl). There is no need for you to use DSL, you can just upload the JSON file in the main directory.

If you want to compile this blueprint using Calm DSL move to [Using DSL](##using-dsl), otherwise, continue reading to use the blueprint option.

## Using Blueprint

This method is for using the *blueprint.json* file in the main directory. 

1. Save the [blueprint](https://raw.githubusercontent.com/pipoe2h/calm-dsl/anthos-on-ahv/blueprints/anthos-on-ahv/blueprint.json) in your computer. You can right-click the link, and choose *Save Link As...*

2. Upload the blueprint into Calm

3. Select the same network in the *Config Pane* for each of the three services: adminVm, ControlPlaneVMs and WorkerNodesVMs

4. Credentials:

    * CRED_OS: Upload a SSH private key. You can leave the user *nutanix* if you like

    * CRED_PE: Configure username and password with an user that has *User Admin* role in the Prism Element cluster that will provide persistent storage

    * CRED_GCLOUD: This is the GCP Service Account name you have created with the format *`name`*@*`project`*.iam.gserviceaccount.com. Upload the JSON key that was generated as part of the GCP service account creation.

5. Default Application Profile variables

    Configure the variable values accordingly to your environment. There are a few of them that are privates, runtime disabled, that most of the time are static and doesn't need changes. You can always make them available at launch checking the runtime icon if you need to deliver more flexibility to the user. 

    * ANTHOS_CLUSTER_NAME: Anthos cluster name

    * ANTHOS_CONTROLPLANE_VIP: This is the IP address for Kubernetes API. Format: XXX.XXX.XXX.XXX

    * ANTHOS_PODS_NETWORK: This is the network for your pods. Preferably do not overlap with other networks. CIDR format: XXX.XXX.XXX.XXX/XX

    * ANTHOS_SERVICES_NETWORK: This is the network for your services. Preferably do not overlap with other networks. CIDR format: XXX.XXX.XXX.XXX/XX

    * ANTHOS_INGRESS_VIP: This is the IP address for Kubernetes Ingress. This address MUST be within the load balancing pool. Format: XXX.XXX.XXX.XXX

    * ANTHOS_LB_ADDRESSPOOL: This is the IP address range for Load Balancing. Format: XXX.XXX.XXX.XXX-YYY.YYY.YYY.YYY

    * KUBERNETES_SERVICE_ACCOUNT: This K8s SA is for Google Cloud Console so the K8s cluster can be managed in GKE. This service account will have cluster-admin role for Google Cloud Marketplace to work. Default is  *google-cloud-console*

    * OS_DISK_SIZE: The minimum OS disk size MUST be 128GB, recommended by Google is 256GB

    * PYTHON_ANTHOS_GENCONFIG: This script is hosted externally and produce an Anthos configuration file for cluster creation with user provided inputs during launch. DO NOT CHANGE default value unless you will host the script in an internal repository.

    * NTNX_CSI_URL: Nutanix CSI Driver URL. Minimum supported version is 2.3.1

    * NTNX_PE_IP: The Prism Element VIP address is needed for the CSI plugin to create persistent volumes via the API. This VIP doesn't have to be the one where the Anthos cluster will run. You can choose any VIP of any of your clusters from where you want to get persistent storage

    * NTNX_PE_PORT: Prism Element port. Default is *9440*

    * NTNX_PE_DATASERVICE_IP: Data service is required to allow iSCSI connectivity between the Kubernetes pods and the volumes created by CSI plugin

    * NTNX_PE_STORAGE_CONTAINER: This is the Nutanix Storage Container where the requested Persistent Volume Claims will get their volumes created. You can enable things like compression and deduplication in a Storage Container. The recommendation is to create at least one storage container in Prism Element well identified for Karbon usage. This will facilitate the search of persistent volumes when the environment scales

## Using DSL
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

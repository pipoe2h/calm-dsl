pipeline {
  agent {
    kubernetes {
      label 'pod-dind'
      defaultContainer 'dind'
      yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  # Use service account that can deploy to all namespaces
  serviceAccountName: cd-jenkins
  containers:
  - name: calm-dsl
    image: ntnx/calm-dsl:latest
    command:
    - cat
    tty: true
"""
}

  }
  stages {
    stage('Print Message') {
      steps {
        echo 'Hello world'
      }
    }

    stage('Test') {
      steps {
        container('calm-dsl'){
          sh 'calm'
        }
      }
    }

  }
}
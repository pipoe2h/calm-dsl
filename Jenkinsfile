pipeline {
  agent {
    kubernetes {
      label 'jenkins-jenkins-slave '
      defaultContainer 'jnlp'
      yaml '''
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
'''
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
        container(name: 'calm-dsl') {
          sh 'calm'
        }

      }
    }

  }
}
pipeline {
  agent {
    kubernetes {
      label 'pod-dind'
      defaultContainer 'ntnx/calm-dsl'
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
        sh 'calm'
      }
    }

  }
}
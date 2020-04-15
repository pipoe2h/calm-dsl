pipeline {
  agent {
    kubernetes {
      label 'dsl-app'
      idleMinutes 5
      yamlFile 'build-pod.yaml'
      defaultContainer 'calm-dsl'
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
        sh '''
          ls -la
          calm init dsl -h
        '''
      }
    }

  }
}
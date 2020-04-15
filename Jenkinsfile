pipeline {
  agent {
    kubernetes {
      label 'dsl-app'
      idleMinutes 5
      yamlFile 'build-pod.yaml'
      defaultContainer 'calm-dsl'
    }
  }

  // environment {
  //       PC_IP = "bar"
  // }

  stages {
    stage('Print Message') {
      steps {
        echo 'Hello world'
      }
    }

    stage('Test') {
      input {
        parameters {
          string(name: 'PC_IP', defaultValue: '192.168.2.50', description: 'Prism Central IP address')
        }
      }
      steps {
        sh '''
          ls -la
          echo ${env.PC_IP}
          calm init dsl -i ${env.PC_IP}
        '''
      }
    }

  }
}
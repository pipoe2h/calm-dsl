pipeline {
  agent {
    kubernetes {
      label 'dsl-app'
      idleMinutes 5
      yamlFile 'build-pod.yaml'
      defaultContainer 'calm-dsl'
    }
  }
  
  parameters {
    string(name: 'PC_IP', defaultValue: '192.168.2.50', description: 'Prism Central IP address')
    string(name: 'PC_USER', defaultValue: 'admin', description: 'Prism Central username')
    password(name: 'PC_PASSWORD', defaultValue: 'nutanix/4u', description: 'Enter a password')
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
      steps {
        sh "calm init dsl -i ${params.PC_IP} -u ${params.PC_USER} -p ${params.PC_PASSWORD}"
      }
    }

  }
}
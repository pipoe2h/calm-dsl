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
      environment {
        PASSWORD = ${params.PC_PASSWORD}
      }
      steps {
        sh "calm init dsl -i ${params.PC_IP} -P ${params.PC_PORT} -u ${params.PC_USER} -p $PASSWORD -pj ${params.CALM_PROJECT}"
      }
    }

  }
  parameters {
    string(name: 'PC_IP', defaultValue: '192.168.2.50', description: 'Prism Central IP address')
    string(name: 'PC_PORT', defaultValue: '9440', description: 'Prism Central port')
    string(name: 'PC_USER', defaultValue: 'admin', description: 'Prism Central username')
    password(name: 'PC_PASSWORD', defaultValue: 'nutanix/4u', description: 'Enter a password')
    string(name: 'CALM_PROJECT', defaultValue: 'default', description: 'Calm project')
  }
}
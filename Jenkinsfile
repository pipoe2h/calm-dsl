BPPATH = ''
pipeline {
  agent none
  options {
    buildDiscarder(logRotator(numToKeepStr: '3'))
    disableConcurrentBuilds()
    timeout(time: 24, unit: 'HOURS')
  }
  stages {
    stage('Cleanup') {
      agent {
        label 'jenkins-jenkins-slave'
      }
      steps {
        sh "git clean -x -f"
      }
    }
    stage('Discovering blueprint...') {
      agent {
        node {
          label 'jenkins-jenkins-slave'
          // customWorkspace "/tmp/${BRANCH_NAME}-${BUILD_NUMBER}"
        }
      }
      steps {
        script {
          BPPATH = sh(script: '/bin/bash -c "git show --name-only HEAD^..HEAD | tail -1 | cut -d/ -f1-2"', returnStdout: true).trim()
        }
      }
    }
    stage('Calm DSL...') {
      environment {
        CALM_CRED = credentials('Jenkins Calm Service Account')
        CALM_USER = "${env.CALM_CRED_USR}"
        CALM_PASSWORD = "${env.CALM_CRED_PSW}"
        WINDOWS_LOCAL_ADMINISTRATOR_PASSWORD = credentials('Windows_Local_Administrator_Password')
        DOMAIN_JOIN_USER_PASSWORD = credentials('Domain_Join_User_Password')
        WINDOWS_LICENSE_KEY = credentials('Windows_License_Key')
      }
      agent {
        kubernetes {
          label 'dsl-app'
          idleMinutes 5
          yamlFile 'build-pod.yaml'
          defaultContainer 'calm-dsl'
        }
      }
      steps {
        sh "calm init dsl -i ${params.PC_IP} -P ${params.PC_PORT} -u $CALM_USER -p $CALM_PASSWORD -pj ${params.CALM_PROJECT}"
        sh "calm create bp -f ${BPPATH}/*.py --name jg-dsl-${BRANCH_NAME}-${BUILD_NUMBER}"
        sh "calm launch bp -a jg-dsl-${BRANCH_NAME}-${BUILD_NUMBER} jg-dsl-${BRANCH_NAME}-${BUILD_NUMBER}"
        // sh "calm watch app jg-dsl-${BRANCH_NAME}-${BUILD_NUMBER}"
        cleanWs()
      }
    }
  }
  // post { 
  //   always { 
  //     agent {
  //       label 'default'
  //     }
  //     deleteDir()
  //   } 
  // }
  parameters {
    string(name: 'PC_IP', defaultValue: '192.168.2.50', description: 'Prism Central IP address')
    string(name: 'PC_PORT', defaultValue: '9440', description: 'Prism Central port')
    string(name: 'CALM_PROJECT', defaultValue: 'default', description: 'Calm project')
  }
}
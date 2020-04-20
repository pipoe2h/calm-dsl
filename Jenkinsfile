// def BPPATH = sh(script: '/bin/bash -c "git show --name-only HEAD^..HEAD | tail -1 | cut -d/ -f1-2"', returnStdout: true)

pipeline {
  agent none
  // agent {
  //   kubernetes {
  //     label 'dsl-app'
  //     idleMinutes 5
  //     yamlFile 'build-pod.yaml'
  //     defaultContainer 'calm-dsl'
  //   }
  // }
  environment {
    BPPATH = ''
  }
  stages {
    stage('Discovering blueprint...') {
      agent any
      steps {
        // script {
        //   // def ver_script = '$/git show --name-only HEAD^..HEAD | tail -1 | cut -d/ -f1-2/$'
        //   // echo "${ver_script}"
        //   // BPPATH = sh(script: '/bin/bash -c "git show --name-only HEAD^..HEAD | tail -1 | cut -d/ -f1-2"', returnStdout: true)
        //   // echo "${BPPATH}"
        //   // env.BPPATH = BPPATH
        // }
        sh '/bin/bash -c "git show --name-only HEAD^..HEAD | tail -1 | cut -d/ -f1-2"'
        stash 'BPPATH'
      }
    }
    stage('Calm DSL...') {
      environment {
        CALM_CRED = credentials('Jenkins Calm Service Account')
        CALM_USER = "${env.CALM_CRED_USR}"
        CALM_PASSWORD = "${env.CALM_CRED_PSW}"
        CALM_BPPATH = "${env.BPPATH}"
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
        unstash 'BPPATH'
        sh "source BPPATH; echo $BPPATH"
        sh "calm init dsl -i ${params.PC_IP} -P ${params.PC_PORT} -u $CALM_USER -p $CALM_PASSWORD -pj ${params.CALM_PROJECT}"
        sh "source BPPATH; calm compile bp -f $BPPATH/*.py"
      }
    }
  }
  parameters {
    string(name: 'PC_IP', defaultValue: '192.168.2.50', description: 'Prism Central IP address')
    string(name: 'PC_PORT', defaultValue: '9440', description: 'Prism Central port')
    string(name: 'CALM_PROJECT', defaultValue: 'default', description: 'Calm project')
  }
}
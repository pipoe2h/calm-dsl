pipeline {
  agent {
    docker {
      image 'ntnx/calm-dsl'
    }

  }
  stages {
    stage('Print Message') {
      steps {
        echo 'Hello world'
      }
    }

  }
}
pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('download') {
      steps {
        sh 'python3 24-05-07-BD-Descarga-Descomprimir_1.py'
      }
    }
  }
}
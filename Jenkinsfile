pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'py --version'
      }
    }
    stage('download') {
      steps {
        sh 'py 24-05-07-BD-Descarga-Descomprimir_1.py'
      }
    }
    stage('presidencia') {
      steps {
        sh 'py presidencia.py'
      }
    }
    stage('publicacion') {
      steps {
        sh 'py publicacion.py'
      }
    }
    }
  }

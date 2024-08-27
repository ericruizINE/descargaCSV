pipeline {
  agent any
  stages {
    stage('Setup') {
            steps {
                // Crear el entorno virtual
              cd /var/jenkins_home/workspace/Descarga\ CSV/path/to/venv.
              source venv/bin/activate
              // sh 'python3 -m venv venv'
            }
        }
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
    stage('presidencia') {
      steps {
        sh 'python3 presidencia.py'
      }
    }
    stage('publicacion') {
      steps {
        sh 'python3 publicacion.py'
      }
    }
    }
  }

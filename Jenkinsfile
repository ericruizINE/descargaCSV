pipeline {
  agent any
  stages {
    stage('Setup') {
            steps {
                // Instalar virtualenv si no está instalado
                //sh 'pip3 install --root virtualenv'
                // Crear el entorno virtual
                sh 'python3 -m venv venv'
            }
        }
    stage('Install Dependencies') {
            steps {
                // Activar el entorno virtual y luego instalar las dependencias
                sh '''
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
    stage('version') {
      steps {
        sh '''
              . venv/bin/activate
        sh 'python3 --version'
        '''
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

pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
    }
    stages {
        stage('Setup Virtualenv') {
            steps {
                sh 'pip3 install --user virtualenv'
                sh "python3 -m venv ${VENV_DIR}"
            }
        }
        stage('Install Requirements') {
            steps {
                sh """
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                """
            }
        }
        stage('Version Python') {
            steps {
                sh """
                    . ${VENV_DIR}/bin/activate
                    python --version
                """
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

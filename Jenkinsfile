pipeline {
    agent any
    stages {
        stage('Install Virtualenv') {
            steps {
                sh 'sudo pip3 install virtualenv'
            }
        }
        stage('Setup Virtualenv') {
            steps {
                sh 'virtualenv venv'
            }
        }
        stage('Install Requirements') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python --version
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

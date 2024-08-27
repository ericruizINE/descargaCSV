pipeline {
    agent any
    environment {
        VENV_DIR = '/var/jenkins_home/workspace/Descarga CSV Publicación/venv'
    }
    stages {
        stage('Checkout') {
            steps {
                // Clonar el repositorio Git
                git url: 'https://github.com/ericruizINE/descargaCSV.git', branch: 'main'
            }
        }
        stage('Setup Virtualenv') {
            steps {
                // Crear el entorno virtual en el workspace
                sh "python3 -m venv ${VENV_DIR}"
            }
        }
        stage('Install Dependencies') {
            steps {
                // Activar el entorno virtual e instalar las dependencias
                sh """
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                """
            }
        }
        stage('Run Tests') {
            steps {
                // Ejecutar tests dentro del entorno virtual
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

pipeline {
    agent any    
    environment {
        VENV_DIR = '/var/jenkins_home/workspace/Publicacion/venv'
    }
    stages {
        stage('Clean Up') {
            steps {
                deleteDir()
            }
        }
        stage('Install venv') {
            steps {
                // Instalar el paquete python3-venv si aún no está instalado
                sh 'apt-get update && apt-get install -y python3-venv'
                sh 'apt-get update && apt-get install -y python3-pip'
            }
        }
        stage('Setup Virtualenv') {
            steps {
                // Crear el entorno virtual
                sh "python3 -m venv ${VENV_DIR}"
            }
        }
        stage('Install Dependencies') {
            steps {
                // Activar el entorno virtual e instalar las dependencias
                sh """
                    . ${VENV_DIR}/bin/activate
                    pip install --no-cache-dir -r requirements.txt
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

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
        stage('Checkout') {
            steps {
                // Clonar el repositorio Git
                git url: 'https://github.com/ericruizINE/descargaCSV.git', branch: 'main'
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
        stage('Version Python') {
            steps {
                // Ejecutar tests dentro del entorno virtual
                sh """
                    . ${VENV_DIR}/bin/activate
                    python3 --version
                """
            }
          }
        stage('Install ChromeDriver') {
            steps {
                // Descarga e instala la versión correcta de ChromeDriver
                sh """
                    CHROME_VERSION=$(google-chrome --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
                    CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)
                    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
                    unzip chromedriver_linux64.zip -d /usr/local/bin/
                """
            }
        }
        stage('Descarga de CSV') {
          steps {
            sh """
                    . ${VENV_DIR}/bin/activate
                    python3 24-05-07-BD-Descarga-Descomprimir_1.py
               """
          }
        }
        stage('Validación datos') {
          steps {
            sh """
                    . ${VENV_DIR}/bin/activate
                    python3 presidencia.py
               """
          }
        }
        stage('Validacion Publicación') {
          steps {
            sh """
                    . ${VENV_DIR}/bin/activate
                    python3 publicacion.py
               """
          }
        }
    }
  }

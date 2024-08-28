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
        stage('Show Screenshot URLs') {
            steps {
                script {
                    // Mostrar las URLs de las capturas de pantalla
                    def screenshots = sh(script: "ls ${WORKSPACE}/screenshots_publi/*.png", returnStdout: true).trim().split('\n')
                    screenshots.each { screenshot ->
                        echo "Screenshot URL: ${env.BUILD_URL}execution/node/3/ws/screenshots_publi/${screenshot.split('/').last()}"
                    }
            }
        }
    }
  }
}

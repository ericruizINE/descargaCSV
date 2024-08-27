pipeline {
  agent any
  stages {
    stage('Setup') {
            steps {
                // Crear el entorno virtual
              //cd '/var/jenkins_home/workspace/Descarga CSV/path/to/venv.'
              //source venv/bin/activate
              sh 'python3 -m venv venv'
              //sh 'source venv/bin/activate'
              sh '. venv/bin/activate'
              //sh 'python3 -m pip install --upgrade pip'
              sh 'pwd'
            }
        }
    stage('Install Dependencies') {
            steps {
                // pip install -r requirements.txt
                sh 'pip install requests'
                sh 'pip install selenium'
                sh 'pip install webdriver-manager'
                sh 'pip install pandas'
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

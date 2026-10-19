pipeline {
    agent any

    environment {
        IMAGE_NAME           = 'muhammadagilh/simple-app'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Melakukan checkout dari SCM...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat 'echo Mulai build aplikasi'
                bat 'docker version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%BUILD_NUMBER% ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: REGISTRY_CREDENTIALS,
                        usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    bat 'echo %DH_PASS%| docker login -u %DH_USER% --password-stdin'
                    bat "docker push %IMAGE_NAME%:%BUILD_NUMBER%"
                    bat "docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest"
                    bat "docker push %IMAGE_NAME%:latest"
                }
            }
        }

        stage('Deploy App + Database') {
            steps {
                bat 'docker compose version'
                bat 'docker-compose version'
                bat 'docker compose up -d --build'
            }
        }

        stage('Verify') {
            steps {
                // tunggu app dan database siap, lalu cek endpoint /health
                bat 'ping -n 16 127.0.0.1 > nul'
                bat 'curl -f http://localhost:5000/health'
            }
        }
    }

    post {
        always {
            echo 'Selesai build'
        }
    }
}

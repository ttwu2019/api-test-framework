pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat '''
                    pip install requests pytest pytest-html pyyaml
                '''
            }
        }
        
        stage('Run API Tests') {
            steps {
                bat '''
                    cd api_test_framework
                    python run_tests.py
                '''
            }
        }
        
        stage('Publish Test Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    includes: '**/*.html',
                    reportDir: 'api_test_framework/reports',
                    reportFiles: 'report.html',
                    reportName: 'API Test Report'
                ])
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Build Successful!'
        }
        failure {
            echo 'Build Failed!'
        }
    }
}

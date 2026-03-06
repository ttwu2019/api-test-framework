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
                    python -m pytest tests/ -v --html=reports/report.html --self-contained-html
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'api_test_framework/reports/**', allowEmptyArchive: true
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                includes: '**/*.html',
                reportDir: 'api_test_framework/reports',
                reportFiles: 'report.html',
                reportName: 'API Test Report'
            ])
        }
        success {
            echo 'Build Successful!'
        }
        failure {
            echo 'Build Failed!'
        }
    }
}

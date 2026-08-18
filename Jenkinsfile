pipeline {
    // 1. CHANGE THIS AGENT BLOCK
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.42.0-jammy'
            // This runs the pipeline inside a container that already has Python 3 and Playwright installed
        }
    }

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    # Create and activate virtual environment
                    python3 -m venv venv
                    . venv/bin/activate
                    
                    # Install Python dependencies
                    pip install pytest pytest-playwright allure-pytest requests playwright-stealth
                    
                    # You don't need install-deps here anymore because the Docker image already has them!
                    playwright install chromium
                '''
            }
        }

        stage('Execute Playwright Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        . venv/bin/activate
                        pytest tests/ --target-device=desktop --tracing=retain-on-failure --screenshot=only-on-failure --alluredir=allure-results
                    '''
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            archiveArtifacts artifacts: 'test-results/**/trace.zip', allowEmptyArchive: true
            archiveArtifacts artifacts: 'jenkins_reports/videos/**/*.webm', allowEmptyArchive: true
            cleanWs()
        }
    }
}
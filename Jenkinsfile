pipeline {
    agent any

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
                    if ! command -v python3 > /dev/null 2>&1; then
                        echo "Python3 is missing from this Jenkins node. Installing it now..."
                        apt-get update && apt-get install -y python3 python3-venv python3-pip
                    fi

                    python3 -m venv venv
                    . venv/bin/activate
                    
                    pip install pytest pytest-playwright allure-pytest requests playwright-stealth
                    playwright install chromium
                    playwright install-deps chromium
                '''
            }
        }

        stage('Execute Playwright Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        . venv/bin/activate
                        # Added --video=retain-on-failure flag here
                        pytest tests/ --target-device=desktop --tracing=retain-on-failure --screenshot=only-on-failure --video=retain-on-failure --alluredir=allure-results
                    '''
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            
            // Updated to pull traces and videos directly from the test-results folder
            archiveArtifacts artifacts: 'test-results/**/trace.zip', allowEmptyArchive: true
            archiveArtifacts artifacts: 'test-results/**/*.webm', allowEmptyArchive: true
            
            cleanWs()
        }
    }
}
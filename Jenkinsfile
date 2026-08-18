pipeline {
    // Spin up the official Playwright container to run our tests
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.42.0-jammy'
            // Run as root to prevent Jenkins workspace permission errors
            args '-u root:root' 
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
                    # Because we are using the Playwright Docker image, 
                    # Python 3 and all browsers are ALREADY installed!
                    # We only need to install our specific framework dependencies.
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Execute Playwright Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        # Run the tests directly (no venv needed in this isolated container)
                        pytest tests/ --device=desktop --tracing=retain-on-failure --screenshot=only-on-failure --alluredir=allure-results
                    '''
                }
            }
        }
    }

    post {
        always {
            // Generate Allure Report
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            
            // Archive FFMPEG Videos and Playwright Traces
            archiveArtifacts artifacts: 'jenkins_reports/videos/*.webm, test-results/**/trace.zip', allowEmptyArchive: true
            
            // Cleanup workspace
            cleanWs()
        }
    }
}
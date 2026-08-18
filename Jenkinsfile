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
                    # Create and activate virtual environment
                    python3 -m venv venv
                    . venv/bin/activate
                    
                    # Install Python dependencies
                    pip install pytest pytest-playwright allure-pytest requests
                    
                    # Install Playwright browsers and required Linux OS dependencies
                    playwright install chromium
                    playwright install-deps chromium
                '''
            }
        }

        stage('Execute Playwright Tests') {
            steps {
                // catchError ensures the pipeline moves to the 'post' stage even if tests fail
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        . venv/bin/activate
                        # Run the tests and generate Allure results
                        pytest tests/ --device=desktop --tracing=retain-on-failure --screenshot=only-on-failure --alluredir=allure-results
                    '''
                }
            }
        }
    }

    post {
        always {
            // Safely execute post-actions only if a workspace exists
            node {
                // 1. Generate Allure Report
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
                
                // 2. Archive Playwright Traces (for manual debugging)
                archiveArtifacts artifacts: 'test-results/**/trace.zip', allowEmptyArchive: true
                
                // 3. Clean up the workspace to prevent VPS disk bloat
                cleanWs()
            }
        }
    }
}
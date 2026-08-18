pipeline {
    agent any // Or specify a docker agent if your VPS uses Docker

    environment {
        // Ensure Python outputs directly to Jenkins console
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
                    # Create a virtual environment so we don't break VPS system packages
                    python3 -m venv venv
                    . venv/bin/activate
                    
                    # Install Python dependencies
                    pip install -r requirements.txt
                    
                    # Install Playwright browsers and OS dependencies (Linux)
                    playwright install chromium
                    playwright install-deps chromium
                '''
            }
        }

        stage('Execute Playwright Tests') {
            steps {
                // catchError ensures the pipeline continues to the reporting stage even if a test fails
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        . venv/bin/activate
                        # Run Desktop Tests
                        pytest tests/ --device=desktop --tracing=retain-on-failure --screenshot=only-on-failure --alluredir=allure-results
                        
                        # Run Mobile Tests (Optional, uncomment if needed)
                        # pytest tests/ --device=iphone_15_pro_max --alluredir=allure-results
                    '''
                }
            }
        }
    }

    post {
        always {
            // 1. Generate Allure Report
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            
            // 2. Archive FFMPEG Videos and Playwright Traces
            archiveArtifacts artifacts: 'jenkins_reports/videos/*.mp4, test-results/**/trace.zip', allowEmptyArchive: true
            
            // 3. Cleanup workspace to save VPS disk space
            cleanWs()
        }
    }
}
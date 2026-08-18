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
                    # 1. Find Python or install it if missing
                    if command -v python3 &>/dev/null; then
                        PYTHON_CMD="python3"
                    elif command -v python &>/dev/null; then
                        PYTHON_CMD="python"
                    else
                        echo "Python not found. Attempting to install..."
                        # Try installing (works if Jenkins has apt-get access)
                        apt-get update && apt-get install -y python3 python3-venv python3-pip || sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip
                        PYTHON_CMD="python3"
                    fi

                    echo "Using Python command: $PYTHON_CMD"

                    # 2. Create and activate virtual environment
                    $PYTHON_CMD -m venv venv
                    . venv/bin/activate
                    
                    # 3. Install Python dependencies
                    pip install pytest pytest-playwright allure-pytest requests playwright-stealth
                    
                    # 4. Install Playwright browsers and required Linux OS dependencies
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
                        pytest tests/ --target-device=desktop --tracing=retain-on-failure --screenshot=only-on-failure --alluredir=allure-results
                    '''
                }
            }
        }
    }

    post {
        always {
            // Generate Allure Report
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            
            // Archive Playwright Traces AND Videos
            archiveArtifacts artifacts: 'test-results/**/trace.zip', allowEmptyArchive: true
            archiveArtifacts artifacts: 'jenkins_reports/videos/**/*.webm', allowEmptyArchive: true
            
            // Clean up the workspace
            cleanWs()
        }
    }
}
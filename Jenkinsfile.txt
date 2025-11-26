pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Installing Python dependencies...'
                // Install dependencies from requirements.txt
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'python3 -m unittest discover -s .'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application (copying to deploy folder)...'
                sh '''
                mkdir -p ${WORKSPACE}/python-app-deploy
                cp ${WORKSPACE}/app.py ${WORKSPACE}/python-app-deploy/
                cp ${WORKSPACE}/requirements.txt ${WORKSPACE}/python-app-deploy/
                '''
            }
        }

        stage('Run Application') {
            steps {
                echo 'Running application in background...'
                sh '''
                cd ${WORKSPACE}/python-app-deploy
                nohup python3 app.py > app.log 2>&1 &
                echo $! > app.pid
                '''
            }
        }

        stage('Test Application') {
            steps {
                echo 'Testing application via unit tests again...'
                sh 'python3 test_app.py'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for more details.'
        }
    }
}

pipeline {
    environment {
        DOCKER_ID = 'nimamrze'
        DOCKER_IMAGE = 'lioraapi'
        DOCKER_TAG = "v.${BUILD_ID}.0"
    }

    agent any

    stages {
        stage('Docker Build') {
            steps {
                script {
                    sh '''
                    docker rm -f lioraapi || true
                    docker build -t $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG .
                    sleep 6
                    '''
                }
            }
        }

        stage('Docker run') {
            steps {
                script {
                    sh '''
                    docker rm -f lioraapi || true
                    docker run -d -p 8000:80 --name lioraapi $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG
                    sleep 10
                    '''
                }
            }
        }

        stage('Test Acceptance') {
            steps {
                script {
                    sh '''
                    curl -f http://localhost:8000
                    '''
                }
            }
        }

        stage('Docker Push') {
            environment {
                DOCKER_CREDS = credentials('DOCKER_HUB_PASS')
            }
            steps {
                script {
                    sh '''
            echo "$DOCKER_CREDS_PSW" | docker login -u "$DOCKER_CREDS_USR" --password-stdin
            docker push "$DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG"
            '''
                }
            }
        }

        stage('Deployment in dev') {
            environment {
                KUBECONFIG = credentials('config')
            }
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cat $KUBECONFIG > .kube/config
                    cp fastapi/values.yaml values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install app fastapi --values=values.yml --namespace dev
                    '''
                }
            }
        }

        stage('Deployment in staging') {
            environment {
                KUBECONFIG = credentials('config')
            }
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cat $KUBECONFIG > .kube/config
                    cp fastapi/values.yaml values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install app fastapi --values=values.yml --namespace staging
                    '''
                }
            }
        }

        stage('Deployment in prod') {
            environment {
                KUBECONFIG = credentials('config')
            }
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    input message: 'Do you want to deploy in production ?', ok: 'Yes'
                }

                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cat $KUBECONFIG > .kube/config
                    cp fastapi/values.yaml values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install app fastapi --values=values.yml --namespace prod
                    '''
                }
            }
        }
    }
    post {
    always {
        echo "POST ALWAYS WORKS"
        mail to: "nimamrze@gmail.com",
            subject: "Test email from Jenkins",
            body: "Build ${env.BUILD_ID} finished with status: ${currentBuild.currentResult}"
    }
}
}

pipeline {

    environment {
    DEV_BRANCH = "main"
    PROD_BRANCH = "--not-defined-yet--"
    AWS_DEFAULT_REGION = "eu-west-1"
//     change key_id and acsess_key
     AWS_ACCESS_KEY_ID = credentials("AWS_ACCESS_KEY_ID_PULSE2.0_COMMISSIONS_DEV")
    AWS_SECRET_ACCESS_KEY = credentials("AWS_SECRET_ACCESS_KEY_PULSE2.0_COMMISSIONS_DEV")
    }

    agent {
        kubernetes {
          yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: docker-client
      image: karser/docker-compose-ci
      command: [cat]
      tty: true
      env:
        - name: DOCKER_HOST
          value: tcp://localhost:2375

    - name: deploy
      image: fishtownanalytics/dbt:0.20.1
      command: [cat]
      tty: true

    - name: docker-server
      securityContext:
        privileged: true
      image: docker:stable-dind
      tty: true
      env:
      - name: DOCKER_TLS_CERTDIR
        value: ""
'''
        }
    }

    stages {

    stage('build') {


      steps {
        container('docker-client') {
            sh '''
set -eux
docker version
echo $GIT_BRANCH
if [ $GIT_BRANCH == $DEV_BRANCH ]; then
  CONTAINER_TAG=v1
  echo $CONTAINER_TAG
else
  CONTAINER_TAG=$GIT_BRANCH
fi
DOCKER_REPOSITORY="pulse2.0-commissions"
CONTAINER_IMAGE="$DOCKER_REPOSITORY:$CONTAINER_TAG"
echo "--- Current container image name is $CONTAINER_IMAGE and image name is $DOCKER_REPOSITORY ..."
docker build . --pull --tag "$CONTAINER_IMAGE"
docker version
docker images
aws sts get-caller-identity
set +x
eval "$(aws ecr get-login --no-include-email)"
set -x
ECR_REGISTRY="$(aws sts get-caller-identity --query "Account" --output text).dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
ECR_REPOSITORY="$ECR_REGISTRY/$DOCKER_REPOSITORY"
ECR_CONTAINER_IMAGE="$ECR_REPOSITORY:$CONTAINER_TAG"
echo "Tagging $CONTAINER_IMAGE as $ECR_CONTAINER_IMAGE"
docker tag "$CONTAINER_IMAGE" "$ECR_CONTAINER_IMAGE"
echo "--------- Image is ready to push to ECR --------"
docker push "$ECR_CONTAINER_IMAGE"
echo "--------- Image pushed successfully ------------"
'''
        }
      }
    }



        stage('Deploy') {
            steps {
                /*
                Only if branch is the right one
                --> Call codedeploy
                */
                container('deploy') {
                    sh '''#!/bin/bash
if [[ "$GIT_BRANCH" == "$DEV_BRANCH" ]]; then
    set -euo pipefail

    CODEDEPLOY_APPLICATION="sms-model"
    CODEDEPLOY_DEPLOYMENT_GROUP="sms-model"
    CODEDEPLOY_DEPLOYMENT_CONFIG="CodeDeployDefault.OneAtATime"
    CODE_TAG="$BUILD_ID"

    python3 CIScripts/codedeploy-deploy.py \
      --application-name $CODEDEPLOY_APPLICATION \
      --deployment-config-name $CODEDEPLOY_DEPLOYMENT_CONFIG \
      --deployment-group-name $CODEDEPLOY_DEPLOYMENT_GROUP \
      --github-location repository=BBOXX/Sms_model,commit=$GIT_COMMIT

elif [[ "$GIT_BRANCH" == "$PROD_BRANCH" ]]; then
    echo "Not implemented yet!"
fi

'''
                }
            }
        }

    }
}
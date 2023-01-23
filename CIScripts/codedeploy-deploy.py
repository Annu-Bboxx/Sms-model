import argparse
import logging
import time

import boto3


logging.basicConfig(level=logging.INFO)
client = boto3.client('codedeploy')


def parse_arguments():

    parser = argparse.ArgumentParser(description='AWS CodeDeploy deployment wrapper: start a deployment and follow it, fail if it fails.')
    parser.add_argument('--application-name', type=str, required=True)
    parser.add_argument('--deployment-group-name', type=str, required=True)
    parser.add_argument('--github-location', type=str, required=True)
    parser.add_argument('--deployment-config-name', type=str, required=False, default='CodeDeployDefault.OneAtATime')
    parser.add_argument('--check-interval', type=int, required=False, default=5, help="Check deployment status every X seconds.")
    args = parser.parse_args()

    args.repository, args.commit_id = _parse_github_location(args.github_location)
    return args


def _parse_github_location(github_string):
    repo, commit = github_string.split(',')
    return repo.replace('repository=', ''), commit.replace('commit=', '')


def start_deployment(args):
    response = client.create_deployment(
        applicationName=args.application_name,
        deploymentGroupName=args.deployment_group_name,
        revision={
            'revisionType': 'GitHub',
            'gitHubLocation': {
                'repository': args.repository,
                'commitId': args.commit_id,
            },
        },
        deploymentConfigName=args.deployment_config_name,
        ignoreApplicationStopFailures=True,
        fileExistsBehavior='OVERWRITE'
    )
    logging.info(f"Started deployment: {args.application_name} on {args.deployment_group_name} from {args.github_location}")
    logging.info(response)
    return response


def check_deployment(deployment):
    response = client.get_deployment(
                        deploymentId=deployment['deploymentId']
               )['deploymentInfo']
    if 'errorInformation' in response:
        deployment['running'] = False
        logging.error(response['errorInformation'])
        raise RuntimeError('Failed Deployment: check on AWS web-console')

    outcome = response['status']
    if outcome == 'Succeeded':
        deployment['running'] = False
        logging.info(f"Deployment completed successfully.")
        return deployment
    else:
        logging.info(f"Deployment still {outcome}.")
        deployment['running'] = True
        return deployment


if __name__ == '__main__':
    args = parse_arguments()
    print(args)

    deployment = start_deployment(args)
    deployment['running'] = True
    while deployment['running']:
        time.sleep(args.check_interval)
        deployment = check_deployment(deployment)
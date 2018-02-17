#!/usr/bin/python
import json
import boto3
import botocore
import sys
from subprocess import call

sqs = boto3.resource('sqs', region_name='us-gov-west-1')
s3 = boto3.resource('s3', region_name='us-gov-west-1')
queue = sqs.get_queue_by_name(QueueName='SnapglassDockerQueue')

BUCKET_NAME = 'snapglass-transfers'

if __name__ == '__main__':
    try:
        while True:
            messages = queue.receive_messages(WaitTimeSeconds=5)
            for message in messages:
                print("Message received: {0}\n".format(message.body))
                try:
                    key_dict = json.loads(message.body)
                    FILE_NAME = 'aws-compose.yml'
                    KEY = key_dict["Records"][0]["s3"]["object"]["key"]
                    s3.Bucket(BUCKET_NAME).download_file(KEY, FILE_NAME)
                    docker_compose_command = ['docker-compose', '-f', FILE_NAME, 'up', '-d']
                    print("Running command: " + " ".join(docker_compose_command) + "\n")
                    call(docker_compose_command)
                except ValueError as ve:
                    print("ValueError: " + str(ve) + "\n")
                except botocore.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == "404":
                        print("The object does not exist.\n")
                    else:
                        raise
                finally:
                    message.delete()
    except KeyboardInterrupt:
        print("KeyboardInterrupt, quitting...")
        sys.exit()

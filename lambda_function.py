import boto3
import json
import os
import logging

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    logger.info("Lambda function invoked.")
    logger.debug(f"Event received: {event}")
    
    glue_client = boto3.client('glue')
    s3_event = event['Records'][0]['s3']  # Get the S3 event

    # S3 Bucket and Object info from event
    bucket_name = s3_event['bucket']['name']
    file_name = s3_event['object']['key']
    
    # Glue Job Name from environment variable
    glue_job_name = os.environ.get('GLUE_JOB_NAME', 'MyGlueJob')
    
    try:
        # Print event details for debugging
        print(f"File uploaded: {file_name} to bucket {bucket_name}")

        # Start the Glue Job
        response = glue_client.start_job_run(
            JobName=glue_job_name,
            Arguments={
                '--bucket_name': bucket_name,
                '--file_name': file_name
            }
        )
        job_run_id = response['JobRunId']

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Glue Job started successfully!',
                'JobRunId': job_run_id
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to start Glue Job'})
        }

import boto3
import json
import os

def lambda_handler(event, context):
    glue_client = boto3.client('glue')

    # Glue Job Name from environment variable
    glue_job_name = os.environ.get('GLUE_JOB_NAME', 'MyGlueJob')

    try:
        # Start the Glue Job
        response = glue_client.start_job_run(JobName=glue_job_name)
        job_run_id = response['JobRunId']

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Glue Job started successfully!',
                'JobRunId': job_run_id
            })
        }
    #except block
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to start Glue Job'})
        }

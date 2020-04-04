import json
import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
import boto3

currentDT = datetime.datetime.now()
Date_time = currentDT.strftime("%Y%m%d_%H%M%S")
print('currentDT is: {a} | Date_time is: {b}'.format(a=currentDT, b=Date_time))

ssm = boto3.client('ssm')

USERNAME = ssm.get_parameter(
    Name="/assignment/Name"
)

USERVALUE = ssm.get_parameter(
    Name="/assignment/Value"
)

USERNAME = USERNAME['Parameter']['Value']
USERVALUE = USERVALUE['Parameter']['Value']

BUCKET_NAME = 'demo-document-bucket-1234'

print('USERNAME:', USERNAME)
print('USERVALUE:', USERVALUE)

# Lambda execution starts here.
def handler(event, context):
    # TODO implementz

    string = USERNAME + ':' + USERVALUE
    encoded_string = string.encode("utf-8")

    file_name = "file_from_s3.txt"
    lambda_path = "/tmp/" + file_name
    s3_path = file_name

    s3 = boto3.resource("s3")
    s3.Bucket(BUCKET_NAME).put_object(Key=s3_path, Body=encoded_string)

    print('PROCESS COMPLETED!!!')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda! Process completed.')
    }
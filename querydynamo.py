import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):


    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('test_table_v3')
    skill = event['skill']
    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.

    resp = table.query(
        KeyConditionExpression=Key('skill').eq(skill)
    )
    respLower = table.query(
        KeyConditionExpression=Key('skill').eq(skill.lower())
    )
    ret = appender(resp) + appender(respLower)
    
    


    return {
        'statusCode': 200,
        'body': ret
    }

def appender(resp):
    ret = []
    respItems = resp['Items']
    for item in respItems:
        job = item['Job'].replace("'",'"')
        jobJson = json.loads(job)

        jobName = jobJson['position_name']
        toAppend = {
            "position_name": jobName
        }
        ret.append(toAppend)
    return ret
    
import json
import requests
import boto3
import json
import sys
import logging
import os
from bs4 import BeautifulSoup

API_URL = 'https://arcssotest33.tcheetah09.com'
API_KEY = 'W3xhAVpaYhCcpOHYewHT6pEvWxtvAoHW'
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/665687765246/position_description'

TABLE_NAME='test_table_v3'

api_url = API_URL  # os.environ['api_url']
api_key = API_KEY  # os.environ['api_key']
startZip = 10000  # int(os.environ['startZip'])
endZip = 99999  # int(os.environ['endZip'])
queue_url = QUEUE_URL  # os.environ['queue_url']

sqs_client = boto3.client('sqs')
comprehend_client = boto3.client('comprehend')
dynamodb_client = boto3.client('dynamodb')

# position_id = os.environ['position_id']

# filter = os.environ['filter']
filter = 'get_opportunity_detail'


def get_comprehend_entities(message, opp):
    # message = json.loads(message)
    if message :
        qualifications = BeautifulSoup(message['qualifications']).get_text()
        position_id = message['position_id']
        try:
            entities = comprehend_client.detect_entities(
                Text=qualifications, LanguageCode='en')
            if entities:
                for entity in entities['Entities']:
                    if not entity['Text'].isnumeric():
                        response_db = dynamodb_client.put_item(TableName=TABLE_NAME, 
                                                            Item={'position': {'N': str(position_id)}, 
                                                            'Job': {'S': str(opp)},
                                                            'skill': {'S': entity['Text']}})                                    
                        print(response_db)
                        
                    else:
                        print(entity['Type'], ' : ', entity['Text'])
                    
        except:
            pass


def simpleGet(url):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.get(url, {'headers': headers})


def getDetails(id):
    parameters = {'nd': filter, 'key': api_key, 'position_id': id}
    response = requests.get(api_url, params=parameters)
    return response


def getFromZipCode(zipCode, api_url=api_url):
    query = {'key': api_key, 'zip_code': zipCode}
    url = f'{api_url}/?nd=get_opportunities&json_req=' + json.dumps(query)
    return simpleGet(url)


def iterateZipCodes(startZip=startZip, endZip=endZip):
    """
    """
    for i in range(startZip, endZip + 1):
        # print(f'area code{i}')
        resp = getFromZipCode(i)
        if resp.text and 'Server Error' not in resp.text:
            jsonResp = json.loads(str(resp.text))
            oppCount = 0
            if 'opportunities' in jsonResp:
                for opp in jsonResp['opportunities']:
                    oppCount += 1
                    # print(f'Opp count: {oppCount}')
                    detResp = getDetails(opp['position_id'])

                    if detResp : 
                        detJson = json.loads(detResp.content.decode('utf-8'))

                        if 'detail' in detJson.keys():
                            MessageBody = {'position_id': opp['position_id'],'qualifications': detJson['detail']['qualifications']}
                            get_comprehend_entities(MessageBody, opp)


if __name__ == "__main__":
    iterateZipCodes()
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

client = boto3.client('sqs', region_name='eu-west-1', aws_access_key_id=os.getenv("AWS_ACCESS_ID"), aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"))
resp = client.get_queue_url(QueueName="AlexaSmarthome.fifo")
qURL=resp['QueueUrl']

try:
    while True:
        resp = client.receive_message(QueueUrl=qURL,WaitTimeSeconds=10)
        if 'Messages' in resp:
            mStr = json.loads(resp['Messages'][0]['Body'])
            print(mStr)
            resp = client.delete_message(QueueUrl=qURL,ReceiptHandle=resp['Messages'][0]['ReceiptHandle'])
except Exception as e:
    print("SQS Error: "+str(e))

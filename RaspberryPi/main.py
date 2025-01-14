import boto3
from dotenv import load_dotenv
import os
import json
import gpiozero
import logging

load_dotenv()

client = boto3.client('sqs', region_name='eu-west-1', aws_access_key_id=os.getenv("AWS_ACCESS_ID"), aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"))
resp = client.get_queue_url(QueueName="iHome.fifo")
qURL=resp['QueueUrl']
light = gpiozero.LED(21)
fan = gpiozero.LED(20)
logging.basicConfig(filename="/home/vishal/iHome.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)


def handleResponse(d):
    try:
        device = d["device"]
        op = d["operation"]
        logging.info("Device: "+device+" Operation: "+op)
        if device == "LIGHT":
            if op == "on":
                light.on()
            elif op == "off":
                light.off()
        if device == "FAN":
            if op == "on":
                fan.on()
            elif op == "off":
                fan.off()
    except:
        print(d)

logging.info("Connecting to SQS...")
try:
    while True:
        resp = client.receive_message(QueueUrl=qURL,WaitTimeSeconds=10)
        if 'Messages' in resp:
            mStr = json.loads(resp['Messages'][0]['Body'])
            handleResponse(mStr)
            resp = client.delete_message(QueueUrl=qURL,ReceiptHandle=resp['Messages'][0]['ReceiptHandle'])
except Exception as e:
    logging.error("SQS Error: "+str(e))
    exit(1)

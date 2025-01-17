import boto3
from dotenv import load_dotenv
import os
import json
import gpiozero
import logging
import os

load_dotenv()

client = boto3.client('sqs', region_name='eu-west-1', aws_access_key_id=os.getenv("AWS_ACCESS_ID"), aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"))
resp = client.get_queue_url(QueueName="iHome.fifo")
qURL=resp['QueueUrl']
light1 = gpiozero.LED(21)
light2 = gpiozero.LED(16)
fan = gpiozero.LED(20)
if os.getenv("REVERSE") == "TRUE":
    rev = True
else:
    rev = False

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
        if device == "LIGHT1":
            if op == "on":
                if rev:
                    light1.off()
                else:
                    light1.on()
            elif op == "off":
                if rev:
                    light1.on()
                else:
                    light1.off()
        elif device == "LIGHT2":
            if op == "on":
                if rev:
                    light2.off()
                else:
                    light2.on()
            elif op == "off":
                if rev:
                    light2.on()
                else:
                    light2.off()
        elif device == "FAN":
            if op == "on":
                if rev:
                    fan.off()
                else:
                    fan.on()
            elif op == "off":
                if rev:
                    fan.on()
                else:
                    fan.off()
        elif device == "AC":
            if op == "on":
                os.system("irsend SEND_ONCE LG_AC AC_ON")
            elif op == "off":
                os.system("irsend SEND_ONCE LG_AC AC_OFF")
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

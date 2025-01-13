import json
import boto3
import uuid

sqs = boto3.resource('sqs', region_name='eu-west-1')
queue = sqs.get_queue_by_name(QueueName='iHome.fifo')

def form_message(device, operation, extravalue="") :
    timestamp = str(uuid.uuid4())
    message = {}
    message['device'] = device
    message['operation'] = operation
    message['extraValue'] = extravalue
    message['timestamp'] = timestamp
    return str(json.dumps(message))

def lambda_handler(event, context):
    # TODO implement
    print(event["queryStringParameters"])
    try:
        params = event["queryStringParameters"]
        queue.send_message(MessageBody=form_message(params["device"],params["operation"]),MessageGroupId='messageGroup1')
        return {
            'statusCode': 200,
            'body': json.dumps({"message":"success"})
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({"message":"invalid params"})
        }

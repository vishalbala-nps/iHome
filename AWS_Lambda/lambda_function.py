import json
from alexa_smarthome import SmartHomeResponseHandler,SmartHomeRequestHandler
import boto3
import uuid
import json
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='iHome.fifo')

sresobj = SmartHomeResponseHandler()
sresobj.addLightAppliance(manufacturer="iHome",name="Bedroom Light",description="Light",device_id="endpoint-ihome-light1")
sresobj.addLightAppliance(manufacturer="iHome",name="Living Room Light",description="Light",device_id="endpoint-ihome-light2")
sresobj.addSwitchAppliance(manufacturer="iHome",name="Bedroom Fan",description="Fan",device_id="endpoint-ihome-fan")

def form_message(device, operation, extravalue="") :
    timestamp = str(uuid.uuid4())
    message = {}
    message['device'] = device
    message['operation'] = operation
    message['extraValue'] = extravalue
    message['timestamp'] = timestamp
    return str(json.dumps(message))

def lambda_handler(event, context):
    sreqobj = SmartHomeRequestHandler(event)
    otoken = sreqobj.get_authentication_details()["token"]
    print(sreqobj.get_request_name())
    if sreqobj.get_request_name() == "Discover":
        return sresobj.buildDiscoveryResponse()
    elif sreqobj.get_request_name() == "TurnOn":
        if sreqobj.get_endpoint_id() == "endpoint-ihome-light1":
            print("turn on light1")
            queue.send_message(MessageBody=form_message("LIGHT1", 'on'),MessageGroupId='messageGroup1')
            return sresobj.buildSwitchResponse(endpoint="endpoint-ihome-light1",powerState="ON",oauthToken=otoken)
        if sreqobj.get_endpoint_id() == "endpoint-ihome-light2":
            print("turn on light2")
            queue.send_message(MessageBody=form_message("LIGHT2", 'on'),MessageGroupId='messageGroup1')
            return sresobj.buildSwitchResponse(endpoint="endpoint-ihome-light2",powerState="ON",oauthToken=otoken)
        elif sreqobj.get_endpoint_id() == "endpoint-ihome-fan":
            print("turn on fan")
            queue.send_message(MessageBody=form_message("FAN", 'on'),MessageGroupId='messageGroup1')
            return sresobj.buildSwitchResponse(endpoint="endpoint-ihome-fan",powerState="ON",oauthToken=otoken)
    elif sreqobj.get_request_name() == "TurnOff":
        if sreqobj.get_endpoint_id() == "endpoint-ihome-light1":
            print("turn off light1")
            queue.send_message(MessageBody=form_message("LIGHT1", 'off'),MessageGroupId='messageGroup1')
            return sresobj.buildSwitchResponse(endpoint="endpoint-ihome-light1",powerState="OFF",oauthToken=otoken)
        if sreqobj.get_endpoint_id() == "endpoint-ihome-light2":
            print("turn off light2")
            queue.send_message(MessageBody=form_message("LIGHT2", 'off'),MessageGroupId='messageGroup1')
            return sresobj.buildSwitchResponse(endpoint="endpoint-ihome-light2",powerState="OFF",oauthToken=otoken)
        elif sreqobj.get_endpoint_id() == "endpoint-ihome-fan":
            print("turn on fan")
            queue.send_message(MessageBody=form_message("FAN", 'off'),MessageGroupId='messageGroup1')
            return sresobj.buildSwitchResponse(endpoint="endpoint-ihome-fan",powerState="OFF",oauthToken=otoken)

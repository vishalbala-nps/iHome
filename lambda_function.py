import json
from alexa_smarthome import SmartHomeResponseHandler,SmartHomeRequestHandler
import boto3
import uuid
import json
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='AlexaSmarthome.fifo')

sresobj = SmartHomeResponseHandler()
sresobj.addThermostat(manufacturer="LG",name="AC",description="AC",device_id="endpoint-lg-ac",targetSetpoint=True,thermostatMode=True,supportedModes=["COOL","OFF"],power=True,temperatureRetrievable=False,powerRetrievable=False)

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
    print(sreqobj.get_request_name())
    if sreqobj.get_request_name() == "Discover":
        return sresobj.buildDiscoveryResponse()
    elif sreqobj.get_request_name() == "SetThermostatMode":
        if sreqobj.get_thermostat_mode() == "COOL":
            print("turn on ac")
            queue.send_message(MessageBody=form_message("AC", 'on'),MessageGroupId='messageGroup1')
            return sresobj.buildTemperatureResponse(endpoint="endpoint-lg-ac",powerState="ON",targetSetpointValue=26,mode="COOL")
        else:
            print("turn off ac")
            queue.send_message(MessageBody=form_message("AC", 'off'),MessageGroupId='messageGroup1')
            return sresobj.buildTemperatureResponse(endpoint="endpoint-lg-ac",powerState="OFF")
    elif sreqobj.get_request_name() == "SetTargetTemperature":
        print("turn off ac")
        queue.send_message(MessageBody=form_message("AC", 'temperature', float(sreqobj.get_thermostat_temperature()["targetSetpoint"]["value"])),MessageGroupId='messageGroup1')
        return sresobj.buildTemperatureResponse(endpoint="endpoint-lg-ac",powerState="ON",targetSetpointValue=float(sreqobj.get_thermostat_temperature()["targetSetpoint"]["value"]),mode="COOL")

import uuid
import secrets
import time

class SmartHomeResponseHandler():
    def __init__(self,appliances=[]):
        self.appliances = appliances
        self.capabilities = {}
    def getAppliances(self):
        return self.appliances
    #Adding Appliances
    def addSwitchAppliance(self,manufacturer,name,description,device_id=str(uuid.uuid4()),cookie={},retrievable=True,proactivelyReported=False):
        self.capabilities[device_id] = ["power"]
        self.appliances.append({
            "endpointId": device_id,
            "manufacturerName": manufacturer,
            "friendlyName": name,
            "description": description,
            "displayCategories": ["SWITCH"],
            "cookie":cookie,
            "capabilities": [
                {
                    "type": "AlexaInterface",
                    "interface": "Alexa",
                    "version": "3"
                },
                {
                    "interface": "Alexa.PowerController",
                    "version": "3",
                    "type": "AlexaInterface",
                    "properties": {
                        "supported": [{
                            "name": "powerState"
                        }],
                    "proactivelyReported": proactivelyReported,
                    "retrievable": retrievable,
                    }
                }
            ]
        })
    def addLightAppliance(self,manufacturer,name,description,device_id=str(uuid.uuid4()),cookie={},colorControl=False,brightnessControl=False,powerRetrievable=True,powerProactivelyReported=False,colorRetrievable=True,colorProactivelyReported=False,brightnessRetrievable=True,brightnessProactivelyReported=False):
        icaps = ["power"]
        devcaps = [
            {
                "type": "AlexaInterface",
                "interface": "Alexa",
                "version": "3"
            },
            {
                "interface": "Alexa.PowerController",
                "version": "3",
                "type": "AlexaInterface",
                "properties": {
                    "supported": [{
                        "name": "powerState"
                    }],
                "proactivelyReported":powerProactivelyReported,
                "retrievable": powerRetrievable,
                }
            }
        ]
        if colorControl:
            icaps.append("color")
            devcaps.append(
                {
                  "type": "AlexaInterface",
                  "interface": "Alexa.ColorController",
                  "version": "3",
                  "properties": {
                    "supported": [
                      {
                        "name": "color"
                      }
                    ],
                    "proactivelyReported": colorProactivelyReported,
                    "retrievable": colorRetrievable
                  }
                }
            )
        if brightnessControl:
            icaps.append("brightness")
            devcaps.append(
                {
                  "type": "AlexaInterface",
                  "interface": "Alexa.BrightnessController",
                  "version": "3",
                  "properties": {
                    "supported": [
                      {
                        "name": "brightness"
                      }
                    ],
                    "proactivelyReported": brightnessProactivelyReported,
                    "retrievable": brightnessRetrievable
                  }
                }
              )
        self.capabilities[device_id] = icaps
        self.appliances.append({
            "endpointId": device_id,
            "manufacturerName": manufacturer,
            "friendlyName": name,
            "description": description,
            "displayCategories": ["LIGHT"],
            "cookie":cookie,
            "capabilities": devcaps
        })
        
    def addMediaAppliance(self,manufacturer,name,description,displayDeviceAs,device_id=str(uuid.uuid4()),cookie={},volumeControl=False,step=False,channelControl=False,powerRetrievable=True,powerProactivelyReported=False,channelRetrievable=True,channelProactivelyReported=False,volumeRetrievable=True,volumeProactivelyReported=False):
        dcats = []
        icaps = ["power"]
        dcats.append(displayDeviceAs)
        devcaps = [
            {
                "type": "AlexaInterface",
                "interface": "Alexa",
                "version": "3"
            },
            {
                "interface": "Alexa.PowerController",
                "version": "3",
                "type": "AlexaInterface",
                "properties": {
                    "supported": [{
                        "name": "powerState"
                    }],
                "proactivelyReported":powerProactivelyReported,
                "retrievable": powerRetrievable
                }
            }
        ]
        if volumeControl:
            if step:
                devcaps.append({
                    "type": "AlexaInterface",
                     "interface": "Alexa.StepSpeaker",
                     "version": "3"
                })
            else:
                icaps.append("volume")
                devcaps.append(
                    {
                      "type": "AlexaInterface",
                      "interface": "Alexa.Speaker",
                      "version": "3",
                      "properties": {
                        "supported": [{ "name": "volume" },{ "name": "muted" }],
                        "retrievable": volumeRetrievable,
                        "proactivelyReported": volumeProactivelyReported
                      }
                    }
                )
        if channelControl:
            icaps.append("channel")
            devcaps.append(
                {
                  "type": "AlexaInterface",
                  "interface": "Alexa.ChannelController",
                  "version": "3",
                  "properties": {
                    "supported": [
                      {
                        "name": "channel"
                      }
                    ],
                    "proactivelyReported": channelProactivelyReported,
                    "retrievable": channelRetrievable
                  }
                }
            )
        self.capabilities[device_id] = icaps
        self.appliances.append({
            "endpointId": device_id,
            "manufacturerName": manufacturer,
            "friendlyName": name,
            "description": description,
            "displayCategories": dcats,
            "cookie":cookie,
            "capabilities": devcaps
        })
    def addThermostat(self,manufacturer,name,description,device_id=str(uuid.uuid4()),cookie={},targetSetpoint=False,lowerSetpoint=False,upperSetpoint=False,thermostatMode=False,supportedModes=[],supportsScheduling=False,proactivelyReported=False,retrievable=True,power=False,powerProactivelyReported=False,powerRetrievable=True,temperature=False,temperatureProactivelyReported=False,temperatureRetrievable=True):
        supports = []
        icaps = []
        if targetSetpoint:
          icaps.append("targetSetpoint")
          supports.append({"name":"targetSetpoint"})
        if lowerSetpoint:
          icaps.append("lowerSetpoint")
          supports.append({"name":"lowerSetpoint"})
        if upperSetpoint:
          icaps.append("upperSetpoint")
          supports.append({"name":"upperSetpoint"})
        if thermostatMode:
          icaps.append("thermostatMode")
          supports.append({"name":"thermostatMode"})
        devcaps = [
            {
                "type": "AlexaInterface",
                "interface": "Alexa",
                "version": "3"
            },
            {
              "type": "AlexaInterface",
              "interface": "Alexa.ThermostatController",
              "version": "3",
              "properties": {
                "supported": supports,
                "proactivelyReported": proactivelyReported,
                "retrievable": retrievable
              },
              "configuration": {
                "supportedModes": supportedModes,
                "supportsScheduling": supportsScheduling
              }
            }
        ]
        if temperature:
          icaps.append("temperature")
          devcaps.append(
            {
              "type": "AlexaInterface",
              "interface": "Alexa.TemperatureSensor",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "temperature"
                  }
                ],
                "proactivelyReported": temperatureProactivelyReported,
                "retrievable": temperatureRetrievable
                }
            }
          )
        if power:
          icaps.append("power")
          devcaps.append(
            {
                "interface": "Alexa.PowerController",
                "version": "3",
                "type": "AlexaInterface",
                "properties": {
                    "supported": [{
                        "name": "powerState"
                    }],
                "proactivelyReported":powerProactivelyReported,
                "retrievable": powerRetrievable
                }
            }
          )
        self.capabilities[device_id] = icaps
        self.appliances.append({
            "endpointId": device_id,
            "manufacturerName": manufacturer,
            "friendlyName": name,
            "description": description,
            "displayCategories": ["THERMOSTAT", "TEMPERATURE_SENSOR"],
            "cookie":cookie,
            "capabilities": devcaps
        })
      
    #Response building
    def buildDiscoveryResponse(self):
        return {
            "event": {
                "header": {
                  "namespace": "Alexa.Discovery",
                  "name": "Discover.Response",
                  "payloadVersion": "3",
                  "messageId":str(uuid.uuid4())
                },
                "payload": {
                    "endpoints": self.appliances
                }
            }
        }
    def buildSwitchResponse(self,endpoint,powerState,oauthToken,uncertaintyInMilliseconds=50,response_type="Response"):
        tstamp = time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(None))
        return {
              "event": {
                "header": {
                  "namespace": "Alexa",
                  "name": response_type,
                  "messageId": str(uuid.uuid4()),
                  "correlationToken": secrets.token_hex(128),
                  "payloadVersion": "3"
                },
                "endpoint": {
                  "scope": oauthToken,
                  "endpointId": endpoint
                },
                "payload": {}
              },
              "context": {
                "properties": [
                  {
                    "namespace": "Alexa.PowerController",
                    "name": "powerState",
                    "value": powerState,
                    "timeOfSample": tstamp,
                    "uncertaintyInMilliseconds": uncertaintyInMilliseconds
                  }
                ]
              }
            }
    def buildLightResponse(self,endpoint,powerState,oauthToken,brightnessValue=0,colorValue={},uncertaintyInMilliseconds=50,response_type="Response"):
      tstamp = time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(None))
      dprops = [
        {
          "namespace": "Alexa.PowerController",
          "name": "powerState",
          "value": powerState,
          "timeOfSample": tstamp,
          "uncertaintyInMilliseconds": uncertaintyInMilliseconds
        }
      ]
      if "brightness" in self.capabilities[endpoint]:
        dprops.append({
          "namespace": "Alexa.BrightnessController",
          "name": "brightness",
          "value": brightnessValue,
          "timeOfSample": tstamp,
          "uncertaintyInMilliseconds": uncertaintyInMilliseconds
        })
      if "color" in self.capabilities[endpoint]:
        dprops.append({
          "namespace": "Alexa.ColorController",
          "name": "color",
          "value": colorValue,
          "timeOfSample": tstamp,
          "uncertaintyInMilliseconds": uncertaintyInMilliseconds 
        })
      return {
              "event": {
                "header": {
                  "namespace": "Alexa",
                  "name": response_type,
                  "messageId": str(uuid.uuid4()),
                  "correlationToken": secrets.token_hex(128),
                  "payloadVersion": "3"
                },
                "endpoint": {
                  "scope": oauthToken,
                  "endpointId": endpoint
                },
                "payload": {}
              },
              "context": {
                "properties": dprops
              }
            }
    def buildMediaResponse(self,endpoint,oauthToken,mute=False,volume=0,powerState="ON",channel=False,channelNum=0,uncertaintyInMilliseconds=50,response_type="Response"):
        tstamp = time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(None))
        dpjson = [
          {
            "namespace": "Alexa.PowerController",
            "name": "powerState",
            "value": powerState,
            "timeOfSample": tstamp,
            "uncertaintyInMilliseconds": uncertaintyInMilliseconds
          }
        ]
        if "volume" in self.capabilities[endpoint]:
            dpjson = [
              {
                "namespace": "Alexa.Speaker",
                "name": "volume",
                "value": volume,
                "timeOfSample": tstamp,
                "uncertaintyInMilliseconds": 0
              },
              {
                "namespace": "Alexa.Speaker",
                "name": "muted",
                "value": mute,
                "timeOfSample": tstamp,
                "uncertaintyInMilliseconds": 0
              }
            ]
        if "channel" in self.capabilities[endpoint]:
          dpjson.append({
            "namespace": "Alexa.ChannelController",
            "name": "channel",
            "value": channelNum,
            "timeOfSample": tstamp,
            "uncertaintyInMilliseconds": 0     
          })
        return {
          "event": {
            "header": {
              "namespace": "Alexa",
              "name": "Response",
              "messageId": str(uuid.uuid4()),
              "correlationToken": secrets.token_hex(128),
              "payloadVersion": "3"
            },
            "endpoint":{
              "endpointId": endpoint
            },
            "payload": {}
          },
          "context": {
            "properties": dpjson
          }
        }
    def buildTemperatureResponse(self,endpoint,powerState="OFF",targetSetpointValue=0,targetSetpointUnit="CELSIUS",lowerSetpointValue=0,lowerSetpointUnit="CELSIUS",upperSetpointValue=0,upperSetpointUnit="CELSIUS",mode="",roomTemp=0,roomTempUnits="CELSIUS",uncertaintyInMilliseconds=50,response_type="Response"):
        tstamp = time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(None))
        propslist = []
        if "power" in self.capabilities[endpoint]:
          propslist.append(
            {
              "namespace": "Alexa.PowerController",
              "name": "powerState",
              "value": powerState,
              "timeOfSample": tstamp,
              "uncertaintyInMilliseconds": uncertaintyInMilliseconds
            } 
          )
        if "targetSetpoint" in self.capabilities[endpoint]:
          propslist.append(
            {
              "namespace": "Alexa.TemperatureSensor",
              "name": "targetSetpoint",
              "value": {
                "value": targetSetpointValue,
                "scale": targetSetpointUnit
              },
              "timeOfSample": tstamp,
              "uncertaintyInMilliseconds": uncertaintyInMilliseconds
            } 
          )
        if "lowerSetpoint" in self.capabilities[endpoint]:
          propslist.append(
            {
              "namespace": "Alexa.TemperatureSensor",
              "name": "lowerSetpoint",
              "value": {
                "value": lowerSetpointValue,
                "scale": lowerSetpointUnit
              },
              "timeOfSample": tstamp,
              "uncertaintyInMilliseconds": uncertaintyInMilliseconds
            } 
          )
        if "upperSetpoint" in self.capabilities[endpoint]:
          propslist.append(
            {
              "namespace": "Alexa.TemperatureSensor",
              "name": "upperSetpoint",
              "value": {
                "value": upperSetpointValue,
                "scale": upperSetpointUnit
              },
              "timeOfSample": tstamp,
              "uncertaintyInMilliseconds": uncertaintyInMilliseconds
            } 
          )
        if "thermostatMode" in self.capabilities[endpoint]:
          propslist.append(
            {
              "namespace": "Alexa.ThermostatController",
              "name": "thermostatMode",
              "value": mode,
              "timeOfSample": tstamp,
              "uncertaintyInMilliseconds": uncertaintyInMilliseconds
            }
          )
        if "temperature" in self.capabilities[endpoint]:
          propslist.append(
            {
              "namespace": "Alexa.TemperatureSensor",
              "name": "temperature",
              "value": {
                "value": roomTemp,
                "scale": roomTempUnits
              },
              "timeOfSample": tstamp,
              "uncertaintyInMilliseconds": uncertaintyInMilliseconds
            } 
          )
        return {
              "event": {
                "header": {
                  "namespace": "Alexa",
                  "name": response_type,
                  "messageId": str(uuid.uuid4()),
                  "correlationToken": secrets.token_hex(128),
                  "payloadVersion": "3"
                },
                "endpoint": {
                  "endpointId": endpoint
                },
                "payload": {}
              },
              "context": {
                "properties": propslist
              }
            }
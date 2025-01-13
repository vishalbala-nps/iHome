class SmartHomeRequestHandler():
    def __init__(self,aws_request):
        self.aws_req = aws_request
    def get_request_name(self):
        return self.aws_req["directive"]["header"]["name"]
    def get_request_namespace(self):
        return self.aws_req["directive"]["header"]["namespace"]
    def get_endpoint_id(self):
        try:
            return self.aws_req["directive"]["endpoint"]["endpointId"]
        except:
            return ""
    def get_brightness(self):
        try:
            return self.aws_req["directive"]["payload"]["brightness"]
        except:
            return None
    def get_color(self):
        try:
            return self.aws_req["directive"]["payload"]["color"]
        except:
            return {}
    def get_channel_details(self):
        fjson = {"channel":{},"channelMetadata":{}}
        try:
            fjson["channel"] = self.aws_req["directive"]["payload"]["channel"]
            fjson["channelMetadata"] = self.aws_req["directive"]["payload"]["channelMetadata"]
        except:
            pass
        return fjson
    def get_volume(self):
        try:
            return self.aws_req["directive"]["payload"]["volume"]
        except:
            return ""
    def get_volume_steps(self):
        try:
            return self.aws_req["directive"]["payload"]["volumeSteps"]
        except:
            return ""
    def get_volume_mute(self):
        try:
            return self.aws_req["directive"]["payload"]["mute"]
        except:
            return None
    def get_thermostat_temperature(self):
        fres = {"targetSetpoint":{},"lowerSetpoint":{},"upperSetpoint":{},"schedule":{}}
        try:
            fres["targetSetpoint"] = self.aws_req["directive"]["payload"]["targetSetpoint"]
        except:
            pass
        try:
            fres["lowerSetpoint"] = self.aws_req["directive"]["payload"]["lowerSetpoint"]
        except:
            pass
        try:
            fres["upperSetpoint"] = self.aws_req["directive"]["payload"]["upperSetpoint"]
        except:
            pass
        try:
            fres["schedule"] = self.aws_req["directive"]["payload"]["schedule"]
        except:
            pass
        return fres
    def get_thermostat_temperature_adjust(self):
        try:
            return self.aws_req["directive"]["payload"]["targetSetpointDelta"]
        except:
            return {}
    def get_thermostat_mode(self):
        try:
            return self.aws_req["directive"]["payload"]["thermostatMode"]["value"]
        except:
            return ""
    def get_authentication_details(self):
        try:
            return self.aws_req["directive"]["payload"]["scope"]
        except:
            try:
                return self.aws_req["directive"]["endpoint"]["scope"]
            except:
               return {}
import json


class Feedback:
    def __init__(self, purpose="info", username="sysMsg", payload="testMsg", consum=''):

        self.purpose = purpose
        self.username = username
        if(consum==''):
            consum=f"[{username}]"
        self.consum=consum
        if(payload == None):
            payload=""
        self.payload = payload

    def get_data(self):
        return {
            "purpose": self.purpose,
            "username": self.username,
            "payload": self.payload,
            "consumers":self.consum
        }

    def __str__(self):
        return json.dumps(self.get_data())

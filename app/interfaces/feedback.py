class Feedback:
    def __init__(self, purpose="info", username="sysMsg", payload="testMsg"):
        self.purpose = purpose
        self.username = username
        self.payload = payload

    def get_data(self):
        return {
            "purpose": self.purpose,
            "username": self.username,
            "payload": self.payload
        }

    def __str__(self):
        return str(self.get_data())

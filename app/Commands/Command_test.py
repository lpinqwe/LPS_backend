import json

from app.interfaces.command import Command
from app.interfaces.feedback import Feedback


class MoveCommand(Command):

    def __init__(self, body_json):
        print("ComamndTest")

        self.body_json = body_json

    def execute(self) -> Feedback:
        command_entity = json.loads(self.body_json)
        pur = command_entity['purpose']
        user = command_entity['username']
        payload = self.body_json
        feed = Feedback(payload=payload, username=user, purpose=pur)
        print(f"RECIEVE TO COMMAND {self.body_json}")
        return feed

import json

from app.interfaces.command import Command
from app.interfaces.feedback import Feedback
from app.utils.DBReader import DBReader


class online(Command):

    def __init__(self, body_json):
        self.body_json = body_json
        self.connection = DBReader()

    def execute(self) -> Feedback:
        try:
            command_entity = json.loads(self.body_json)
            pur = command_entity['purpose']
            user = command_entity['username']
            sql = "UPDATE public.userinfo " \
                  "SET lastonline = null " \
                  f"WHERE userid = '{user}';"
            resp = self.connection.read_data(sql)
            return Feedback(payload=resp, purpose=pur, username=user)
        except Exception as e:
            print(e)

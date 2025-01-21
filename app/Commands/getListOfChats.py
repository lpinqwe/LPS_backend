

import json
from app.interfaces.command import Command
from app.utils.DBReader import DBReader

class getListOfChats(Command):
    """
    purpose: "getListOfChats"
    username: String
    должно вернуть список чатов (их id)
    """
    def __init__(self, body_json):
        self.body_json = body_json
        self.connection = DBReader()

    def execute(self):
        try:
            print("getListOfChats func")
            command_entity = json.loads(self.body_json)
            pur = command_entity['purpose']
            username = command_entity['username']

            sql = """
            SELECT chatid 
            FROM public.chatandusers 
            WHERE userid = %s;
            """
            params = [username]
            chats = self.connection.read_data(sql, params)

            customFeedback = {
                "username": username,
                "consumers": f"[{username}]",
                "purpose": pur,
                "chats": [f"{chat[0]}" for chat in chats]  # Получение только ID чатов
            }

            return json.dumps(customFeedback)

        except Exception as e:
            print(e)

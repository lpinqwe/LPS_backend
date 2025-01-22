import json
from datetime import datetime
from app.interfaces.command import Command
from app.utils.DBReader import DBReader

class getChatData(Command):
    def __init__(self, body_json):
        self.body_json = body_json
        self.connection = DBReader()

    def execute(self):
        try:
            print("getChatData func")
            command_entity = json.loads(self.body_json)
            pur = command_entity['purpose']
            username = command_entity['username']
            chatId = command_entity['chatId']

            sql_users = """
                SELECT userid 
                FROM chatandusers 
                WHERE chatid = %s;
            """
            users = self.connection.read_data(sql_users, [chatId])

            sql_messages = """
                SELECT msgid, text, typemsg, load, fromUID, isdeleted, isRead, sendtime, isAnswer
                FROM messages 
                WHERE chatid = %s 
                ORDER BY sendtime DESC 
                LIMIT 50;
            """
            messages = self.connection.read_data(sql_messages, [chatId])

            sql_chat_settings = """
                SELECT chatID, chatName, chatImage, chatSettings 
                FROM chatinfo 
                WHERE chatid = %s;
            """
            chat_settings = self.connection.read_data(sql_chat_settings, [chatId])

            self.messages_ = {
                "purpose": pur,
                "chatId": chatId,
                "consumers": [username],
                "chatName": chat_settings[0][1],
                "chatSettings": chat_settings[0][3],
                "users": [row[0] for row in users],
                "messages": [
                    {
                        "msgid": msg[0],
                        "text": msg[1],
                        "typemsg": msg[2],
                        "load": msg[3],
                        "isdeleted": msg[5],
                        "isRead": msg[6],
                        "isAnswer": msg[8],
                        "sendTime": msg[7].strftime("%Y-%m-%d %H:%M:%S") if isinstance(msg[7], datetime) else msg[7],
                        "sender": msg[4]
                    } for msg in messages
                ]
            }
            data = self.messages_
            json_data = json.dumps(data, default=self.custom_serializer, ensure_ascii=False, indent=4)

            return json_data

        except Exception as e:
            print(e)

    def custom_serializer(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if obj is None:
            return ""
        raise TypeError(f"Type {type(obj)} not serializable")

import json

from app.interfaces.command import Command
from app.utils.DBReader import DBReader


class getChatData(Command):
    """
    purpose: "getChatData"
    username: String
    chatId: String
    """

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

            # Получение информации о пользователях в чате
            sql_users = """
                SELECT userid 
                FROM chatandusers 
                WHERE chatid = %s;
            """
            users = self.connection.read_data(sql_users, [chatId])

            # Получение последних 50 сообщений из чата
            sql_messages = """
                SELECT msgid, text,typemsg,load,fromUID,isdeleted,isRead, sendtime,isAnswer
                FROM messages 
                WHERE chatid = %s 
                ORDER BY sendtime DESC 
                LIMIT 50;
            """
            messages = self.connection.read_data(sql_messages, [chatId])

            # Получение настроек чата
            sql_chat_settings = """
                SELECT chatID, chatName,chatImage,chatSettings 
                FROM chatinfo 
                WHERE chatid = %s;
            """
            chat_settings = self.connection.read_data(sql_chat_settings, [chatId])

            data = {
                "purpose": pur,
                "chatId": chatId,
                "chatName": chat_settings[0][1],
                "chatSettings": chat_settings[0][3],
                "users": list(users[0]),
                "messages": [
                    {"msgid": msg[0], "text": msg[1], "typemsg": msg[2], "load": msg[3], "isdeleted": msg[5], "isRead": msg[6],
                     "isAnswer": msg[8], "sendtime": msg[7], "fromuid": msg[4]} for msg in
                    messages]
            }

            return data

        except Exception as e:
            print(e)

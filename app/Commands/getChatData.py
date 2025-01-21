import json
from datetime import datetime

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

            self.messages_ = {
                "purpose": pur,
                "chatId": chatId,
                "consumers": [username],
                "chatName": chat_settings[0][1],
                "chatSettings": chat_settings[0][3],
                "users": [row[0] for row in users],
                "messages": [
                    {"msgid": msg[0], "text": msg[1], "typemsg": msg[2], "load": msg[3], "isdeleted": msg[5],
                     "isRead": msg[6],
                     "isAnswer": msg[8], "sendtime": msg[7], "sender": msg[4]} for msg in
                    messages]
            }
            data = self.messages_
            json_data = json.dumps(data, default=self.custom_serializer, ensure_ascii=False, indent=4)

            return json_data

        except Exception as e:
            print(e)

    def custom_serializer(self,obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Преобразуем datetime в строку формата ISO 8601
        if obj is None:
            return ""  # Заменяем None на пустую строку
        raise TypeError(f"Type {type(obj)} not serializable")
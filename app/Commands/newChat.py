import json
from datetime import datetime

from app.interfaces.command import Command
from app.interfaces.feedback import Feedback
from app.utils.DBReader import DBReader


class newChat(Command):

    def __init__(self, body_json):
        self.body_json = body_json
        self.connection = DBReader()

    def custom_serializer(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Преобразуем datetime в строку формата ISO 8601
        if obj is None:
            return ""  # Заменяем None на пустую строку
        raise TypeError(f"Type {type(obj)} not serializable")

    def execute(self):
        try:
            command_entity = json.loads(self.body_json)
            pur = command_entity['purpose']
            user = command_entity['username']
            chatId = command_entity['chatId']
            chatName = command_entity['chatName']
            consumers = command_entity['consumers']
            # access_token = command_entity['access_token']

            if user not in consumers:
                return Feedback(payload="sth gone bad (not user in consumers)", purpose=pur, username=user)

            if not isinstance(consumers, list):
                return Feedback(payload="sth gone bad (str_list должен быть списком строк)", purpose=pur, username=user)

            chatInfo = f'insert into public.chatinfo (chatID , chatName) values (\'{chatId}\',\'{chatName}\');'
            try:

                self.connection.read_data(chatInfo)

                print("here2")

                [self.connection.read_data(
                    'insert into public.chatandusers (chatID,userID) values (%s,%s);', params=(chatId, cons))
                    for cons
                    in consumers]
                print("here1")

            except Exception as e:
                print(e)
            """
            purpose: "newChat"
            chatId:String  
            chatName:String
            consumers:список людей из чата
            """

            customFeedback = {"purpose": "newChat",
                              "chatId": chatId,
                              "chatName": chatName,
                              "consumers": consumers
                              }
            json_data = json.dumps(customFeedback, default=self.custom_serializer, ensure_ascii=False, indent=4)

            return json_data
        except Exception as e:
            print("here3")
            print(e)

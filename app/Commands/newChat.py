import json

from app.interfaces.command import Command
from app.interfaces.feedback import Feedback
from app.utils.DBReader import DBReader


class newChat(Command):

    def __init__(self, body_json):
        self.body_json = body_json
        self.connection = DBReader()

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

            chatInfo = f'insert into public.chatinfo (chatID , chatName) values ({chatId},\'{chatName}\');'
            try:

                self.connection.read_data(chatInfo)
            except Exception as e:
                print(e)
            try:

                [self.connection.read_data(
                    f'insert into public.chatandusers (chatID,userID) values (%s,%s);', params=(chatId, cons))
                    for cons
                    in consumers]

            except Exception as e:
                print(e)
            """
            purpose: "newChat"
            chatId:String  
            chatName:String
            consumers:список людей из чата
            """

            customFeedback = f'{"purpose":"newChat","chatID":"{chatId}","chatName":"{chatName}","consumers":"{consumers}"}'

            return customFeedback
        except Exception as e:
            print(e)

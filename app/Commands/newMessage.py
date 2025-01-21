import json

from app.interfaces.command import Command
from app.utils.DBReader import DBReader


class newMessage(Command):
    """
    purpose: "newMessage"
    messageId:String
    chatId:String
    text:String
    username:String
    IsAnswer:String
    isDeleted:ZonedDateTime
    isRead:ZonedDateTime
    sendTime:ZonedDateTime
    должно добавить сообщение в базу
    """
    def __init__(self, body_json):
        self.body_json = body_json
        self.connection = DBReader()

    def execute(self):
        try:
            print("NewMessage func")
            command_entity = json.loads(self.body_json)
            pur = command_entity['purpose']
            user = command_entity['username']
            messageId=command_entity['messageId']
            chatId=command_entity['chatId'] #########
            text=command_entity['text']
            IsAnswer=command_entity['isAnswer']
            isDeleted=command_entity['isDeleted']
            isRead=command_entity['isRead']
            sendTime=command_entity['sendTime']

            sql = """
            INSERT INTO public.messages (msgid, chatid, text, isdeleted, isread, sendtime, isanswer, fromuid) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = [messageId,chatId,text,isDeleted,isRead,sendTime,IsAnswer,user]
            for i in range(len(params)):
                if params[i] == '':
                    params[i] = None


            self.connection.read_data(sql,params)

            sql = """
            select userid 
            from public.chatandusers 
            where chatid = %s;            
            """
            params=[chatId]
            tmp=self.connection.read_data(sql,params)
            print(tmp)

            data = {
                "purpose": {pur},
                "consumers": {list(tmp[0])},  
                "messageId": {messageId},
                "chatId": {chatId},
                "text": {text},
                "username":{user},
                "isAnswer": {IsAnswer},
                "isDeleted": {isDeleted},  
                "isRead": {isRead}, 
                "sendTime": {sendTime}
                }
            return json.dumps(data)
        except Exception as e:
            print(e)

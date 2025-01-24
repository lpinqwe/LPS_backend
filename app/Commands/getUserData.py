import json

from app.interfaces.command import Command
from app.interfaces.feedback import Feedback
from app.utils.DBReader import DBReader


class getUserData(Command):
    def __init__(self, body_json):
        self.body_json = body_json
        self.connection = DBReader()

    def execute(self):
        try:
            command_entity = json.loads(self.body_json)
            pur = command_entity['purpose']
            user = command_entity['username']
            userToGet = command_entity['userToGet']
            sql = f'select userid,username,nickname,phonenumber,userkey,useremail,isdeleted,birthdate from userinfo ' \
                  f'where userid = \'{userToGet}\';'
            # this version od time
            tmp = list(self.connection.read_data(sql)[0])
            print(tmp)
            for i in range((len(tmp))):
                if tmp[i] == None:
                    tmp[i] = ""
            customfeedback = {
                "purpose": pur,
                "consumers": [user],
                "username": tmp[0],
                "nickname": tmp[2],
                "phoneNumber": tmp[3],
                "userkey": tmp[4],
                "usermail": tmp[5],
                "isdeleted": tmp[6],
                "dateOfBirth": tmp[7]
            }

            print(customfeedback)
            # return json.dumps(customfeedback)
            return Feedback.from_map(customfeedback)
        except Exception as e:
            print(e)

import json

from app.interfaces.command import Command
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

            sql = f'select userid,username,nickname,phonenumber,userkey,useremail,isdeleted,birthdate from userinfo ' \
                  f'where userid = \'{user}\';'

            tmp = self.connection.read_data(sql)[0]
            print(tmp)
            customfeedback = "{" + f'''
                    "userid": "{tmp[0]}",
                    "username": "{tmp[1]}",
                    "nickname": "{tmp[2]}",
                    "phonenumber": "{tmp[3]}",
                    "userkey": "{tmp[4]}",
                    "usermail": "{tmp[5]}",
                    "isdeleted": "{tmp[6]}",
                    "birthdate": "{tmp[7]}"
            ''' + "}"

            print(customfeedback)
            return customfeedback
        except Exception as e:
            print(e)

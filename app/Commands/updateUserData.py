#getListOfChats
#updateUserData --> specialConsumers

import json
from datetime import datetime
from app.interfaces.command import Command
from app.interfaces.feedback import Feedback
from app.utils.DBReader import DBReader


class updateUserData(Command):
    """
    purpose: "updateUserData"
    username: String
    nickname: String
    phoneNumber: String
    email: String
    lastOnline: ZonedDateTime
    dateOfBirth: LocalDate
    """

    def __init__(self, body_json):
        self.body_json = body_json
        self.connection = DBReader()

    def execute(self):
        try:
            print("updateUserData func")
            command_entity = json.loads(self.body_json)
            pur = command_entity['purpose']
            username = command_entity['username']
            nickname = command_entity['nickname']#
            phoneNumber = command_entity['phoneNumber']#
            #email = command_entity['email']
            #lastOnline = command_entity['lastOnline']
            dateOfBirth = command_entity['dateOfBirth']

            sql = """
            UPDATE public.userinfo
            SET nickname=%s, phoneNumber=%s, birthdate=%s
            WHERE userID=%s;
            """
            params = [nickname, phoneNumber,  dateOfBirth, username]
            for i in range(len(params)):
                if params[i] == '':
                    params[i] = None
            self.connection.read_data(sql, params)

            sql = "select distinct userid from chatandusers where chatid in (select chatid from chatandusers where userid = %s)"
            tmp = self.connection.read_data(sql, [username])
            print("ans="+str(tmp))



            data = {
                "purpose": pur,
                "username": username,
                "nickname": nickname,
                "consumers": [row[0] for row in tmp],
                "phoneNumber": phoneNumber,
                "dateOfBirth": dateOfBirth
            }

            return Feedback.from_map(data)

        except Exception as e:
            print(e)

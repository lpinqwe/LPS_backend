import json

from app.Commands.Command_test import MoveCommand
from app.Commands.getChatData import getChatData
from app.Commands.getListOfChats import getListOfChats
from app.Commands.getUserData import getUserData
from app.Commands.newChat import newChat
from app.Commands.newMessage import newMessage
from app.Commands.offline import offline
from app.Commands.online import online
from app.Commands.singUpLogIn import SignUpLogIn
from app.Commands.updateUserData import updateUserData


class Factory:
    def lifeCheck(self):
        return [True, "factory"]

    def __init__(self):
        # purpose -> is type of command
        self.commands = {
            'updateUserData': updateUserData,
            'newMessage': newMessage,
            'getListOfChats': getListOfChats,
            'SignUpLogIn': SignUpLogIn,
            'readMessage': MoveCommand,
            'offline': offline,
            'online': online,
            'newChat': newChat,
            'getUserData': getUserData,
            'getChatData':getChatData
            # etc
            # Добавьте сюда другие команды по мере необходимости
        }

    def execute_command(self, cmd):
        try:
            command_entity = json.loads(cmd)
            cmd_type = command_entity['purpose']
            command_class = self.commands.get(cmd_type)
            if command_class is None:
                raise ValueError(f"Unknown command type: {cmd_type}")

            if not callable(command_class):
                raise TypeError(f"Command {cmd_type} is not callable.")

            command = command_class(cmd)
            return command.execute()
        except Exception as e:
            print(cmd)
            print("sthGoneWrong")
            print(e)
            raise e

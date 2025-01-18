import json

from app.Commands.Command_test import MoveCommand
class Factory:
    def lifeCheck(self):
        return [True,"factory"]
    def __init__(self):
        # purpose -> is type of command
        self.commands = {
            'updateUserData': MoveCommand,
            'newMessage': MoveCommand,
            'newChat': MoveCommand,
            'addUserToChat': MoveCommand,
            'deleteMessage': MoveCommand,
            'readMessage': MoveCommand,
            # etc
            # Добавьте сюда другие команды по мере необходимости
        }
    def execute_command(self,cmd):
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
        except:
            print("sthGoneWrong")
            None

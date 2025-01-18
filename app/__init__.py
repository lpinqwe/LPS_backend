import threading

from flask import Flask, jsonify

from app.utils.BrockerManager import BrockerM
from app.utils.factory import Factory

factory = Factory()
broker = BrockerM(factory)

objList = [factory, broker]

app = Flask(__name__)
from app import routes

thread = None


def runAll():
    thread_msg = threading.Thread(target=broker.start_consuming())
    thread_msg.start()

runAll()


@app.route('/health', methods=['GET'])
def lifecheck():
    resp = ""
    for obj in objList:
        respond = obj.lifeCheck()
        if respond[0] != True:
            resp += str(respond)

    if resp == "":
        return "ok", 200
    return jsonify({"status": "error", "details": resp}), 500

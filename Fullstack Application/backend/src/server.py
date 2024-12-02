import signal
from json import dumps
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from error import InputError, AccessError
import config
from private import mysqlpath
from user import user
from task import task
from conference import conference
from message import message
from volunteerlist import volunteerlist
from attendance import attendance
from flask_mail import Mail, Message

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


# init DB
from models import DB

APP = Flask(__name__, static_url_path='/static/')
CORS(APP)
APP.config['SECRET_KEY']='IJH2sdU29#dD83901ASkt*x2hdjk!a%B^3*'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
APP.config['SQLALCHEMY_DATABASE_URI'] = mysqlpath
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
DB.init_app(APP)

APP.register_error_handler(Exception, defaultHandler)
APP.register_blueprint(user)
APP.register_blueprint(conference)
APP.register_blueprint(task)
APP.register_blueprint(message)
APP.register_blueprint(volunteerlist)
APP.register_blueprint(attendance)

APP.config['MAIL_SERVER'] = 'smtp.gmail.com'  

APP.config['MAIL_PORT'] = 587
APP.config['MAIL_USE_TLS'] = True
APP.config['MAIL_USE_SSL'] = False
APP.config['MAIL_USERNAME'] = 'bestgroupconference@gmail.com'
APP.config['MAIL_PASSWORD'] = 'khix cepi mamn njqu'
APP.config['MAIL_DEFAULT_SENDER'] = 'bestgroupconference@gmail.com'

mail = Mail(APP)

with APP.app_context():
    DB.create_all()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)
    APP.run(port=config.port)
    print('Server Commenced!')
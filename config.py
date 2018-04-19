DEBUG = True
import os

SECRET_KEY = os.urandom(24)

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'flask_bbs'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'test'

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True
#MAIL_USE_SSL: default
#False
# MAIL_DEBUG =
MAIL_USERNAME = ""
MAIL_PASSWORD= ""
MAIL_DEFAULT_SENDER= ""
# MAIL_MAX_EMAILS: defaultNone
# MAIL_SUPPRESS_SEND: defaultapp.testing
# MAIL_ASCII_ATTACHMENTS: defaultFalse

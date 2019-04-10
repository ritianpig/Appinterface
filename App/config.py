import os

# MySQL connection
dev_db = 'mysql+pymysql://root:123456@127.0.0.1:3306/appinterface?charset=utf8'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
Debug = False

from flask import Flask
from flask_cors import CORS
from pymysql import install_as_MySQLdb

install_as_MySQLdb()

app=Flask(__name__)
app.config.from_object("config")
CORS(app,support_credentials=True)

from app import view,model

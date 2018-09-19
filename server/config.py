import os

basedir=os.path.abspath(os.path.dirname(__file__))
DEBUG=True
CSRF_ENABLED=True
SECRET_KEY="songxy"
SECURITY_PASSWORD_SALT  = 'my_precious_two'

#数据库配置路径
SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS=False

#邮件配置
MAIL_DEBUG = True
MAIL_SUPPRESS_SEND=False
MAIL_SERVER='smtp.qq.com'
MAIL_PROT=25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = '1821908096@qq.com'
MAIL_PASSWORD = 'votpntlokywiefce'
MAIL_DEFAULT_SENDER="1821908096@qq.com"

#公网地址
LINK_URI="http://119.29.19.43"
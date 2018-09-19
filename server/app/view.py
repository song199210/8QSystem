from flask import jsonify,request
from app import app
from .views import UserView,FilmView,JokeView,MusicView

user_blue=UserView.UserBlue
film_blue=FilmView.FilmBlue
joke_blue=JokeView.JokeBlue
music_blue=MusicView.MusicBlue

app.register_blueprint(user_blue,url_prefix="/login")
app.register_blueprint(film_blue,url_prefix="/film")
app.register_blueprint(joke_blue,url_prefix="/joke")
app.register_blueprint(music_blue,url_prefix="/music")

@app.route("/",methods=['GET'])
def index():
    print("测试")
    return "测试成功"

@app.errorhandler(404)
def page_not_fount(error):
    resData=dict(flag="error",msg="404不存在")
    return jsonify(resData)

@app.errorhandler(500)
def page_error_500(error):
    resData=dict(flag="error",msg="500服务器内部错误")
    return jsonify(resData)

@app.before_first_request
def before_first_request():
    print("before first request started")
    print(request.url)

@app.before_request
def before_request():
    print("before request started")
    print(request.url)

@app.after_request
def after_request(response):
    print("after request finished")
    print(request.url)
    response.headers['key']="value"
    return response

@app.teardown_request
def teardown_request(exception):
    print("teardown request")
    print(request.url)
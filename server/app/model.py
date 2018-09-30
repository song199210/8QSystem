from app import init_db
from app.models import Users,Films,Jokes,Musics,Menus,Proxyip

UsersM=Users.UserModels
FilmsM=Films.FilmModels
JokesM=Jokes.JokeModels
MusicsM=Musics.MusicModels
MenusM=Menus.MenuModels
ProxyIpM=Proxyip.ProxyIPModels
session=init_db.session
create_db=init_db.init_db

create_db()
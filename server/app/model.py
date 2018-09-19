from app import init_db
from app.models import Users,Films,Jokes,Musics,Menus

UsersM=Users.UserModels
FilmsM=Films.FilmModels
JokesM=Jokes.JokeModels
MusicsM=Musics.MusicModels
MenusM=Menus.MenuModels

session=init_db.session
create_db=init_db.init_db

create_db()
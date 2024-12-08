from manage import *
from blueprints.artists import artists
from blueprints.albums import albums
from blueprints.genres import genres

app.register_blueprint(artists, url_prefix='/api/artists')
app.register_blueprint(albums, url_prefix='/api/albums')
app.register_blueprint(genres, url_prefix='/api/genres')

if __name__ == '__main__':
    # запускаем сервер
    app.run(debug=True, port=8000)

from manage import *
from blueprints.artists import artists
from blueprints.albums import albums

# заменяем список обработчиков на регистрацию двух блупринтов с префиксами
app.register_blueprint(artists, url_prefix='/api/artists')
app.register_blueprint(albums, url_prefix='/api/albums')

if __name__ == '__main__':
    # запускаем сервер
    app.run(debug=True, port=8000)

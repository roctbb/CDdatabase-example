from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cd_collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# модель - описывает таблицу в базе
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


# создаем базу данных, если ее пока нет
with app.app_context():
    db.create_all()


# презенторы - функции, которые представляют модели в виде словарей
def present_artist(artist):
    return {
        'id': artist.id,
        'name': artist.name
    }


# ендпоинты - реагируют на запросы пользователей

# получение списка исполнителей
@app.route('/api/artists', methods=['GET'])
def get_all_artists():
    # забираем всех исполнителей из базы
    artists = Artist.query.all()
    # превращаем их в список словарей
    artist_descriptions = [present_artist(artist) for artist in artists]
    # возвращаем ответ в виде списка словарей и типом application/json
    return jsonify(artist_descriptions)


# получение исполнителя по id
@app.route('/api/artists/<int:id>', methods=['GET'])
def get_artist_by_id(id):
    # ищем в базе запись с указанным id - вернется объект типа Artist или None
    artist = Artist.query.filter_by(id=id).first()

    # если исполнитель не найден - сообщаем об этом пользователю
    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    # если исполнитель найден - отправляем словарь с его описанием
    return jsonify(present_artist(artist))


# добавление исполнителя
@app.route('/api/artists', methods=['POST'])
def add_artist():
    # получаем данные, отправленные пользователем в формате словаря
    data = request.get_json()

    # проверяем
    if data is None:
        return jsonify({'reason': 'Invalid JSON format'}), 400

    # получаем имя исполнителя, отправленное пользователем (или None, если его нет)
    name = data.get('name')

    # валидация запроса - проверяем, что передано имя, и артист с таким именем отсутствует в базе
    if not name:
        return jsonify({'reason': 'Missing name'}), 400
    # проверяем, нет ли в базе исполнителя с таким именем
    if Artist.query.filter_by(name=name).first():
        return jsonify({'reason': 'Artist already exists'}), 400

    # если валидация пройдена - создаем новый объект
    artist = Artist(name=name)
    # добавляем объект в ORM
    db.session.add(artist)
    # сохраняем изменения
    db.session.commit()
    # возвращаем описание нового артиста с его id
    return jsonify(present_artist(artist))


# PATCH - изменение выбранных свойств исполнителя, в нашем случае - имени
@app.route('/api/artists/<int:id>', methods=['PATCH'])
def update_artist(id):
    # получаем новое имя
    data = request.get_json()
    name = data.get('name')

    # если имя не передано - возвращаем ошибку
    if not name:
        return jsonify({'reason': 'Missing name'}), 400

    # находим артиста в базе по id и возвращаем ошибку, если его нет
    artist = Artist.query.filter_by(id=id).first()

    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    # если имя поменяло
    if name != artist.name and Artist.query.filter_by(name=name).first():
        return jsonify({'reason': 'Artist already exists'}), 400

    artist.name = name
    # сохраняем изменения
    db.session.commit()

    # возвращаем описание артиста с изменениями
    return jsonify(present_artist(artist))


# запрос типа DELETE - удаление артиста из базы
@app.route('/api/artists/<int:id>', methods=['DELETE'])
def delete_artist(id):
    # находим артиста в базе и возвращаем ошибку, если его нет
    artist = Artist.query.filter_by(id=id).first()

    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404
    # удаляем запись
    db.session.delete(artist)
    # сохраняем изменения
    db.session.commit()

    # возвращаем успешный ответ
    return jsonify({'success': True})


if __name__ == '__main__':
    # запускаем сервер
    app.run(debug=True)

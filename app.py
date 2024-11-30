from docutils.nodes import description
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cd_collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# добавили description
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

# добавили description
def present_artist(artist):
    return {
        'id': artist.id,
        'name': artist.name,
        'description': artist.description
    }

# не меняется
@app.route('/api/artists', methods=['GET'])
def get_all_artists():
    artists = Artist.query.all()
    artist_descriptions = [present_artist(artist) for artist in artists]
    return jsonify(artist_descriptions)


# не меняется
@app.route('/api/artists/<int:id>', methods=['GET'])
def get_artist_by_id(id):
    artist = Artist.query.filter_by(id=id).first()

    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    return jsonify(present_artist(artist))


# добавляем указание описания
@app.route('/api/artists', methods=['POST'])
def add_artist():
    data = request.get_json()

    name = data.get('name')
    # получаем описание
    description = data.get('description')

    # описание не проверяем - оно может быть и пустым
    if not name:
        return jsonify({'reason': 'Missing name'}), 400
    if Artist.query.filter_by(name=name).first():
        return jsonify({'reason': 'Artist already exists'}), 400

    # добавляем описание к новому исполнителю
    artist = Artist(name=name, description=description)
    db.session.add(artist)
    db.session.commit()

    return jsonify(present_artist(artist))


# добавляем возможность поменять описание
@app.route('/api/artists/<int:id>', methods=['PATCH'])
def update_artist(id):
    data = request.get_json()

    artist = Artist.query.filter_by(id=id).first()
    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    # логика PATCH подразумевает, что можно передавть не все свойства, а только те, что нужно поменять.
    # для изменения объекта целиком используется метод PUT
    # если передали имя - проводим проверки для имени
    if 'name' in data:
        name = data.get('name')

        if not name:
            return jsonify({'reason': 'Missing name'}), 400

        if name != artist.name and Artist.query.filter_by(name=name).first():
            return jsonify({'reason': 'Artist already exists'}), 400

        artist.name = name

    # если передали любое описание - меняем описание
    if 'description' in data:
        description = data.get('description')
        artist.description = description

    db.session.commit()

    # возвращаем описание артиста с изменениями
    return jsonify(present_artist(artist))


# не меняется
@app.route('/api/artists/<int:id>', methods=['DELETE'])
def delete_artist(id):
    artist = Artist.query.filter_by(id=id).first()

    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    db.session.delete(artist)
    db.session.commit()

    return jsonify({'success': True})


if __name__ == '__main__':
    # запускаем сервер
    app.run(debug=True)

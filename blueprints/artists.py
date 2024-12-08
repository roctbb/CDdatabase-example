from flask import Blueprint, jsonify, request
from models import *
from presenters import *

artists = Blueprint('artists', __name__)

@artists.route('', methods=['GET'])
def get_all_artists():
    artists = Artist.query.all()
    artist_descriptions = [present_artist(artist) for artist in artists]
    return jsonify(artist_descriptions)


@artists.route('/<int:id>', methods=['GET'])
def get_artist_by_id(id):
    artist = Artist.query.filter_by(id=id).first()

    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    return jsonify(present_artist(artist))


@artists.route('', methods=['POST'])
def add_artist():
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'reason': 'Missing name'}), 400
    if Artist.query.filter_by(name=name).first():
        return jsonify({'reason': 'Artist already exists'}), 400

    artist = Artist(name=name, description=description)
    db.session.add(artist)
    db.session.commit()

    return jsonify(present_artist(artist))


@artists.route('/<int:id>', methods=['PATCH'])
def update_artist(id):
    data = request.get_json()

    artist = Artist.query.filter_by(id=id).first()
    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    if 'name' in data:
        name = data.get('name')

        if not name:
            return jsonify({'reason': 'Missing name'}), 400

        if name != artist.name and Artist.query.filter_by(name=name).first():
            return jsonify({'reason': 'Artist already exists'}), 400

        artist.name = name

    if 'description' in data:
        description = data.get('description')
        artist.description = description

    db.session.commit()

    return jsonify(present_artist(artist))


@artists.route('/<int:id>', methods=['DELETE'])
def delete_artist(id):
    artist = Artist.query.filter_by(id=id).first()

    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    db.session.delete(artist)
    db.session.commit()

    return jsonify({'success': True})


@artists.route('/<int:id>/albums', methods=['GET'])
def get_artist_albums(id):
    artist = Artist.query.filter_by(id=id).first()
    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    return jsonify([present_album(album) for album in artist.albums])


@artists.route('/<int:id>/albums', methods=['POST'])
def add_album(id):
    artist = Artist.query.filter_by(id=id).first()
    if not artist:
        return jsonify({'reason': 'Artist not found'}), 404

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'reason': 'Missing name or description'}), 400

    # не забываем указать id исполнителя
    album = Album(name=name, description=description, artist_id=id)
    db.session.add(album)
    db.session.commit()

    return jsonify(present_album(album))
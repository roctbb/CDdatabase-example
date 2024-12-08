from flask import Blueprint, request, jsonify
from models import *
from presenters import *

albums = Blueprint('albums', __name__)


@albums.route('/<int:album_id>', methods=['PATCH'])
def update_album(album_id):
    album = Album.query.filter_by(id=album_id).first()
    if not album:
        return jsonify({'reason': 'Album not found'}), 404

    data = request.get_json()

    if 'name' in data:
        name = data.get('name')

        if not name:
            return jsonify({'reason': 'Missing name'}), 400

        album.name = name

    if 'description' in data:
        description = data.get('description')

        if not description:
            return jsonify({'reason': 'Missing description'}), 400

        album.description = description

    if 'genres' in data:
        requested_genres = data.get('genres')

        # проверяем, что жанры передали списком
        if not isinstance(requested_genres, list):
            return jsonify({'reason': 'Genres must be a list'}), 400

        # проверяем, что все жанры есть в базе
        genres = []
        for requested_genre in requested_genres:
            genre = Genre.query.filter_by(name=requested_genre).first()

            if not genre:
                return jsonify({'reason': f'Genre {requested_genre} not found'}), 400

            genres.append(genre)
        # изменяем список жанров
        album.genres = genres

    db.session.commit()

    return jsonify(present_album(album))


@albums.route('/<int:album_id>', methods=['DELETE'])
def delete_album(album_id):
    album = Album.query.filter_by(id=album_id).first()
    if not album:
        return jsonify({'reason': 'Album not found'}), 404

    db.session.delete(album)
    db.session.commit()

    return jsonify({'success': True})

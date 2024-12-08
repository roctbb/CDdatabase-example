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
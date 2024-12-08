from flask import Blueprint, request, jsonify
from models import *
from presenters import *

genres = Blueprint('genres', __name__)

@genres.route('', methods=['GET'])
def get_genres_list():
    genres = Genre.query.all()
    return jsonify([present_genre(genre) for genre in genres])


@genres.route('', methods=['POST'])
def add_genre():
    data = request.get_json()

    name = data.get('name')
    if not name:
        return jsonify({'reason': 'Missing name'}), 400

    if Genre.query.filter_by(name=name).first():
        return jsonify({'reason': 'Genre already exists'}), 400

    genre = Genre(name=name)
    db.session.add(genre)
    db.session.commit()

    return jsonify(present_genre(genre))

@genres.route('/<genre_title>', methods=['DELETE'])
def delete_genre(genre_title):
    genre = Genre.query.filter_by(name=genre_title).first()

    if not genre:
        return jsonify({'reason': 'Genre not found'}), 404

    db.session.delete(genre)
    db.session.commit()

    return jsonify({'success': True})
from manage import db

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)


album_genre = db.Table('album_genre',
                       db.Column('album_id', db.Integer, db.ForeignKey('album.id', ondelete='CASCADE'), primary_key=True),
                       db.Column('genre_id', db.Integer, db.ForeignKey('genre.id', ondelete='CASCADE'), primary_key=True)
                       )


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete='CASCADE'), nullable=False)

    artist = db.relationship('Artist', backref=db.backref('albums'))
    genres = db.relationship('Genre', secondary=album_genre, backref=db.backref('albums'))


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

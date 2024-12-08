def present_album(album):
    return {
        'id': album.id,
        'name': album.name,
        'description': album.description,
        "genres": [present_genre(genre) for genre in album.genres]
    }


def present_artist(artist):
    return {
        'id': artist.id,
        'name': artist.name,
        'description': artist.description,
    }

def present_genre(genre):
    return genre.name
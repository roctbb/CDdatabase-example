def present_album(album):
    return {
        'id': album.id,
        'name': album.name,
        'description': album.description,
    }


def present_artist(artist):
    return {
        'id': artist.id,
        'name': artist.name,
        'description': artist.description,
    }
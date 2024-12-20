import requests

API_URL = 'http://127.0.0.1:8000/api/'


def create_artist_request(name, description=None):
    data = {'name': name}
    if description:
        data['description'] = description
    return requests.post(
        API_URL + 'artists',
        json=data
    )


def get_artist_request(artist_id):
    return requests.get(API_URL + 'artists/' + str(artist_id))


def get_all_artists_request():
    return requests.get(API_URL + 'artists')


def delete_artist_request(artist_id):
    return requests.delete(API_URL + 'artists/' + str(artist_id))


def update_artist_request(artist_id, name=None, description=None):
    data = {}

    if name:
        data['name'] = name
    if description:
        data['description'] = description

    return requests.patch(
        API_URL + 'artists/' + str(artist_id),
        json=data
    )


def create_album_request(name, description, artist_id, genres=[]):
    return requests.post(
        API_URL + 'artists/' + str(artist_id) + '/albums',
        json={'name': name, 'description': description, 'genres': genres}
    )


def update_album_request(album_id, name=None, description=None, genres=[]):
    return requests.patch(
        API_URL + 'albums/' + str(album_id),
        json={'name': name, 'description': description, 'genres': genres}
    )

def get_albums_request(artist_id):
    return requests.get(
        API_URL + 'artists/' + str(artist_id) + '/albums'
    )


def delete_album_request(album_id):
    return requests.delete(
        API_URL + 'albums/' + str(album_id)
    )


def add_genre_request(name):
    return requests.post(
        API_URL + 'genres',
        json={'name': name}
    )


def get_genres_request():
    return requests.get(API_URL + 'genres')


def delete_genre_request(name):
    return requests.delete(
        API_URL + 'genres/' + str(name)
    )


def run_artists_api_tests():
    # проверяем жанры
    genre_response = add_genre_request('Jazz')
    assert genre_response.status_code == 200

    genre_response = add_genre_request('Rock')
    assert genre_response.status_code == 200

    genre_response = get_genres_request()
    assert genre_response.status_code == 200
    assert len(genre_response.json()) == 2

    print("Genres creation tests passed!")

    # проверяем создание артистов
    artist_response1 = create_artist_request('Test Artist1', 'Description1')
    artist_response2 = create_artist_request('Test Artist2', 'Description2')
    assert artist_response1.status_code == 200
    assert artist_response2.status_code == 200
    print("Artist creation tests passed!")

    # сохраняем id новых артистов
    artist_id1 = artist_response1.json().get('id')
    artist_id2 = artist_response2.json().get('id')

    # проверяем, что нельзя создать артиста с уже использованным именем
    artist_response = create_artist_request('Test Artist1')
    assert artist_response.status_code == 400
    print("Artist name uniqueness tests passed!")

    # проверяем, что можно получить артиста по id
    artist_response = get_artist_request(artist_id1)
    assert artist_response.status_code == 200
    assert artist_response.json().get('name') == 'Test Artist1'
    assert artist_response.json().get('description') == 'Description1'
    print("Get artist by id tests passed!")

    # проверяем, что можно изменить артиста
    artist_response = update_artist_request(artist_id1, 'Test Artist1', 'Updated Description1')
    assert artist_response.status_code == 200
    print("Update artist tests passed!")

    # проверяем возможность добавления и удаления альбомов
    album_response = create_album_request('Test Album1', 'Description1', artist_id1, ['Rock'])
    assert album_response.status_code == 200

    album_response = create_album_request('Test Album2', 'Description2', artist_id1, ['Jazz'])
    assert album_response.status_code == 200

    album_response = get_albums_request(artist_id1)
    assert album_response.status_code == 200
    assert len(album_response.json()) == 2

    album_id1 = album_response.json()[0].get('id')
    album_id2 = album_response.json()[1].get('id')

    print('Albums creation tests passed!')


    album_response = update_album_request(
        album_id1,
        name='Updated Album1',
        description='Updated Description1',
        genres=['Rock', 'Jazz'])

    assert album_response.status_code == 200

    album_response = get_albums_request(artist_id1)
    assert len(set(album_response.json()[0]['genres']).intersection(['Rock', 'Jazz'])) == 2
    print('Update album tests passed!')


    album_response = delete_album_request(album_id1)
    assert album_response.status_code == 200
    album_response = delete_album_request(album_id2)
    assert album_response.status_code == 200

    album_response = get_albums_request(artist_id1)
    assert album_response.status_code == 200
    assert len(album_response.json()) == 0

    print("Album deletion tests passed!")

    # проверяем, что нельзя задать артисту уже использованное имя при обновлении
    artist_response = update_artist_request(artist_id1, 'Test Artist2')
    assert artist_response.status_code == 400
    print("Update artist name uniqueness tests passed!")

    # проверяем, что можно изменить артиста
    artist_response = update_artist_request(artist_id1, 'Test Artist3', 'Another Description')
    assert artist_response.status_code == 200
    print("Update artist tests passed!")

    # проверяем, что можно получить список артистов
    artist_response = get_all_artists_request()
    assert artist_response.status_code == 200
    assert len(artist_response.json()) == 2
    print("Get all artists tests passed!")

    # проверяем, что можно удалить артиста
    artist_response = delete_artist_request(artist_id1)
    assert artist_response.status_code == 200
    print("Delete artist tests passed!")

    artist_response = get_artist_request(artist_id1)
    assert artist_response.status_code == 404
    print("Delete artist confirmation tests passed!")

    # удаляем второго артиста из базы
    artist_response = delete_artist_request(artist_id2)
    assert artist_response.status_code == 200
    print("Artist deletion passed!")

    # удаляем жанры
    delete_genre_request('Rock')
    delete_genre_request('Jazz')

    genre_response = get_genres_request()
    assert len(genre_response.json()) == 0
    print("Genres deletion passed!")


if __name__ == '__main__':
    run_artists_api_tests()

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import DB_api


DB_PATH = 'sqlite:///albums.sqlite3'


def pretty_name(name):
    """
    Обрабатывает имя артиста и заменяет
    разделители слов пробелами.
    Делает первые буквы слов заглавными.
    Например pink-floyd заменит на Pink Floyd.
    """
    separator = ' '
    for symbol in name:
        if not symbol.isalpha():
            separator = symbol
    return name.replace(separator, ' ').title()


def valid_data(data: dict):
    """
    Проверяет, что год - число.
    Если число, взвращает True,
    иначе False.
    """

    try:
        int(data['year'])
    except ValueError:
        return False
    else:
        return True


def correct_end(number):
    """
    Вазвращает слово "альбом" с корректным
    окончанием в зависимости от количества
    """

    end = str(number)[-1]
    if end == '1':
        return 'альбом'
    elif end in ['2', '3', '4']:
        return 'альбома'
    else:
        return 'альбомов'


@route('/albums/<artist>')
def show_albums(artist):
    """
    Возвращает количество альбомов и
    список альбомов по имени артиста.
    При отсутствии артиста в базе
    отображает ошибку 404 и
    выводит соответствующее сообщение.
    """

    artist = pretty_name(artist)
    number, albums = DB_api.get_albums_by_artist(artist, DB_PATH)
    if number == 0:
        return HTTPError(404, f'Альбомов {artist} в базе данных нет.')
    else:
        return f'В базе данных {number} {correct_end(number)} исполнителя {artist}.\n{albums}'


@route('/albums/', method='POST')
def receive_album_data():
    """
    Обрабатывает полученные от клиента данные
    об альбоме.
    Проверяет полноту данных и валидность года,
    если есть несоответствия выводит соответствующее
    сообщение.
    Если альбом уже есть в БД выводит ошибку 409.
    """
    album_data = {
        'year': request.forms.get('year'),
        'artist': request.forms.get('artist'),
        'genre': request.forms.get('genre'),
        'album': request.forms.get('album')
    }

    if None in album_data.values():
        return 'Введены не все данные. Проверьте year, artist, genre, album.'
    if not valid_data(album_data):
        return 'Введите корректную дату'
    else:
        if DB_api.add_new_album(album_data, DB_PATH):
            return HTTPError(409, f'Альбом {album_data["album"]} артиста {album_data["artist"]} уже есть в БД.')
        else:
            return 'Данные альбома добавлены в базу данных'


if __name__ == '__main__':
    run(host='localhost', port=8080)




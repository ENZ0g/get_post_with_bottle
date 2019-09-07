import sqlalchemy as a
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Album(Base):
    __tablename__ = 'Album'

    id = a.Column(a.INTEGER,
                  primary_key=True,
                  autoincrement=True)
    year = a.Column(a.INTEGER)
    artist = a.Column(a.TEXT)
    genre = a.Column(a.TEXT)
    album = a.Column(a.TEXT)


def db_connect(path):
    """
    Создает подключение к БД
    """
    engine = a.create_engine(path)
    Base.metadata.create_all(engine)
    Sessions = sessionmaker(engine)
    return Sessions()


def get_albums_by_artist(artist, db_path):
    """
    Возврвщает количество и
    список альбомов по имени артиста
    Список заворачивается в html-тэг <ol>
    """
    session = db_connect(db_path)
    query = session.query(Album).filter(Album.artist == artist).all()
    return len(query), query_to_ol(query)


def query_to_ol(query):
    """
    Обрабатывет запрос к БД и заворачивает его
    в html-тэг <ol>
    """
    ol = '<ol>'
    for i in [x.album for x in query]:
        ol += '<li>' + str(i) + '</li>'
    return ol + '</ol>'


def add_new_album(data: dict, db_path):
    """
    Добавляет в БД информацию о новом альбоме.
    Предварительно проверяет наличие альбома в БД.
    Если он уже есть, добавления не происходит -
    функция возвращает True (альбом есть).
    Иначе, добавляет данные в БД и возвращает False.
    """

    session = db_connect(db_path)
    query = session.query(Album).filter(Album.artist == data['artist'].title(),
                                        Album.album == data['album'].title()).count()
    if query:
        return True
    else:
        album = Album(
            year=data['year'],
            artist=data['artist'].title(),
            genre=data['genre'].capitalize(),
            album=data['album'].title()
        )

        session.add(album)
        session.commit()
        return False

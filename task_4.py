"""
TODO

1. Pull data for the first movie ("A New Hope") and save in DB.

2. Replace the data for each endpoint listed in the JSON object and insert
that data into database table

For example - "A new hope" movie has following resource endpoints -

- characters 15
- planets  7
- starships   10
- vehicles  5
- species  40


"""

from multiprocessing.pool import ThreadPool

from resources.films import Film   # resource model
from models.datamodels.films import Film_  # pydantic model
from models.datamodels.characters import Character_

from dal.db_conn_helper import get_db_conn
from dal.dml import insert_resource
from utils.fetch_data import hit_url, fetch_data
from utils.timing import timeit


@timeit
def store_characters():
    characters = film_data.characters
    characters_data = []

    char_columns = [
        "name",
        "height",
        "mass",
        "hair_color"
    ]

    for character in characters:
        response = hit_url(character)
        char = response.json()
        char = Character_(**char)
        char_values = [
            char.name,
            char.height,
            char.mass,
            char.hair_color
        ]

        char_id = int(character.split("/")[-2])
        result = insert_resource(
            "characters",
            "char_id",
            char_id,
            char_columns,
            char_values
        )
        characters_data.append(char)
    return characters_data


if __name__ == "__main__":
    data = Film().get_sample_data(id_=1)
    film_data = Film_(**data)

    # create DB connection
    conn = get_db_conn()

    film_columns = [
        "title",
        "opening_crawl",
        "director",
        "producer",
        "release_date",
        "created",
        "edited",
        "url",
    ]

    film_values = [
        film_data.title,
        film_data.opening_crawl,
        film_data.director,
        film_data.producer,
        film_data.release_date,
        film_data.created.strftime("%y-%m-%d"),
        film_data.edited.strftime("%y-%m-%d"),
        film_data.url,
    ]

    # DB operation
    result = insert_resource(
        "film", "film_id", film_data.episode_id, film_columns, film_values
    )

    characters = film_data.characters
    pool = ThreadPool(5)
    results = pool.map(fetch_data, characters)

    breakpoint()

    # TODO
    # capture all characters
    # film_data.characters
    # only values will change
    # column list can be once created and re-used

    character_data = store_characters()

    # TODO
    # capture all planets
    # film_data.planets
    # only values will change
    # column list can be once created and re-used












import json
import os
import requests
import requests_cache
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from datetime import timedelta
from typing import List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RESULT_FILE_PATH = "../web-app/src/lib/assets/cities.json"


# was only an idea during dev, now using main_json.py to not be dependent on a db
def get_env_var(key: str, default: Optional[str] = None) -> str:
    value = os.getenv(key)
    if not value and default is None:
        raise EnvironmentError(f"Environment variable {key} is required but not set.")
    return value


class City:
    def __init__(self, full_name: str):
        name, *description = full_name.split(", ")
        self.name: str = name
        self.description: Optional[str] = description[0] if description else None
        self.lat: Optional[float] = None
        self.lon: Optional[float] = None


def main() -> None:
    cities: List[City] = parse_cities_from_sheet()
    add_coordinates(cities)
    write_to_json(cities)
    # insert_into_db(cities)


def parse_cities_from_sheet() -> List[City]:
    workbook: Workbook = load_workbook(filename="05-staedte.xlsx")
    sheet: Worksheet = workbook["Städte"]

    return [
        City(full_name=full_name_row.value)
        for (full_name_row, postal_code_row) in sheet["G8:H2066"]
    ]


def add_coordinates(cities: List[City]) -> None:
    session: requests_cache.CachedSession = requests_cache.CachedSession(
        cache_name="cache", expire_after=timedelta(weeks=1)
    )

    for city in cities:
        city.lat, city.lon = get_lat_lon(city, session)


def get_lat_lon(
    city: City, session: requests_cache.CachedSession
) -> Tuple[Optional[float], Optional[float]]:
    url: str = "https://nominatim.openstreetmap.org/search"
    params: dict[str, str] = {
        "city": city.name,
        "country": "de",
        "format": "json",
    }
    headers: dict[str, str] = {"User-Agent": "visit-german-cities"}

    try:
        response: requests.Response = session.get(url, params=params, headers=headers)
        response.raise_for_status()
        results: list[dict[str, str]] = response.json()

        if results:
            logger.info(f"Fetched lat/lon for: {city.name}")
            return float(results[0]["lat"]), float(results[0]["lon"])
        else:
            logger.warning(f"Failed fetch for: {city.name}")
            return None, None
    except requests.RequestException as e:
        logger.error(f"Error fetching data for city {city.name}: {e}")
        return None, None


def write_to_json(cities: List[City]) -> None:
    cities = list(
        map(
            lambda city: {
                "name": city.name,
                "description": city.description,
                "lat": city.lat,
                "lon": city.lon,
            },
            cities,
        )
    )
    with open(RESULT_FILE_PATH, "w") as fp:
        json.dump(cities, fp)

    logger.info(f"Created file at: {RESULT_FILE_PATH}")


# was only an idea during dev, now using main_json.py to not be dependent on a db
def insert_into_db(cities: List[City]) -> None:
    headers: dict[str, str] = {
        "Authorization": f"Bearer {get_env_var('TURSO_AUTH_TOKEN')}",
        "Content-Type": "application/json",
    }

    sql_delete_table: str = "DROP TABLE IF EXISTS cities"

    sql_create_table: str = """
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        lat REAL,
        lon REAL
    )
    """

    sql_insert_city: str = """
    INSERT INTO cities (name, description, lat, lon)
    VALUES (?, ?, ?, ?)
    """

    sql_add_index: str = "CREATE INDEX idx_column_name ON cities(name);"

    query: dict[str, list[dict]] = {
        "requests": [
            {"type": "execute", "stmt": {"sql": sql_delete_table}},
            {"type": "execute", "stmt": {"sql": sql_create_table}},
            *[
                {
                    "type": "execute",
                    "stmt": {
                        "sql": sql_insert_city,
                        "args": [
                            {"type": "text", "value": city.name},
                            (
                                {"type": "text", "value": city.description}
                                if city.description
                                else {"type": "null"}
                            ),
                            (
                                {"type": "float", "value": city.lat}
                                if city.lat
                                else {"type": "null"}
                            ),
                            (
                                {"type": "float", "value": city.lon}
                                if city.lon
                                else {"type": "null"}
                            ),
                        ],
                    },
                }
                for city in cities
            ],
            {"type": "execute", "stmt": {"sql": sql_add_index}},
            {"type": "close"},
        ]
    }

    try:
        response: requests.Response = requests.post(
            url=get_env_var("TURSO_DATABASE_URL"),
            headers=headers,
            json=query,
        )

        response.raise_for_status()

    except requests.RequestException as e:
        logger.error(f"An error occurred while inserting into the database: {e}")


if __name__ == "__main__":
    main()

import os
import requests
import requests_cache
from openpyxl import load_workbook
from datetime import timedelta


def main():
    cities_with_postal = get_cities_with_postal()
    cities_with_postal_and_coords = get_cities_with_postal_and_coords(
        cities_with_postal
    )
    insert_into_db(cities_with_postal_and_coords)


def insert_into_db(cities):

    headers = {
        "Authorization": f"Bearer {os.getenv("TURSO_AUTH_TOKEN")}",
        "Content-Type": "application/json",
    }

    query = {
        "requests": [
            {"type": "execute", "stmt": {"sql": "DROP TABLE IF EXISTS cities"}},
            {
                "type": "execute",
                "stmt": {
                    "sql": """CREATE TABLE IF NOT EXISTS cities (
                         name TEXT NOT NULL,
                         description TEXT,
                         postal_code INTEGER NOT NULL,
                         latitude REAL NOT NULL,
                         longitude REAL NOT NULL
                         )
                        """
                },
            },
            *[
                {
                    "type": "execute",
                    "stmt": {
                        "sql": "INSERT INTO cities (name, description, postal_code, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
                        "args": [
                            {
                                "type": "text",
                                "value": name,
                            },
                            (
                                {
                                    "type": "text",
                                    "value": description,
                                }
                                if description
                                else {
                                    "type": "null",
                                }
                            ),
                            {
                                "type": "integer",
                                "value": str(postal_code),
                            },
                            {
                                "type": "float",
                                "value": float(lat),
                            },
                            {
                                "type": "float",
                                "value": float(lon),
                            },
                        ],
                    },
                }
                for (name, description, postal_code, lat, lon) in cities
            ],
            {"type": "close"},
        ]
    }

    try:
        response = requests.post(
            url=os.getenv("TURSO_DATABASE_URL"),
            headers=headers,
            json=query,
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def get_cities_with_postal():
    workbook = load_workbook(filename="05-staedte.xlsx")
    sheet = workbook["Städte"]

    return [
        (
            parts[0],
            parts[1] if len(parts) > 1 else None,
            postal_code.value,
        )
        for (name, postal_code) in sheet["G8:H2066"]
        if (parts := name.value.split(", "))
    ]


def get_cities_with_postal_and_coords(cities):
    session = requests_cache.CachedSession("cache", expire_after=timedelta(weeks=1))

    cities = [
        (name, description, postal_code, *get_lat_long(postal_code, session))
        for (name, description, postal_code) in cities
    ]

    # remove filtering and manually add lat/lon
    return [item for item in cities if item[3] and item[4]]


def get_lat_long(postal_code, session):
    url = f"https://nominatim.openstreetmap.org/search"
    params = {
        "postalcode": postal_code,
        "country": "de",
        "format": "json",
    }
    headers = {"User-Agent": "visit-german-cities"}

    try:
        response = session.get(url, params=params, headers=headers)
        response.raise_for_status()
        results = response.json()

        if results:
            return results[0]["lat"], results[0]["lon"]
        else:
            return None, None
    except requests.RequestException as e:
        print(f"Error fetching data for postal code {postal_code}: {e}")
        return None, None


if __name__ == "__main__":
    main()

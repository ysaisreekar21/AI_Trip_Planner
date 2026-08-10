import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def geocode_destination(destination: str) -> dict:
    """Convert a destination name into geographic information."""

    params = {
        "name": destination,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = requests.get(
        GEOCODING_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        raise ValueError(f"Destination not found: {destination}")

    result = data["results"][0]

    return {
        "name": result.get("name"),
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "country": result.get("country"),
        "country_code": result.get("country_code"),
        "timezone": result.get("timezone"),
    }
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude: float, longitude: float) -> dict:
    """Get hourly weather forecast for a location."""

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
            "temperature_2m,"
            "precipitation_probability,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "forecast_days": 7,
        "timezone": "auto",
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timezone": data.get("timezone"),
        "hourly": data.get("hourly"),
    }

AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def get_air_quality(latitude: float, longitude: float) -> dict:
    """Get hourly air quality forecast for a location."""

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "pm10,pm2_5,uv_index",
        "forecast_days": 7,
        "timezone": "auto",
    }

    response = requests.get(
        AIR_QUALITY_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timezone": data.get("timezone"),
        "hourly": data.get("hourly"),
    }

WIKIMEDIA_API_URL = "https://en.wikipedia.org/w/api.php"


def get_wikimedia_description(destination: str) -> dict:
    """Get a plain-text description of a destination from Wikipedia."""

    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": 1,
        "exintro": 1,
        "titles": destination,
        "format": "json",
    }

    headers = {
        "User-Agent": "AI-Trip-Planner/1.0 (educational project)"
    }

    response = requests.get(
        WIKIMEDIA_API_URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    pages = data["query"]["pages"]

    page = next(iter(pages.values()))

    if "missing" in page:
        raise ValueError(
            f"Wikimedia page not found: {destination}"
        )

    return {
        "page_id": page.get("pageid"),
        "page_title": page.get("title"),
        "description": page.get("extract"),
    }

def get_nearby_attractions(
    latitude: float,
    longitude: float,
    radius: int = 10000,
    limit: int = 10,
) -> list:
    """Get nearby Wikipedia pages that can represent attractions."""

    params = {
        "action": "query",
        "list": "geosearch",
        "gscoord": f"{latitude}|{longitude}",
        "gsradius": radius,
        "gslimit": limit,
        "format": "json",
    }

    headers = {
        "User-Agent": "AI-Trip-Planner/1.0 (educational project)"
    }

    response = requests.get(
        WIKIMEDIA_API_URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("query", {}).get("geosearch", [])

def collect_destination_data(destination: str) -> dict:
    """Collect all external data for a destination."""

    location = geocode_destination(destination)

    weather = get_weather(
        location["latitude"],
        location["longitude"],
    )

    air_quality = get_air_quality(
        location["latitude"],
        location["longitude"],
    )

    description = get_wikimedia_description(destination)

    attractions = get_nearby_attractions(
        location["latitude"],
        location["longitude"],
    )

    return {
        "destination": location,
        "weather": weather,
        "air_quality": air_quality,
        "wikimedia_description": description,
        "nearby_attractions": attractions,
    }

def write_destination_to_bronze(location: dict) -> None:
    """Write geocoding data to the Bronze Delta table."""

    df = spark.createDataFrame([location])

    (
        df.write
        .format("delta")
        .mode("append")
        .saveAsTable("trip_planner.bronze.destinations_raw")
    )

    print("Destination data written to Bronze.")

def write_weather_to_bronze(weather: dict) -> None:
    """Write hourly weather data to the Bronze Delta table."""

    hourly = weather["hourly"]

    records = []

    for i in range(len(hourly["time"])):
        records.append({
            "forecast_time": hourly["time"][i],
            "temperature_2m": hourly["temperature_2m"][i],
            "precipitation_probability": hourly["precipitation_probability"][i],
            "precipitation": hourly["precipitation"][i],
            "weather_code": hourly["weather_code"][i],
            "wind_speed_10m": hourly["wind_speed_10m"][i],
        })

    df = spark.createDataFrame(records)

    (
        df.write
        .format("delta")
        .mode("append")
        .saveAsTable("trip_planner.bronze.weather_raw")
    )

    print("Weather data written to Bronze.")

def write_air_quality_to_bronze(air_quality: dict) -> None:
    """Write hourly air quality data to the Bronze Delta table."""

    hourly = air_quality["hourly"]

    records = []

    for i in range(len(hourly["time"])):
        records.append({
            "forecast_time": hourly["time"][i],
            "pm10": hourly["pm10"][i],
            "pm2_5": hourly["pm2_5"][i],
            "uv_index": hourly["uv_index"][i],
        })

    df = spark.createDataFrame(records)

    (
        df.write
        .format("delta")
        .mode("append")
        .saveAsTable("trip_planner.bronze.air_quality_raw")
    )

    print("Air quality data written to Bronze.")

def write_wikimedia_description_to_bronze(description: dict) -> None:
    """Write Wikimedia destination description to Bronze."""

    df = spark.createDataFrame([description])

    (
        df.write
        .format("delta")
        .mode("append")
        .saveAsTable("trip_planner.bronze.wikimedia_descriptions_raw")
    )

    print("Wikimedia description written to Bronze.")

def write_wikimedia_attractions_to_bronze(attractions: list) -> None:
    """Write nearby Wikimedia attractions to Bronze."""

    if not attractions:
        print("No nearby attractions found.")
        return

    df = spark.createDataFrame(attractions)

    (
        df.write
        .format("delta")
        .mode("append")
        .saveAsTable("trip_planner.bronze.wikimedia_attractions_raw")
    )

    print("Wikimedia attractions written to Bronze.")

if __name__ == "__main__":
    destination = "Visakhapatnam"

    location = geocode_destination(destination)

    attractions = get_nearby_attractions(
        location["latitude"],
        location["longitude"],
    )

    print("Nearby attractions retrieved successfully.")

    write_wikimedia_attractions_to_bronze(attractions)
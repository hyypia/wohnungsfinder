from typing import Literal


def get_gps_coordinates() -> dict[Literal["longitude", "latitude"], float]:
    return {"longitude": 10, "latitude": 20}


get_gps_coordinates()

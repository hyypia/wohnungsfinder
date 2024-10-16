from datetime import datetime
from typing import TypeAlias
from dataclasses import dataclass

from bs4 import element

from config import URL
from exceptions import ParserError
from scraper import scrap_all_flats


# Search parameters
search_params = {
    "min_qm": 39,
    "max_qm": 50,
    "min_rooms": 1,
    "max_rooms": 2,
    "wbs": "erforderlich",
}


Id: TypeAlias = str
FlatUrl: TypeAlias = str


@dataclass(slots=True, frozen=True)
class Flat:
    flat_id: Id
    date: datetime
    address: str
    square: float
    rooms: float
    url: FlatUrl


def _check_wbs_flat(flat: element.Tag) -> bool:
    if (
        flat.abbr
        and flat.abbr["title"] == "Wohnberechtigungsschein"
        and flat.abbr.parent.next_sibling.string == search_params["wbs"]
    ):
        return True
    return False


def _find_element(flat: element.Tag, param_name: str) -> element.Tag:
    """Find HTML target element with flat parameter"""
    element = flat.find(string=param_name)
    if element is None:
        raise ParserError
    element_with_data = element.find_parents("tr")[0].td
    if element_with_data is None:
        raise ParserError
    return element_with_data


def _parse_qm_flat(square: element.Tag) -> float:
    square_str = square.text.replace(",", ".").replace(" m²", "")
    flat_qm = float(square_str)
    return flat_qm


def _parse_rooms_flat(rooms_quantity: element.Tag) -> float:
    flat_rooms_str = rooms_quantity.text.replace(",", ".")
    flat_rooms = float(flat_rooms_str)
    return flat_rooms


def _parse_flat(flat: element.Tag) -> Flat:
    return Flat(
        flat_id=flat["id"],
        date=datetime.now(),
        address=flat.find(class_="map-but").text,
        square=_parse_qm_flat(_find_element(flat, "Wohnfläche: ")),
        rooms=_parse_rooms_flat(_find_element(flat, "Zimmeranzahl: ")),
        url="https://inberlinwohnen.de" + flat.find(class_="org-but")["href"],
    )


def get_flats() -> list[Flat]:
    all_flats_set = scrap_all_flats(URL)
    target_flats = []
    for flat in all_flats_set:
        wbs = _check_wbs_flat(flat)
        qm = _parse_qm_flat(_find_element(flat, "Wohnfläche: "))
        rooms = _parse_rooms_flat(_find_element(flat, "Zimmeranzahl: "))
        if (
            wbs
            and qm > search_params["min_qm"]
            and qm <= search_params["max_qm"]
            and rooms <= search_params["max_rooms"]
        ):
            target_flats.append(_parse_flat(flat))

    return target_flats


if __name__ == "__main__":
    get_flats()

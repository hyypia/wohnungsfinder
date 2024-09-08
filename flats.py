# from db import init_db
# from queries import create_flats_table
# from config import DB_NAME

from pprint import pprint
import json
from parser import parse_flats


def get_flats():
    flats = parse_flats()

    with open("flats.json", "w", encoding="utf-8") as file:
        json.dump(flats, file, indent=4, ensure_ascii=False)


def get_new_flat():
    flats = parse_flats()

    with open("flats.json", "r") as file:
        flats_in_file = json.load(file)

    new_flats = {}
    for flat in flats:
        if flat not in flats_in_file:
            new_flats[flat] = {
                "address": flats[flat]["address"],
                "qm": flats[flat]["qm"],
                "rooms": flats[flat]["rooms"],
                "link": flats[flat]["link"],
            }

    with open("flats.json", "w", encoding="utf-8") as file:
        json.dump(flats, file, indent=4, ensure_ascii=False)

    return new_flats


if __name__ == "__main__":
    # get_flats()
    pprint(get_new_flat())

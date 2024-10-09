# from db import init_db
# from queries import create_flats_table
# from config import DB_NAME

from pathlib import Path
from pprint import pprint
import json

from parser import get_flats
from storage import JSONFileFlatStorage, save_flat, load_flats


def save_flats():
    flats = get_flats()
    for flat in flats:
        save_flat(flat, JSONFileFlatStorage(Path.cwd() / "flats.json"))


def get_new_flat():
    flats = get_flats()
    file_flats = load_flats(JSONFileFlatStorage(Path.cwd() / "flats.json"))
    file_flats_ids = {flat["flat_id"]: True for flat in file_flats}
    new_flats = [flat for flat in flats if flat.flat_id in file_flats_ids]
    pprint(new_flats)


if __name__ == "__main__":
    # save_flats()
    get_new_flat()

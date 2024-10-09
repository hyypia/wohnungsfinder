from typing import Protocol, TypedDict
from pathlib import Path
import json

from parser import Flat


class FlatStorage(Protocol):
    """Interface for storage saving Flat"""

    def save(self, flat: Flat) -> None:
        raise NotImplementedError

    def read(self) -> list:
        raise NotImplementedError


class FlatRecord(TypedDict):
    flat_id: str
    date: str
    address: str
    square: str
    rooms: str
    url: str


class JSONFileFlatStorage:
    """Storing flat in JSON file"""

    def __init__(self, json_file: Path) -> None:
        self._json_file = json_file
        self._init_storage()

    def save(self, flat: Flat) -> None:
        flats = self._read()
        flats.append(
            {
                "flat_id": flat.flat_id,
                "date": str(flat.date),
                "address": flat.address,
                "square": str(flat.square),
                "rooms": str(flat.rooms),
                "url": flat.url,
            }
        )
        self._write(flats)

    def read(self) -> list[FlatRecord]:
        return self._read()

    def _init_storage(self) -> None:
        if not self._json_file.exists():
            self._json_file.write_text("[]")

    def _read(self) -> list[FlatRecord]:
        with open(self._json_file, "r") as file:
            return json.load(file)

    def _write(self, flat_record: list[FlatRecord]) -> None:
        with open(self._json_file, "w", encoding="utf-8") as file:
            json.dump(flat_record, file, indent=4, ensure_ascii=False)


def save_flat(flat: Flat, storage: FlatStorage) -> None:
    storage.save(flat)


def load_flats(storage: FlatStorage) -> list[FlatRecord]:
    return storage.read()

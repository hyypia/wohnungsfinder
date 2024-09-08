import random
import requests
from bs4 import BeautifulSoup

from config import URL


# Search parameters
search_params = {
    "min_qm": 39,
    "max_qm": 50,
    "min_rooms": 1,
    "max_rooms": 2,
    "wbs": "erforderlich",
}


def generate_user_agents():
    headers = {}
    with open("user_agents.txt", "rt") as file:
        user_agents = file.read().splitlines()
    random_user_agent = random.choice(user_agents)
    headers = {"user-agent": random_user_agent}
    return headers


def get_all_flats(url):
    headers = generate_user_agents()
    r = requests.post(url, headers=headers).text
    soup = BeautifulSoup(r, "html.parser").find_all("li", class_="tb-merkflat ipg")
    return soup


def check_wbs_flat(flat):
    if (
        flat.abbr
        and flat.abbr["title"] == "Wohnberechtigungsschein"
        and flat.abbr.parent.next_sibling.string == search_params["wbs"]
    ):
        return True


def check_qm_flat(flat):
    flat_qm = (
        flat.th.parent.next_sibling.next_sibling.next_sibling.next_sibling.contents[2]
    )
    flat_qm = float(flat_qm.text.replace(",", ".").replace(" m²", ""))

    if flat_qm > search_params["min_qm"] and flat_qm <= search_params["max_qm"]:
        return True


def check_rooms_flat(flat):
    flat_rooms = flat.th.parent.next_sibling.next_sibling.contents[2].text.replace(
        ",", "."
    )
    flat_rooms = float(flat_rooms)

    if flat_rooms <= search_params["max_rooms"]:
        return True


def get_target_flats(all_flats_list, target_flats):
    for flat in all_flats_list:
        if check_wbs_flat(flat) and check_rooms_flat(flat) and check_qm_flat(flat):
            flat_id = flat["id"]
            flat_address = flat.find(class_="map-but").text
            flat_qm = flat.find(string="Wohnfläche: ").find_parents("tr")[0].td.text
            flat_rooms = (
                flat.find(string="Zimmeranzahl: ").find_parents("tr")[0].td.text
            )
            flat_link = flat.find(class_="org-but")["href"]

            target_flats[flat_id] = {
                "address": flat_address,
                "qm": flat_qm,
                "rooms": flat_rooms,
                "link": "https://inberlinwohnen.de" + flat_link,
            }

    return target_flats


def parse_flats():
    flats_dict = {}
    all_flats_list = get_all_flats(URL)
    flats_list = get_target_flats(all_flats_list, flats_dict)

    return flats_list

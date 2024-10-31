import random
from typing import Literal

import requests
from bs4 import BeautifulSoup, element

from exceptions import BadRequest, RequestError, RequestTimeout


def _generate_user_agents() -> dict[Literal["user-agent"], str]:
    with open("user_agents.txt", "rt") as file:
        user_agents = file.read().splitlines()
    random_user_agent = random.choice(user_agents)
    return {"user-agent": random_user_agent}


def _get_response(url: str) -> str:
    try:
        req = requests.get(url, headers=_generate_user_agents(), timeout=5)
    except requests.ConnectionError:
        raise RequestError
    except requests.Timeout:
        raise RequestTimeout
    if req.status_code != 200:
        raise BadRequest
    return req.text


def scrap_all_flats(url: str) -> element.ResultSet:
    page = _get_response(url)
    soup = BeautifulSoup(page, "html.parser").find_all("li", class_="tb-merkflat ipg")
    return soup

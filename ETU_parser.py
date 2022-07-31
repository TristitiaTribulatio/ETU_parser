from config import SPECIALITIES, ETU_URL
import requests
from typing import NamedTuple
from bs4 import BeautifulSoup

class Info(NamedTuple):
    speciality: str
    count_agreements: str

def get_pages(unique_number: str) -> list[Info]:
    info = list()

    for desc, spec in SPECIALITIES:
        page = requests.get(f'{ETU_URL + spec}-competitive')
        soup = BeautifulSoup(page.text, "html.parser")
        info.append(get_info(unique_number, desc, soup))

    return info

def get_info(unique_number: str, desc: str, soup: BeautifulSoup) -> Info:
    count_agreements = 0
    
    for user in soup.find_all('tr'):
        for field in user.children:
            if 'class="fio"' in str(field) and field.string == unique_number:
                return Info(desc, count_agreements)
            if 'class="is-agree"' in str(field) and field.string == 'Да': count_agreements += 1
    return Info(desc, 'Нет в списке')
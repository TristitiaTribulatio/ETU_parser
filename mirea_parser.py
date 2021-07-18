import requests
from bs4 import BeautifulSoup

MIREA_URL = 'https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition='
COMPETITIONS = {
                '09.03.01 IT': ['Информатика и вычислительная техника (ИТ)', '1698268858631105846'],
                '09.03.01 Kib': ['Информатика и вычислительная техника (Киб)', '1700361394138950966'],
                '09.03.02 KBSP': ['Информационные системы и технологии (КБСП)', '1700361765783645494'],
                '09.03.02 RTS': ['Информационные системы и технологии (РТС)', '1700361828395167030'],
                '09.03.02 FTI': ['Информационные системы и технологии (ФТИ)', '1700361912410221878'],
                '09.03.03 IT': ['Прикладная информатика (ИТ)', '1700362013307350326'],
                '09.03.04 IT': ['Программная инженерия (ИТ)', '1700362082409557302'],
                }

class Parser:
    def __init__(self, unique_number):
        self.info = {'unique_number': unique_number, 'info': {}}
        self.get_pages()

    '''Парсит страницу каждой компетенции'''
    def get_pages(self):
        for info in COMPETITIONS.values():
            page = requests.get(f'{MIREA_URL + info[1]}')
            soup = BeautifulSoup(page.text, "html.parser")
            self.get_info(info[0], soup)

    '''Получает всю информацию для указанного СНИЛСА, а также подсчитывает количество согласий выше'''
    def get_info(self, competetion, soup):
        count_agreements = 0
        for user in soup.find_all('tr'):
            for field in user.children:
                if field.string == 'да':
                    count_agreements += 1
                if field.string == self.info['unique_number']:
                    self.info['info'][competetion] = []
                    [self.info['info'][competetion].append(field.string) for field in user.children if field.string != '\n']
                    self.info['info'][competetion].append(count_agreements)
                    return True

if __name__ == '__main__':
    Parser()
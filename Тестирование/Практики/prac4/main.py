import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

plural_words = {
    'комедии': 'комедия',
    'мультфильмы': 'мультфильм',
    'ужасы': 'ужасы',
    'фантастика': 'фантастика',
    'триллеры': 'триллер',
    'боевики': 'боевик',
    'мелодрамы': 'мелодрама',
    'детективы': 'детектив',
    'приключения': 'приключения',
    'фэнтези': 'фэнтези',
    'военные': 'военный',
    'семейные': 'семейный',
    'аниме': 'аниме',
    'исторические': 'история',
    'драмы': 'драма',
    'документальные': 'документальный',
    'детские': 'детский',
    'криминал': 'криминал',
    'биографии': 'биография',
    'вестерны': 'вестерн',
    'фильмы-нуар': 'фильм-нуар',
    'спортивные': 'спорт',
    'реальное тв': 'реальное тв',
    'короткометражки': 'короткометражка',
    'музыкальные': 'музыка',
    'мюзиклы': 'мюзикл',
    'ток-шоу': 'ток-шоу',
    'игры': 'игра',
}

real_films = [
    'американский психопат', 'во все тяжкие', 'чужой', 'легенда', 'крик',
    'аватар', 'риддик', 'паранормальное явление', 'острые козырьки',
    'и гаснет свет...', 'ходячие мертвецы', 'гравити фолз', 'фиксики'
]

false_films = [
    'ропвыроапвыроапроы', 'рту мирэа', 'сиаод', ' ', '...', 'видеокарта'
]


class TestKinopoisk(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    @unittest.skip("Долгая хуйня")
    def test_check_genres(self):
        url = 'https://www.kinopoisk.ru/lists/categories/movies/8/'
        self.browser.get(url)
        time.sleep(20)
        genres = self.browser.find_elements(By.CSS_SELECTOR,
                                            '.styles_content__2mO6X a')
        genre_urls = [genre.get_attribute('href') for genre in genres]
        genre_names = [
            genre.find_element(By.CLASS_NAME,
                               'styles_name__G_1mq').text.lower()
            for genre in genres
        ]
        for genre_name, genre_url in zip(genre_names, genre_urls):
            print(f"Проверка жанра: {genre_name}")
            self.browser.get(genre_url)
            time.sleep(2)
            films = self.browser.find_elements(By.CLASS_NAME,
                                               'styles_root__ti07r')
            for film in films:
                film_desc = film.find_element(
                    By.CLASS_NAME,
                    'desktop-list-main-info_truncatedText__IMQRP').text.lower(
                    )
                self.assertIn(
                    plural_words[genre_name], film_desc,
                    f"Жанр '{plural_words[genre_name]}' не найден в описании.")
            time.sleep(2)

    @unittest.skip("Долгая хуйня")
    def test_film_search(self):
        url = 'https://www.kinopoisk.ru/'
        self.browser.get(url)
        time.sleep(15)
        search_field = self.browser.find_element(By.NAME, 'kp_query')
        search_field.click()
        for film_name in real_films:
            search_field.send_keys(film_name)
            time.sleep(1)
            suggested_film_name = self.browser.find_element(
                By.CLASS_NAME, 'styles_mainLink__A4Xkh').text
            self.assertIn(film_name, suggested_film_name.lower())
            search_field.clear()
        for film_name in false_films:
            search_field.send_keys(film_name)
            time.sleep(1)
            self.assertEqual(
                self.browser.find_element(By.CLASS_NAME,
                                          'styles_emptySuggest__XEkB0').text,
                'По вашему запросу ничего не найдено')
            search_field.clear()

    def test_serial_index(self):
        url = 'https://www.kinopoisk.ru/special/index/#/?dateFrom=2024-10-21&dateTo=2024-10-27'
        self.browser.get(url)
        time.sleep(5)
        main_index = int(
            self.browser.find_element(By.CLASS_NAME,
                                      'MainHeader_value__2mIDd').text)
        rows = self.browser.find_elements(By.CLASS_NAME,
                                          'Table_link__Fz2Jp')[:100]
        for i, row in enumerate(rows):
            print(f'{i + 1} iteration')
            spans = row.find_elements(By.TAG_NAME, 'span')
            index = int(spans[2].text)
            percent = float(spans[3].text.removesuffix('%').replace(',', '.'))
            self.assertAlmostEqual(round(index / main_index * 100, 2), percent,
                                   1)

    def tearDown(self) -> None:
        self.browser.close()


if __name__ == '__main__':
    unittest.main()

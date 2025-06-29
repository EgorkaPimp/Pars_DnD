import re
import time
from operator import index

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from write_json import  write_json_race

options = Options()
options.add_argument("--headless")


driver = webdriver.Chrome()
name_for_json = ['ru', 'en', 'book']

def search_race():
    driver.get("https://dnd.su/point_buy/")
    time.sleep(0.2)
    elements = driver.find_elements(By.CLASS_NAME, 'col.tile.calc_tile')
    # Зополняем каждый расу персонажа
    for blok_race in elements:
        if 'Multiverse' in blok_race.text:
            continue
        elif 'TCE' in blok_race.text:
            continue
        # Создаем необходимые переменные
        map_for_json = {}
        cont = 0
        for text in blok_race.text.split('\n'):
            map_for_json[name_for_json[cont]] = text
            cont += 1

        blok_race.click()
        time.sleep(0.5)

        # Определяем подрасы
        subraces = []
        search_subraces = driver.find_element(By.CLASS_NAME, 'calc_page_stats_subrace_list.grid-equalHeight')
        # Если есть подраса добавить в масив
        if len(search_subraces.text) != 0:
            split_subrace = search_subraces.text.split('\n')
            for i in split_subrace:
                subraces.append(i)

        # Получаем характеристики от расы
        ability = {}
        if len(subraces) != 0:
            for subrace in subraces:
                subrace_click = driver.find_element(By.XPATH, f'//span[text()="{subrace}"]/..')
                subrace_click.click()
                ability_score_blok = driver.find_elements(By.CLASS_NAME, 'bonus_stat')
                character_aray = []
                for i in ability_score_blok:
                    character_aray.append(i.text)
                ability[subrace] = character_aray
        else:
            ability_score_blok = driver.find_elements(By.CLASS_NAME, 'bonus_stat')
            character_aray = []
            for i in ability_score_blok:
                character_aray.append(i.text)
            ability['race'] = character_aray

        second_element = driver.find_element(By.CLASS_NAME, "svg.svg-16.svg--race")
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).click(second_element).key_up(Keys.CONTROL).perform()
        # Переключаемся на новую вкладку
        driver.switch_to.window(driver.window_handles[1])

        driver.find_element(By.XPATH, f'//span[text()="{map_for_json['en']}"]/..').click()

        all_text_rase = driver.find_elements(By.TAG_NAME, 'p')
        for element_with_speed in all_text_rase:
            if 'Скорость' in element_with_speed.text:
                print(map_for_json['en'])
                speed_split_text = element_with_speed.text.split(' ')
                for elemnt_speed_split in speed_split_text:
                    if 'фут' in elemnt_speed_split:
                        index_fut = speed_split_text.index(elemnt_speed_split)
                speed_rase = speed_split_text[index_fut-1]

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Возвращаемся к списку рас
        srch_race_button = driver.find_elements(By.CLASS_NAME, 'cbutton.page_button.col.btn.btn-gray')
        for i in srch_race_button:
            if 'Раса' in i.text:
                i.click()
        # Отправляем в json
        write_json_race(map_for_json, ability, subraces, speed_rase)


    driver.quit()




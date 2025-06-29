import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from write_json import write_json_spell

options = Options()
options.add_argument("--headless")


driver = webdriver.Chrome()
name_for_json = ['ru', 'en']

def search_spells():
    driver.get("https://dnd.su/spells/")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    elements = driver.find_elements(By.CLASS_NAME, 'cards_list__item-wrapper')
    for element_spell in elements:
        map_for_json = {}

        # Открываем ссылку в новой вкладке (Ctrl + Click)
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).click(element_spell).key_up(Keys.CONTROL).perform()

        # Переключаемся на новую вкладку
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)

        # Собираем информацию с титульной части
        tittle_spell = driver.find_element(By.CLASS_NAME, "card-title").text
        split_title = (tittle_spell.split('\n'))[0].split(' [')
        print(split_title)
        map_for_json[name_for_json[0]] = split_title[0]
        map_for_json[name_for_json[1]] = split_title[1].replace("]", "")
        level_spell = driver.find_element(By.CLASS_NAME, 'size-type-alignment').text

        # Собираем информацию с уровня и школы
        split_level_spell = level_spell.split(' ')
        map_for_json['level'] = split_level_spell[0]
        if len(split_level_spell) > 2:
            map_for_json['school'] = split_level_spell[2]
        else:
            map_for_json['school'] = split_level_spell[1]

        # Собираем остальные даные
        time_doing = driver.find_elements(By.XPATH,
    "//ul[contains(@class, 'params') and contains(@class, 'card__article-body')]//li")
        for i in time_doing:
            if "Время накладывания" in i.text:
                map_for_json['time'] = i.text.split(': ')[1]
            if "Дистанция" in i.text:
                map_for_json['distans'] = i.text.split(': ')[1]
            if "Компоненты" in i.text:
                map_for_json['components'] = i.text.split(': ')[1]
            if "Длительность" in i.text:
                map_for_json['time_doing'] = i.text.split(': ')[1]
            if "Классы" in i.text:
                map_for_json['class'] = i.text.split(': ')[1]
            else:
                map_for_json['text'] = i.text
        # print(map_for_json)
        # Отправка на запись
        write_json_spell(map_for_json)

        # Возвращаемся обратно
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.5)




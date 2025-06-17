import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from write_json import write_json_class

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome()
name_for_json = ['ru', 'en', 'book']

def search_class():
    driver.get("https://dnd.su/class")
    elements = driver.find_elements(By.CLASS_NAME, 'col.tile')
    # Зополняем каждый класс персонажа
    for blok_class in elements:
        # Создаем необходимые переменные
        map_for_json = {}
        cont = 0
        for text in blok_class.text.split('\n'):
            map_for_json[name_for_json[cont]] = text
            cont += 1
        # Открываем ссылку в новой вкладке (Ctrl + Click)
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).click(blok_class).key_up(Keys.CONTROL).perform()
        # Переключаемся на новую вкладку
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.5)
        additional_info = driver.find_elements(By.CLASS_NAME, 'additionalInfo')
        # Собираем данные для создания класса
        blok_text = next((i.text for i in additional_info if "ХИТЫ" in i.text), None)
        if blok_text is None:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            write_json_class(map_for_json)
            continue
        split_blok = blok_text.split("\n")
        for i in range(len(split_blok)):
            if "Доспехи:" in split_blok[i]:
                value = split_blok[i].split(': ')[1]
                array_value = value.split(', ')
                map_for_json["armor"] = array_value
            if "Оружие:" in split_blok[i]:
                value = split_blok[i].split(': ')[1]
                array_value = value.split(', ')
                map_for_json["weapons"] = array_value
            if "Инструменты:" in split_blok[i]:
                value = split_blok[i].split(': ')[1]
                array_value = value.split(', ')
                map_for_json["instruments"] = array_value
            if "Спасброски:" in split_blok[i]:
                value = split_blok[i].split(': ')[1]
                array_value = value.split(', ')
                map_for_json["saving_throws"] = array_value
            if "Навыки:" in split_blok[i]:
                test_len = split_blok[i].split(': ')
                if len(test_len) < 3:
                    value = 'None'
                else:
                    value = test_len[2]
                array_value = value.split(', ')
                map_for_json["skills"] = array_value
            if "Хиты на 1 уровне:" in split_blok[i]:
                value = split_blok[i].split(' ')[4]
                map_for_json["hits"] = value


        driver.close()
        # Переключаемся на обратно
        driver.switch_to.window(driver.window_handles[0])
        write_json_class(map_for_json)

    driver.quit()
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from write_json import  write_json_race

options = Options()
options.add_argument("--headless")


driver = webdriver.Chrome()
name_for_json = ['ru', 'en', 'book']

def search_race():
    driver.get("https://dnd.su/race")
    elements = driver.find_elements(By.CLASS_NAME, 'col.tile')
    # Зополняем каждый расу персонажа
    for blok_race in elements:
        # Создаем необходимые переменные
        map_for_json = {}
        cont = 0
        if blok_race.text.split('\n')[1] != 'Dwarf':
            continue
        for text in blok_race.text.split('\n'):
            map_for_json[name_for_json[cont]] = text
            cont += 1
        # Открываем ссылку в новой вкладке (Ctrl + Click)
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).click(blok_race).key_up(Keys.CONTROL).perform()
        # Переключаемся на новую вкладку
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.5)
        #Собирам остальные данные
        # additional_info = driver.find_elements(By.CLASS_NAME, 'article-body__feature')
        # for i in additional_info:
        #     print(i.text)
        # blok_text = next((i.text for i in additional_info if "ХИТЫ" in i.text), None)
        # print(blok_text)
        # split_blok = blok_text.split("\n")
        # for i in range(len(split_blok)):
        #     print(i)
        subraces = driver.find_elements(By.CLASS_NAME, "inline-menu__item-wrapper")
        for subrace in subraces:
            if 'MPMM' in subrace.text:
                continue
            subrace.click()
            blocks_text = driver.find_elements(By.CLASS_NAME, 'article-body__feature')
            for block_text in blocks_text:
                cleaned_text = next((i for i in block_text.text.split('\n') if " " in i), None)
                if cleaned_text != None:
                    if "Увеличение характеристик" in cleaned_text:
                        map_for_json['ability_score_increase'] = cleaned_text
                    if "Размер" in cleaned_text:
                        map_for_json['size'] = cleaned_text
                    if "Языки" in cleaned_text:
                        map_for_json['languages'] = cleaned_text
        driver.close()
        # Переключаемся на обратно
        driver.switch_to.window(driver.window_handles[0])
        write_json_race(map_for_json)


        if 'Yuan-ti' in map_for_json['en']:
            break

    driver.quit()




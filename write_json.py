import json
import os
import shutil

base_json_class_path = 'base_json/base_class.json'
base_json_race_path = 'base_json/base_race.json'
temp_json_path = 'base_json/temp.json'

def write_json_class(map_for_json):
    # Создаем временый файл
    shutil.copyfile(base_json_class_path, temp_json_path)

    with open(temp_json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    data["name_ru"] = map_for_json["ru"]
    data["name_en"] = map_for_json["en"]
    data["book"] = map_for_json["book"]
    data["hits"] = map_for_json.get("hits")
    data["armor"] = map_for_json.get("armor")
    data["weapons"] = map_for_json.get("weapons")
    data["skills"] = map_for_json.get("skills")
    data["saving_throws"] = map_for_json.get("saving_throws")
    data["instruments"] = map_for_json.get("instruments")

    with open(f'data_json/class/{map_for_json["en"]}.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    os.remove(temp_json_path)

def write_json_race(map_for_json):
    # Создаем временый файл
    shutil.copyfile(base_json_race_path, temp_json_path)

    with open(temp_json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    data["name_ru"] = map_for_json["ru"]
    data["name_en"] = map_for_json["en"]
    data["book"] = map_for_json["book"]
    data["name_character"] = map_for_json.get("hits")
    data["ability_score_increase"] = map_for_json.get("ability_score_increase")
    data["size"] = map_for_json.get("size")
    data["speed"] = map_for_json.get("speed")
    data["traits"] = map_for_json.get("traits")
    data["languages"] = map_for_json.get("languages")
    data["subraces"] = map_for_json.get("subraces")

    with open(f'data_json/race/{map_for_json["en"]}.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    os.remove(temp_json_path)
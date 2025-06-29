import json
import os
import shutil

base_json_class_path = 'base_json/base_class.json'
base_json_race_path = 'base_json/base_race.json'
base_json_spells_path = 'base_json/base_spells.json'
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

def write_json_race(map_for_json, ability, subraces, speed_rase):
    # Создаем временый файл
    shutil.copyfile(base_json_race_path, temp_json_path)

    with open(temp_json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    data["name_ru"] = map_for_json["ru"]
    data["name_en"] = map_for_json["en"]
    data["book"] = map_for_json["book"]
    data["ability_score_increase"] = ability
    data["subraces"] = subraces
    data["speed"] = speed_rase

    with open(f'data_json/race/{map_for_json["en"]}.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    os.remove(temp_json_path)

def write_json_spell(map_for_json):
    # Создаем временый файл
    shutil.copyfile(base_json_spells_path, temp_json_path)

    with open(temp_json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    data["name_ru"] = map_for_json["ru"]
    data["name_en"] = map_for_json["en"]
    data["level"] = map_for_json["level"]
    data["school"] = map_for_json["school"]
    data["time"] = map_for_json["time"]
    data["distans"] = map_for_json["distans"]
    data["components"] = map_for_json["components"]
    data["time_doing"] = map_for_json["time_doing"]
    data["class"] = map_for_json.get("class") or None
    data["text"] = map_for_json["text"]

    if '/' in map_for_json["en"]:
        map_for_json["en"] = map_for_json["en"].replace("/", "_")
    with open(f'data_json/spells/{map_for_json["en"]}.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    os.remove(temp_json_path)
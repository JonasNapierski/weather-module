import requests
import json
from typing import List


def get_config():
    with open("./modules/weather-module/module.json") as file:
        raw_file = file.readall()
        return json.loads(raw_file)


def city_name_given(splitted_msg: List[str]) -> str:
    """ if msg contains "in" returns city
    """
    for i in range(len(splitted_msg)):
        if splitted_msg[i] == "in":
            return splitted_msg[i+1]


def city_name_missing(msg):
    """ if: keyword in cofig found, returns lat, lon
        else: None
    """
    cfg = get_config()
    for keywordobject in cfg["keywords"]:
        if msg.__contains__(keywordobject["keyword"]):
            return keywordobject
    return None


def command_city(city, language, units, APIKEY):
    city_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang={language}&units={units}&appid={APIKEY}"
    data = requests.post(city_url).json()
    if data['cod'] == 200:
        fcast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={data['coord']['lat']}&lon={data['coord']['lon']}&units={units}&lang={language}&appid={APIKEY}"
        fcast = requests.post(fcast_url).json()
        return fcast

def command_cord(language,units,APIKEY,msg):
    keywordobject = city_name_missing(msg)
    fcast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={keywordobject['lat']}&lon={keywordobject['lon']}&lang={language}&units={units}&appid={APIKEY}"
    fcast = requests.post(fcast_url).json()
    return fcast


def exec(msg: str, predicted_cmd: str):
    cfg = get_config()
    mm = msg.split(" ")
    command = predicted_cmd.split("-")
    APIKEY = cfg['api_token']
    language = cfg['language']
    units = cfg['units']
    degree = cfg['degree']
    grad = degree.get(units)
    status = requests.post(f"http://api.openweathermap.org/data/2.5/weather?q=Hamburg&appid={APIKEY}").json()

    if status['cod'] == 200:
        if city_name_missing(msg) is None:
            city = city_name_given(mm)
            if command[0] == 'temp':
                fcast = command_city(city, language, units, APIKEY)
                temp = int(fcast[command[1]][int(command[2])]['temp']['day'])
                return {"cod": 200, "temp": temp, "msg": f"In {city} werden es {temp}°{grad}"}

            elif command[0] == "description":
                fcast = command_city(city,language,units,APIKEY)
                description = fcast[command[1]][int(command[2])]['weather'][0]['description']
                return {"cod": 200, "msg": f"Es wird {description}"}
            else:
                return {"cod": 500, "msg": "Es ist ein Fehler aufgetreten."}

        else:
            if command[0] == 'temp':
                fcast = command_cord(language, units, APIKEY, msg)
                temp = int(fcast[command[1]][int(command[2])]['temp']['day'])
                return {"cod": 200, "temp": temp, "msg": f"{keywordobject['out']} werden es {temp}°{grad}"}
            elif command[0] == "description":
                fcast = command_cord(language, units, APIKEY, msg)
                description = fcast[command[1]][int(command[2])]['weather'][0]['description']
                return {"cod": 200, "msg": f"Es wird {description}"}          
            else:
                return {"cod": 500, "msg": "Es ist ein Fehler aufgetreten."}

    elif status['cod'] == 401:
        return {"cod": 401, "msg": "Invalid Api key. Please check if you inserted an Api key or copied your Api key correctly"}
    else:
        return {"cod": status['cod'], "msg": "An error ocurred"}

import json 
import requests

def stadt_angegeben(mm):
    """ if msg contains "in" returns city
    """
    for i in range(len(mm)):
        if mm[i] == "in":
            city = mm[i+1]
    return city

def stadt_fehlt(msg, user):
    """ if: city found, returns lat, lon
        else: None
    """
    cfg = user.get_module_config("weather-module")
    for keywordobject in cfg["keywords"]:
        if msg.__contains__(keywordobject["keyword"]):
            return keywordobject
    return None

def exec(msg, user):

    cfg = user.get_module_config("weather-module")
    mm = msg.split(" ")

    APIKEY = cfg['api_token']
    language = cfg['language']
    units = cfg['units']
    degree = {"standart":"°K","imperial":"°F","metric": "°C"}
    grad = degree.get(units)

    print(msg)
    print(mm)

    if stadt_fehlt(msg, user) == None:
        city = stadt_angegeben(mm)
        city_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang={language}&units={units}&appid={APIKEY}"
        data = requests.post(city_url).json()
        if data["cod"] == 200:
            temp = round(float(data['main']['temp']))
            return {"temp": temp, "msg": f"In {city} sind es {temp}{grad}", "user": user.uuid}
        else:
            return {"cod": 500, "user": user.uuid}
    else:
        keywordobject = stadt_fehlt(msg, user)
        cord_url = f"https://api.openweathermap.org/data/2.5/weather?lat={keywordobject['lat']}&lon={keywordobject['lon']}&lang={language}&units={units}&appid={APIKEY}"
        data = requests.post(cord_url).json()

        if data["cod"] == 200:
            temp = round(float(data['main']['temp'])) 
            return {"temp": temp, "msg": f"{keywordobject['out']} sind es {temp}{grad}", "user": user.uuid}
        else:
            return {"cod": 500, "user": user.uuid}

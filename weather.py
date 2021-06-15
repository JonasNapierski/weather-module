import json 
import requests

def exec(msg, user):

    cfg = user.get_module_config("weather-module")
    mm = msg.split(" ")

    print(msg)
    print(mm)

    for i in range(len(mm)):
        if mm[i] == "in":
            city = mm[i+1]

    APIKEY = cfg['api_token']
    language = cfg['language']
    units = cfg['units']
    degree = {"standart":"°K","imperial":"°F","metric": "°C"}
    grad = degree.get(units)

    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang={language}&units={units}&appid={APIKEY}"           

    data = requests.post(api_url).json()
    temp = round(float(data['main']['temp']))
    #return data
    try:
        return {"temp": temp, "msg": f"In {city} sind es {temp} {grad}", "user": user.uuid}
    except:
        return {"cod": 500, "user": user.uuid}
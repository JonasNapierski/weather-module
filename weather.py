import json 
import requests
import datetime

def stadt_angegeben(mm):
    """ if msg contains "in" returns city
    """
    for i in range(len(mm)):
        if mm[i] == "in":
            city = mm[i+1]
    return city

def stadt_fehlt(msg, user):
    """ if: keyword in cofig found, returns lat, lon
        else: None
    """
    cfg = user.get_module_config("weather-module")
    for keywordobject in cfg["keywords"]:
        if msg.__contains__(keywordobject["keyword"]):
            return keywordobject
    return None

def forecast(mm):
    if mm.__contains__('morgen'):
        today = datetime.datetime.now()
        new = today + datetime.timedelta(days=1)
        forecasttime = int(new.timestamp())
        return forecasttime
    elif mm.__contains__('übermorgen'):
        today = datetime.datetime.now()
        new = today + datetime.timedelta(days=2)
        forecasttime = int(new.timestamp())
        return forecasttime
    return None

def exec(msg, user):

    cfg = user.get_module_config("weather-module")
    mm = msg.split(" ")

    APIKEY = cfg['api_token']
    language = cfg['language']
    units = cfg['units']
    degree = cfg['degree']
    grad = degree.get(units)
    print(msg)
    print(mm)

    if stadt_fehlt(msg, user) == None:
        city = stadt_angegeben(mm)
        city_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang={language}&units={units}&appid={APIKEY}"
        data = requests.post(city_url).json()
        time = forecast(mm)
        if data["cod"] == 200 and time == None:
            temp = round(float(data['main']['temp']))
            return {"temp": temp, "msg": f"In {city} sind es {temp}°{grad}", "user": user.uuid}
        elif data["cod"] == 200 and time != None:
            fcast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={data['coord']['lat']}&lon={data['coord']['lon']}&units={units}&lang={language}&appid={APIKEY}"
            fcast = requests.post(fcast_url).json()
            print(fcast)
            temp = int(fcast['daily'][1]['temp']['day'])
            return {"temp": temp, "msg": f"In {city} werden es {temp}°{grad}", "user": user.uuid}
        else:
             return {"cod": 500, "user": user.uuid}

    else:
        keywordobject = stadt_fehlt(msg, user)
        cord_url = f"https://api.openweathermap.org/data/2.5/weather?lat={keywordobject['lat']}&lon={keywordobject['lon']}&lang={language}&units={units}&appid={APIKEY}"
        data = requests.post(cord_url).json()

        if data["cod"] == 200:
            temp = round(float(data['main']['temp'])) 
            return {"temp": temp, "msg": f"{keywordobject['out']} sind es {temp}°{grad}", "user": user.uuid}
        else:
            return {"cod": 500, "user": user.uuid}

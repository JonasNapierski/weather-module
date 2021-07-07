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
    """ if: keyword in cofig found, returns lat, lon
        else: None
    """
    cfg = user.get_module_config("weather-module")
    for keywordobject in cfg["keywords"]:
        if msg.__contains__(keywordobject["keyword"]):
            return keywordobject
    return None

def forecast(msg):
    if msg.__contains__('morgen'):
        time = 'daily'
        section = 1
        return time, section
    elif msg.__contains__('übermorgen'):
        time = 'daily'
        section = 2
        return time, section
    elif msg.__contains__('in einer Stunde'):
        time = 'hourly'
        section = 1
        return time, section
    return None, None

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
        #print(data)
        time, section = forecast(msg)

        if data["cod"] == 200 and time == None:
            temp = round(float(data['main']['temp']))
            return {"temp": temp, "msg": f"In {city} sind es {temp}°{grad}", "user": user.uuid}

        elif data["cod"] == 200 and time != None:
            fcast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={data['coord']['lat']}&lon={data['coord']['lon']}&units={units}&lang={language}&appid={APIKEY}"
            fcast = requests.post(fcast_url).json()
            if time == 'hourly':
                temp = int(fcast[time][section]['temp'])
            else:
                temp = int(fcast[time][section]['temp']['day'])
                
            return {"temp": temp, "msg": f"In {city} werden es {temp}°{grad}", "user": user.uuid}
        else:
             return {"cod": 500, "user": user.uuid}

    else:
        keywordobject = stadt_fehlt(msg, user)
        cord_url = f"https://api.openweathermap.org/data/2.5/weather?lat={keywordobject['lat']}&lon={keywordobject['lon']}&lang={language}&units={units}&appid={APIKEY}"
        data = requests.post(cord_url).json()
        time, section = forecast(msg)

        if data["cod"] == 200 and time == None:
            temp = round(float(data['main']['temp'])) 
            return {"temp": temp, "msg": f"{keywordobject['out']} sind es {temp}°{grad}", "user": user.uuid}

        elif data["cod"] == 200 and time != None:
            fcast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={data['coord']['lat']}&lon={data['coord']['lon']}&units={units}&lang={language}&appid={APIKEY}"
            fcast = requests.post(fcast_url).json()
            if time == 'hourly':
                temp = int(fcast[time][section]['temp'])
            else:
                temp = int(fcast[time][section]['temp']['day'])

            return {"temp": temp, "msg": f"{keywordobject['out']} werden es {temp}°{grad}", "user": user.uuid}             
        else:
            return {"cod": 500, "user": user.uuid}

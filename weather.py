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

def command_stadt(city,language,units,APIKEY):
    city_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang={language}&units={units}&appid={APIKEY}"
    data = requests.post(city_url).json()
    if data['cod'] == 200:
        fcast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={data['coord']['lat']}&lon={data['coord']['lon']}&units={units}&lang={language}&appid={APIKEY}"
        fcast = requests.post(fcast_url).json()
        return fcast

def command_cord(language,units,APIKEY,msg,user):
    keywordobject = stadt_fehlt(msg, user)
    fcast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={keywordobject['lat']}&lon={keywordobject['lon']}&lang={language}&units={units}&appid={APIKEY}"
    fcast = requests.post(cord_url).json()
    return fcast

def exec(msg, user, predicted_cmd):

    cfg = user.get_module_config("weather-module")
    mm = msg.split(" ")
    command = predicted_cmd.split("-")
    APIKEY = cfg['api_token']
    language = cfg['language']
    units = cfg['units']
    degree = cfg['degree']
    grad = degree.get(units)

    print(msg)
    print(mm)
    print(command)


    if stadt_fehlt(msg, user) == None:
            city = stadt_angegeben(mm)
            if command[0] == 'temp':
                fcast = command_stadt(city,language,units,APIKEY)
                temp = int(fcast[command[1]][int(command[2])]['temp']['day'])
                return {"cod": 200, "temp": temp, "msg": f"In {city} werden es {temp}°{grad}", "user": user.uuid}

            elif command[0] == "description":
                    fcast = command_stadt(city,language,units,APIKEY)
                    description = fcast[command[1]][int(command[2])]['weather'][0]['description']
                    return {"cod": 200, "msg": f"Es wird {description}", "user": user.uuid}
            else:
                    return {"cod": 500, "msg": "Es ist ein Fehler aufgetreten.", "user": user.uuid}

    else:
        if command[0] == 'temp':
            fcast = command_cord(language, units, APIKEY, msg, user)
            temp = int(fcast[command[1]][int(command[2])]['temp']['day'])
            return {"cod": 200, "temp": temp, "msg": f"{keywordobject['out']} werden es {temp}°{grad}", "user": user.uuid}             
        else:
            return {"cod": 500, "msg": "Es ist ein Fehler aufgetreten.", "user": user.uuid}
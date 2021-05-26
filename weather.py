import json 
import requests

with open("modules/weather-module/module.json", "r") as f:
    cfg = json.loads(f.read())



def exec(msg, user):

    cfg = user.get_module_config("weather-module")

    api_url = "http://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}"
    api_url = api_url.replace("{API key}", cfg['api_token'])

    print(msg)
    city = ""
    mm = msg.split(" ")
    print(mm)
    for i in range(len(mm)):
        if mm[i] == "in":
            city = mm[i+1]
               
                
    api_url = api_url.replace("{city name}", city)

    data = requests.post(api_url).json()
    temp = float(data['main']['temp'])
    temp = temp - 273.15
    #return data
    try:
        return {"temp": temp, "msg": f"In {city} sind es {temp:.2f}°c", "user": user.uuid}
    except:
        return {"cod": 500, "user": user.uuid}
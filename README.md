# Weather-Module for Leni
Leni-PY or just [Leni](https://github.com/jonasnapierski/leni-py) is a home assistant backend. Based on Flask it is designed to quickly extend your own assistant with simple Python **modules**.

This module uses the [OpenWeatherMap](https://openweathermap.org/api) API to get the weather information your want.
## Installing
To use this module you first need to install [Leni](https://github.com/jonasnapierski/leni-py) and follow the instructions there.
## Use
After you installed the Weather-Module you need an [OpenWeatherMap](https://openweathermap.org/api) API token. You copy that token into the *weather-module.json* file in the *config* folder.
Now the module can be used.
### Personalize
If you want to add specific locations you can do that with keywords in the *weather-module.json* file. So you can ask Leni: "How is the weather at home" and get the correct answer.

 

    "keywords": [
      {
	    "keyword": "EXAPLE_NAME",
	    "lat": [float],
	    "lon":[float],
	    "out": "EXAPLE_NAME output message"
	  }
	],

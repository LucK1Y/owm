import requests
import datetime


class OWM_Wrapper(object):
    def __init__(self, auth_key: str = None):
        if auth_key:
            self.key = auth_key
        else:
            self.key = input("please input Api-key: ")

        self.forecast = None
        self.current = None

        self.city = None
        self.country = None

    def getForeCast(self, cityName: str, countryCode: str) -> list:
        """
        get Forecast for City in Country
        results will be saved in object.forecast
        """
        self.city = cityName
        self.country = countryCode

        headers = {'content-type': 'application/json'}

        url = f'https://api.openweathermap.org/data/2.5/forecast?q={cityName},{countryCode}&APPID={self.key}'
        r = requests.get(url, headers=headers)

        try:
            self.forecast = r.json()['list']
        except Exception as ex:
            print("Got Error message: ")
            print(ex)
            print("got ", r.json())
            print(r)
            return []

        return self.forecast

    def getCurrentWeather(self, cityName: str, countryCode: str) -> list:
        """
        get Current Weather for City in Country
        results will be saved in object.current
        """
        self.city = cityName
        self.country = countryCode

        headers = {'content-type': 'application/json'}

        url = f'https://api.openweathermap.org/data/2.5/weather?q={cityName},{countryCode}&APPID={self.key}'
        r = requests.get(url, headers=headers)

        try:
            self.current = r.json()
        except Exception as ex:
            print("Got Error message: ")
            print(ex)
            print("Got ", r)
            return []

        return self.current

    def requestForData(self, func):
        print("[*] still needs to request data\n")
        if not self.city:
            self.city = input("Please input cityname: ")
        if not self.country:
            self.country = input("Please input countrycode: ")

        func(self.city, self.country)

    def getTodaysRain(self) -> dict:
        """
        get todays rain
        getForeCast has to be invoked
        """

        if not self.forecast:
            self.requestForData(self.getForeCast)

        output = dict()
        for element in self.forecast:
            date_Element = element['dt_txt']
            date_Time = datetime.datetime.strptime(
                date_Element, '%Y-%m-%d %H:%M:%S')

            if date_Time.day == datetime.datetime.today().day:
                if 'rain' in element:
                    rain = element['rain']['3h']
                else:
                    rain = 0
                output[date_Time.hour] = str(rain)

        return output

    def getTodaysTemp(self):
        """
        get todays temperature  
        getForeCast has to be invoked 
        """

        if not self.forecast:
            self.requestForData(self.getForeCast)

        output = dict()
        for element in self.forecast:
            date_Element = element['dt_txt']
            date_Time = datetime.datetime.strptime(
                date_Element, '%Y-%m-%d %H:%M:%S')

            if date_Time.day == datetime.datetime.today().day:
                temp = format(float(element['main']['temp_kf']), ".2f")
                output[date_Time.hour] = str(temp)

        return output

    def todayTemp_MessagePart(self):
        """
        returns nice string with temperature to be part of a message
        """
        data = self.getTodaysTemp()
        msg = "Temp. today \n"

        for key, value in data.items():
            msg += "\t{} Uhr->Temp: {} °C\n".format(key, value)

        return msg + "\n"

    def weatherCurrent_MessagePart(self):
        """
        returns nice string with current weather details  to be part of a message
        """
        if not self.current:
            self.requestForData(self.getCurrentWeather)

        description = self.current["weather"][0]["description"]
        min_t = format(float(self.current["main"]["temp_min"]) - 273.15, ".2f")
        max_t = format(float(self.current["main"]["temp_max"]) - 273.15, ".2f")
        clouds = self.current["clouds"]["all"]

        out = f"""The current weather: 
        {description}
        tmp: {min_t} bis {max_t} °C
        clouds:{clouds}

        """

        return out

    def todayRain_MessagePart(self):
        """
        returns nice string with rain details  to be part of a message
        """

        data = self.getTodaysRain()
        msg = "Rain today \n"

        for key, value in data.items():
            msg += "\t{} Uhr->Rain: {} mm\n".format(key, value)

        return msg + "\n"

    def createMessage(self, *parts) -> str:
        """
        creates complete message with parts

        parts: possible parts for message
        """

        msg = "Hey you,\n\n"
        for part in parts:
            msg += part

        msg += "\n\nGreetings Your Python"
        return msg

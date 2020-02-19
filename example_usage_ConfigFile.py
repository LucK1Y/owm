from src.owmWrapper import OWM_Wrapper


owmWrapper = OWM_Wrapper("<API KEY>")
owmWrapper.city="<City>"
owmWrapper.country="<Countrycode>"

rain=owmWrapper.todayRain_MessagePart()
temp=owmWrapper.todayTemp_MessagePart()

current=owmWrapper.weatherCurrent_MessagePart()

message=owmWrapper.createMessage(rain,temp,current)

print(message)
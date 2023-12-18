import requests

# OpenWeatherMap API anahtarını buraya ekleyin

api_key = "7fdb6f5734ab0e721e58db2859bffe7c"
# Şehir adını ve ülke kodunu belirtin
city_name = "Istanbul"
country_code = "TR"

# API isteği için URL oluşturun
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name},{country_code}&lang=tr&units=metric&appid={api_key}"

# API'den verileri çekin
response = requests.get(url)
data = response.json()

daily_temperatures = []

# Verileri işleyin
for entry in data["list"]:
    date_time = entry["dt_txt"]

    # Eğer saat 15:00:00 ise devam et, değilse bir sonraki veriye geç
    if date_time.endswith("15:00:00"):
        temperature = entry["main"]["temp"]
        description = entry["weather"][0]["description"]

        daily_temperatures.append(entry)

# for date, temperatures in daily_temperatures.items():
#     print(
#         f'Date: {date}, Min Temperature: {temperatures["min"]}°C, Max Temperature: {temperatures["max"]}°C'
#     )
print(daily_temperatures)

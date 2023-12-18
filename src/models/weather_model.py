from datetime import datetime, timedelta


class WeatherModel:
    instances = []

    def __init__(self, data=None):
        self.city_name = data["city"]["name"]
        self.following_days = []
        self.last_month = {}
        self.update(data)

    def update(self, data):
        days_infos = data["list"]
        today_infos = days_infos[0]

        self.coord = data["city"]["coord"]
        self.sunrise = data["city"]["sunrise"]
        self.sunset = data["city"]["sunset"]

        self.temp = today_infos["main"]["temp"]
        self.wind = today_infos["wind"]
        self.date = today_infos["dt"]
        self.description = today_infos["weather"][0]["description"]

        self.last_month = self.create_last_month_fake_data()
        self.following_days = self.update_following_days(days_infos)
        self.creation_date = datetime.now().strftime("%H:%M:%S")

        del days_infos, today_infos

    @classmethod
    def create_or_update(cls, data):
        for instance in cls.instances:
            if instance.city_name == data["city"]["name"]:
                instance.update(data)
                return
        new_instance = cls(data)
        cls.instances.append(new_instance)

    def update_following_days(self, days_infos):
        following_days_list = list()

        for day in days_infos[1:]:
            day_infos = {
                "temp": day["main"]["temp"],
                "description": day["weather"][0]["description"],
                "date": day["dt"],
                "wind": days_infos[0]["wind"],
            }
            following_days_list.append(day_infos)

        return following_days_list

    def create_last_month_fake_data(self):
        sunrise = datetime.utcfromtimestamp(self.sunrise) - timedelta(minutes=30)
        sunset = datetime.utcfromtimestamp(self.sunset) - timedelta(minutes=30)
        date = datetime.utcfromtimestamp(self.date) - timedelta(days=30)
        temp = self.temp + 2.2
        return {
            "temp": temp,
            "wind": self.wind,
            "description": self.description,
            "sunrise": int(sunrise.timestamp()),
            "sunset": int(sunset.timestamp()),
            "date": int(date.timestamp()),
        }

    def get_weather_data(self):
        return self.__dict__

    @classmethod
    def get_all_cities_weather_datas(cls):
        return [nesne.__dict__ for nesne in cls.instances]

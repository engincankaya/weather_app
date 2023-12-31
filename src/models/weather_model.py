from datetime import datetime, timedelta


class WeatherModel:
    instances = []

    def __init__(self, data=None):
        # Eğer veri mevcutsa, özellikleri başlat
        if data:
            self.city_name = data["city"]["name"]
            self.following_days = []
            self.last_year_data = {}
            self.update(data)

    def update(self, data):
        # Bugünkü ve takip eden günlerin hava durumu verilerini güncelle
        days_infos = data["list"]
        today_infos = days_infos[0]

        self.coord = data["city"]["coord"]
        self.sunrise = data["city"]["sunrise"]
        self.sunset = data["city"]["sunset"]

        self.temp = today_infos["main"]["temp"]
        self.wind = today_infos["wind"]
        self.date = today_infos["dt"]
        self.description = today_infos["weather"][0]["description"]
        self.icon = today_infos["weather"][0]["icon"]

        self.last_year_data = self.create_last_year_fake_data()
        self.following_days = self.update_following_days(days_infos[1:])
        self.creation_date = datetime.now().strftime("%H:%M:%S")

        del days_infos, today_infos

    @classmethod
    def create_or_update(cls, data):
        # Şehir adına göre mevcut bir nesne varsa güncelle, yoksa yeni bir nesne oluştur
        for instance in cls.instances:
            if instance.city_name == data["city"]["name"]:
                instance.update(data)
                return
        new_instance = cls(data)
        cls.instances.append(new_instance)

    @classmethod
    def get_all_cities_main_weather_datas(cls):
        # Tüm şehirlerin ana hava durumu verilerini al
        return [instance._extract_main_infos() for instance in cls.instances]

    def _extract_main_infos(self):
        # Ana hava durumu verilerini çıkar
        data_dict = self.__dict__.copy()

        del data_dict["following_days"]
        del data_dict["last_year_data"]

        return data_dict

    @classmethod
    def get_detailed_infos_by_name(cls, city_name):
        # Şehir adına göre detaylı bilgileri al
        for instance in cls.instances:
            if instance.city_name == city_name:
                return instance.__dict__

    def update_following_days(self, following_days):
        # Takip eden günlerin hava durumu verilerini güncelle
        following_days_list = list()

        for day in following_days:
            day_infos = {
                "temp": day["main"]["temp"],
                "description": day["weather"][0]["description"],
                "icon": day["weather"][0]["icon"],
                "date": day["dt"],
                "wind": self.wind,
            }
            following_days_list.append(day_infos)

        return following_days_list

    def create_last_year_fake_data(self):
        # Geçen yılın sahte verilerini oluştur
        date = datetime.utcfromtimestamp(self.date) - timedelta(days=365)
        temp = self.temp + 2.2
        return {
            "temp": temp,
            "wind": self.wind,
            "description": self.description,
            "date": int(date.timestamp()),
        }

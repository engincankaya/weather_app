from datetime import datetime


class UserModel:
    def __init__(self, full_name, email, id):
        self._id = id
        self._full_name = full_name
        self._email = email
        self._login_date = datetime.now().strftime("%H:%M:%S")

    def get_user_infos(self):
        return self.__dict__

    def get_full_name(self):
        return self.__dict__["_full_name"]

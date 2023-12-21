from datetime import datetime
import json
import uuid
import bcrypt
import re


class UserModel:
    def __init__(self, full_name, email, id):
        # Kullanıcı modeli oluşturucu
        self._id = id
        self._full_name = full_name
        self._email = email
        self._login_date = datetime.now().strftime("%H:%M:%S")

    def get_user_infos(self):
        # Kullanıcı bilgilerini getir
        return self.__dict__

    @staticmethod
    def create_account(fullname, email, password):
        # Kullanıcı hesabı oluştur
        if not fullname:
            error_message = "İsim ve Soyisim bilgileri girmelisiniz."
            return error_message
        if not password:
            error_message = "Şifre bilgisi girmelisiniz."
            return error_message

        id = str(uuid.uuid4())
        # Şifreyi bcrypt kullanarak hashle
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        # Kullanıcıları dosyadan oku

        if UserModel.validate_email(email):
            # Eğer email zaten kayıtlıysa
            if UserModel.check_user_exists_in_database(email):
                error_message = "Bu email adresi zaten kullanılmaktadır."
                return error_message
            # Yeni kullanıcıyı ekle
            new_user = {
                "fullname": fullname,
                "email": email,
                "id": id,
                "hashed_password": hashed_password.decode("utf-8"),
            }

            # Kullanıcıları dosyaya yaz
            UserModel.write_user_to_database(new_user)
        else:
            error_message = "Geçersiz email formatı."
            return error_message

    @staticmethod
    def user_login(email, password):
        # Kullanıcı girişi
        users = UserModel.get_all_users()
        success = False
        for user in users:
            if user["email"] == email and bcrypt.checkpw(
                password.encode("utf-8"), user["hashed_password"].encode("utf-8")
            ):
                success = True
                return

        if not success:
            return "Geçersiz mail adresi veya şifre. Lütfen tekrar deneyin"

    @staticmethod
    def check_user_exists_in_database(email):
        # Email'in veritabanında olup olmadığını kontrol et
        users = UserModel.get_all_users()
        if any(user["email"] == email for user in users):
            return True
        else:
            return False

    @staticmethod
    def write_user_to_database(new_user):
        # Yeni kullanıcıyı veritabanına yaz
        users = UserModel.get_all_users()
        users.append(new_user)
        with open("user_database.json", "w") as file:
            # Kullanıcı listesini JSON formatında dosyaya yaz
            json.dump(users, file, indent=2)

    @staticmethod
    def get_all_users():
        try:
            with open("user_database.json", "r") as file:
                # Dosyayı JSON nesnesi olarak oku
                data = file.read()
                # JSON nesnesini Python nesnesine dönüştür
                users = json.loads(data)
                return users
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def validate_email(email):
        # Email doğrulama için regex deseni
        email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

        # Email'i eşleştirmek için regex desenini kullan
        if re.match(email_pattern, email):
            return True
        else:
            return False

    @staticmethod
    def get_user_name(email):
        # Email'e göre kullanıcı adını getir
        users = UserModel.get_all_users()
        for user in users:
            if user["email"] == email:
                return user["fullname"]

import json
import bcrypt
import uuid
import re

from models.user_model import UserModel
from views.user_view import UserView
from views.weather_view import WeatherApp
from controllers.weather_controller import WeatherController


class UserController:
    def __init__(self):
        self.model = None
        self.view = None

    def read_users_from_file(self):
        try:
            with open("user_database.json", "r") as file:
                # Read the file as a JSON object
                data = file.read()
                # Convert the JSON object to a Python object
                users = json.loads(data)
                return users
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_users_to_file(self, users):
        with open("user_database.json", "w") as file:
            # Write the users list to the file in JSON format
            json.dump(users, file, indent=2)

    def create_account(self, fullname, email, password):
        id = str(uuid.uuid4())
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        # Read users from the file
        if self.validate_email(email):
            users = self.read_users_from_file()
            # Check if the email is already registered
            if any(user["email"] == email for user in users):
                self.view.display_error("Bu email adresi zaten kullanılmaktadır.")
                return
            # Add the new user
            users.append(
                {
                    "fullname": fullname,
                    "email": email,
                    "id": id,
                    "hashed_password": hashed_password.decode("utf-8"),
                }
            )
            # Write users back to the file
            self.write_users_to_file(users)
            self.send_main_page(fullname)
        else:
            self.view.display_error("Geçersiz email formatı.")

    def login(self, email, password):
        users = self.read_users_from_file()
        # Check username and password
        for user in users:
            if user["email"] == email and bcrypt.checkpw(
                password.encode("utf-8"), user["hashed_password"].encode("utf-8")
            ):
                self.model = UserModel(user["fullname"], user["email"], user["id"])
                self.send_main_page(user["fullname"])
                return

        self.view.display_error(
            "Geçersiz mail adresi veya şifre. Lütfen tekrar deneyin"
        )

    def validate_email(self, email):
        # Define a simple regex pattern for email validation
        email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

        # Use the regex pattern to match the email
        if re.match(email_pattern, email):
            return True
        else:
            return False

    def send_main_page(self, user_fullname):
        self.view.Hide()
        controller = WeatherController(user_fullname)
        controller.run()

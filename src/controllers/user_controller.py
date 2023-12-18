import json
import bcrypt
import uuid
import sys

sys.path.append("/Users/engincankaya/Desktop/Calismalar/weather_app/src")
from models.user_model import UserModel


class UserController:
    def __init__(self):
        self.model = None

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

    def create_account(self):
        id = str(uuid.uuid4())
        fullname = input("Full Name: ")
        email = input("Email: ")
        password = input("Password: ")
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Read users from the file
        users = self.read_users_from_file()

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

        print("Account successfully created.")

    def login(self):
        email = input("Email: ")
        password = input("Password: ")

        users = self.read_users_from_file()
        # Check username and password
        for user in users:
            if user["email"] == email and bcrypt.checkpw(
                password.encode("utf-8"), user["hashed_password"].encode("utf-8")
            ):
                print("Login successful! Welcome, {}.".format(user["fullname"]))
                self.model = UserModel(user["fullname"], user["email"], user["id"])
                print(self.model.get_user_infos())
                return

        print("Incorrect username or password. Please try again.")


if __name__ == "__main__":
    controller = UserController()
    # Create an account
    # controller.create_account()

    # Login function call
    controller.login()

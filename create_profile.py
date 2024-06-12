from mongo_helper import MongoHelper
import os

def main():
    mongo = MongoHelper()
    os.system('clear') # Clear the screen on MacOS and Linux

    user_id = input("Enter User ID: ")
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")

    mongo.profile_upsert(user_id, name, email, phone)

if __name__ == "__main__":
    main()
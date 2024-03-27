"""
Code for HTTP Microservice
"""

from flask import Flask, jsonify, request
import requests


app = Flask(__name__)

# Test e-commerce server details
TEST_SERVER_URL = "http://20.244.56.144/test"
COMPANY_NAME = "goMart"
CLIENT_ID = "37bb493c-73d3-47ea-8675-21f66ef9b735"
CLIENT_SECRET = "HVIQBVbqmTGEmaED"
OWNER_NAME = "Shubham"
OWNER_EMAIL = "21104046@mail.jiit.ac.in"
ROLL_NO = "21104046"
ACCESS_CODE = "zpKKbc"

# Authentication token
TOKEN = None

# Register with the test e-commerce server
def register():
    global CLIENT_ID, CLIENT_SECRET
    register_url = f"{TEST_SERVER_URL}/register"
    register_data = {
        "companyName": COMPANY_NAME,
        "ownerName": OWNER_NAME,
        "rollNo": ROLL_NO,
        "ownerEmail": OWNER_EMAIL,
        "accessCode": ACCESS_CODE,
    }
    response = requests.post(register_url, json=register_data)
    if response.status_code == 200:
        response_data = response.json()
        CLIENT_ID = response_data["clientID"]
        CLIENT_SECRET = response_data["clientSecret"]
        print("Registration successful!")
        print(f"Client ID: {CLIENT_ID}")
        print(f"Client Secret: {CLIENT_SECRET}")
    else:
        print(f"Registration failed: {response.text}")

# Get the authentication token
def authenticate():
    global token
    auth_url = f"{TEST_SERVER_URL}/auth"
    auth_data = {
        "companyName": COMPANY_NAME,
        "clientID": CLIENT_ID,
        "clientSecret": CLIENT_SECRET,
        "ownerName": OWNER_NAME,
        "ownerEmail": OWNER_EMAIL,
        "rollNo": ROLL_NO,
    }
    response = requests.post(auth_url, json=auth_data)
    if response.status_code == 200:
        TOKEN = response.json()["access_token"]
    else:
        print(f"Authentication failed: {response.text}")

if __name__ == "__main__":
    app.run(debug=True)

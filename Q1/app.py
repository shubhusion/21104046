"""
Code for HTTP Microservice
"""

from flask import Flask, jsonify, request
import requests
import uuid

app = Flask(__name__)

# Client ID: 378093fb-efac-4094-97e8-f92924b5c38c
# Client Secret: soSNeTPADKZOYGJU
# Authentication failed: {"token_type":"Bearer","access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzExNTMzMTc5LCJpYXQiOjE3MTE1MzI4NzksImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjM3ODA5M2ZiLWVmYWMtNDA5NC05N2U4LWY5MjkyNGI1YzM4YyIsInN1YiI6IjIxMTA0MDQ2QG1haWwuamlpdC5hYy5pbiJ9LCJjb21wYW55TmFtZSI6ImdvTWFydCIsImNsaWVudElEIjoiMzc4MDkzZmItZWZhYy00MDk0LTk3ZTgtZjkyOTI0YjVjMzhjIiwiY2xpZW50U2VjcmV0Ijoic29TTmVUUEFES1pPWUdKVSIsIm93bmVyTmFtZSI6IlNodWJoYW0iLCJvd25lckVtYWlsIjoiMjExMDQwNDZAbWFpbC5qaWl0LmFjLmluIiwicm9sbE5vIjoiMjExMDQwNDYifQ.M2360awzI-4_OyE09R863Ch0YB9TKMB34ofV_p_-Yes","expires_in":1711533179}
# Test e-commerce server details
TEST_SERVER_URL = "http://20.244.56.144/test"
COMPANY_NAME = "goMart"
CLIENT_ID = "378093fb-efac-4094-97e8-f92924b5c38c"
CLIENT_SECRET = "soSNeTPADKZOYGJU"
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
    """
    Authentication with the Test Server
    """
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

    TOKEN = response.json()["access_token"]
    print(f"Access token: {TOKEN}")


def fetch_products(
    company_name, category_name, top=10, min_price=0, max_price=float("inf")
):
    authenticate()
    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{TEST_SERVER_URL}/companies/{company_name}/categories/{category_name}/products"
    params = {
        "top": top,
        "minPrice": min_price,
        "maxPrice": max_price,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch products: {response.text}")
        return []


# Combine and sort products from multiple companies
def get_top_products(
    category_name,
    top=10,
    min_price=0,
    max_price=float("inf"),
    sort_by="price",
    ascending=True,
):
    all_products = []
    companies = ["AMZ", "FLP", "SNP", "MYN", "AZO"]
    for company in companies:
        company_products = fetch_products(
            company, category_name, top, min_price, max_price
        )
        all_products.extend(company_products)

    sorted_products = sorted(
        all_products, key=lambda p: p[sort_by], reverse=not ascending
    )
    return sorted_products[:top]


# Generate a unique ID for each product
def generate_product_id(product):
    return str(
        uuid.uuid5(uuid.NAMESPACE_URL, f"{product['productName']}_{product['price']}")
    )

# API endpoint to get top products
@app.route("/categories/<category_name>/products", methods=["GET"])
def get_products(category_name):
    top = int(request.args.get("top", 10))
    min_price = int(request.args.get("minPrice", 0))
    max_price = int(request.args.get("maxPrice", float("inf")))
    sort_by = request.args.get("sortBy", "price")
    ascending = request.args.get("order", "asc") == "asc"

    products = get_top_products(
        category_name, top, min_price, max_price, sort_by, ascending
    )
    response_data = [
        {"id": generate_product_id(product), **product} for product in products
    ]

    return jsonify(response_data)

# API endpoint to get product details
@app.route("/categories/<category_name>/products/<product_id>", methods=["GET"])
def get_product_details(category_name, product_id):
    products = get_top_products(category_name)
    for product in products:
        if generate_product_id(product) == product_id:
            return jsonify(product)
    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    authenticate()

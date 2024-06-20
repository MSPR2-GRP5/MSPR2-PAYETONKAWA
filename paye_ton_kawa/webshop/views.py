import json

from django.shortcuts import render

from webshop.models import Customer, Product
import requests


def index(request):
    customers_json = get_request("customer", {"Id": ""})
    customers: list[Customer] = []

    for customer_dict in customers_json:
        # Could have used customer = Customer(**customer_dict) if the arguments names were the same
        customer = Customer(
            customer_dict["id"],
            customer_dict["Nom"],
            customer_dict["Prenom"],
            customer_dict["Adresse"],
        )
        customers.append(customer)

    products_json = get_request("product", {"id": ""})
    products: list[Product] = []

    for product_dict in products_json:
        product = Product(
            product_dict["id"],
            product_dict["product_name"],
            product_dict["description"],
            product_dict["import_location"],
            product_dict["price"],
            product_dict["stocks"],
        )
        products.append(product)

    return render(
        request, "webshop/index.html", {"customers": customers, "products": products}
    )


def get_request(api: str, params: dict) -> dict:
    options = {
        "customer": {
            "api_key": "fFZz3dds.vDhQdMclOW4Tw4Ny15QRKxsnQWoA64ifrsv6wNlPeG5YMk2M59HIuUEu",
            "port": 8001,
        },
        "product": {"api_key": "", "port": 8002},
    }

    url = f"http://localhost:{options[api]['port']}/api/{api}"
    headers = {
        "accept": "application/json",
        "X-API-Key": options[api]["api_key"],
    }

    try:
        response = requests.get(url, params=params, headers=headers)
    # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed. Is the API server running ?"}

    return json.loads(response.text)

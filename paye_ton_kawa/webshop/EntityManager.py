from pathlib import Path
from typing import Any, Final

from webshop.models import Order, Product, Customer

import requests
import json
import environ


env = environ.Env()
env.read_env(str(Path(__file__).resolve().parent.parent / ".env"))

API_SETTINGS: Final[dict[str, dict[str, str]]] = {
    "customer": {
        "api_key": env("API_TOKEN_CUSTOMER"),
        "url": "http://localhost:8001/api/customer",
    },
    "product": {"api_key": "", "url": "http://localhost:8002/api/product"},
    "order": {"api_key": "", "url": "http://localhost:8003/api/order"},
}


def request(api_name: str, parameters: dict[str, Any]) -> Any:
    settings = API_SETTINGS[api_name]
    url_id = f"/{parameters['url_id']}" if "url_id" in parameters else ""
    url = f"{settings['url']}{url_id}"
    print(url)
    headers = {
        "accept": "application/json",
        "X-API-Key": settings["api_key"],
    }

    try:
        response = requests.get(
            url, params=parameters["request_params"], headers=headers
        )
        print(response)
    # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed. Is the API server running ?"}

    try:
        response_json = response.json()
    except json.JSONDecodeError:
        return {"error": "JSON decoding error. Is the API url correct ?"}

    return response_json


def json_to_object(
    object_json: Any, object_name: str
) -> list[Customer] | list[Product] | list[Order] | list[None]:
    match object_name:
        case "customer":
            customers: list[Customer] = []
            for customer_dict in object_json:
                customer = Customer(
                    customer_dict["id"],
                    customer_dict["Nom"],
                    customer_dict["Prenom"],
                    customer_dict["Adresse"],
                )
                customers.append(customer)
            return customers

        case "product":
            products: list[Product] = []
            for product_dict in object_json:
                product = Product(
                    product_dict["id"],
                    product_dict["product_name"],
                    product_dict["description"],
                    product_dict["import_location"],
                    product_dict["price"],
                    product_dict["stocks"],
                )
                products.append(product)
            return products

        case "order":
            orders: list[Order] = []
            for order_dict in object_json:
                order = Order(
                    int(order_dict["idCommande"]),
                    order_dict["idClient"],
                    order_dict["idProduit"],
                    order_dict["dateCommande"],
                    int(order_dict["quantite"]),
                    int(order_dict["prix"]),
                )
                orders.append(order)
            return orders
    return []


class EntityManager:
    @staticmethod
    def get_all(
        api_name: str,
    ) -> list[Customer] | list[Product] | list[Order] | list[None] | dict[str, Any]:
        # Exploit the API to get all the entities without knowing the fields name
        params = {"request_params": {"gibberish": "random"}}

        response = request(api_name, params)

        if "error" in response:
            print(
                "####################\n",
                "Error: ",
                response["error"],
                "\n####################\n",
            )
            return response

        return json_to_object(response, api_name)

    # def get_entity_by(self, model: Customer|Product|Order, fields: {str: Any}) -> Customer|Product|Order:

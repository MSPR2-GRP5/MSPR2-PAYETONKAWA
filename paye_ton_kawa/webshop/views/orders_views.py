import json
from pathlib import Path
from typing import Any, Final

import environ
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

env = environ.Env()
env.read_env(str(Path(__file__).resolve().parent.parent / ".env"))

API_SETTINGS: Final[dict[str, dict[str, str]]] = {
    "customer": {
        "api_key": env("API_TOKEN_CUSTOMER"),
        "url": "https://client.mspr.lorisperc.in",
    },
    "product": {
        "api_key": env("API_TOKEN_PRODUCT"),
        "url": "https://produit.mspr.lorisperc.in",
    },
    "order": {"api_key": env("API_TOKEN_ORDER"), "url": "https://commande.mspr.lorisperc.in"},
}

HEADERS = {
    "accept": "application/json",
    "X-API-Key": API_SETTINGS["order"]["api_key"],
}


def index_order(request: Any) -> HttpResponse:
    context = {
        "heading": "Commandes",
        "table_headers": ["ID", "Date de création", "Client", "Produits", ""],
        "search_form": {"inputs": []},
    }
    return render(request, "webshop/index.html", context)


def create_order(request: Any) -> HttpResponse:
    error = ""
    if request.method == "POST":
        try:
            data = {
                "customerId": request.POST.get("customer_id"),
                "products": request.POST.get("products"),
            }
            response = requests.post(
                f"{API_SETTINGS['order']['url']}/", params=data, headers=HEADERS
            )
            print("Data: \n", request.POST)
            print("Response: \n", response)
            print("Content: \n", response.content)

            if response.status_code != 200:
                print("Data: \n", request.POST)
                print("Response: \n", response)
                error = "Error in the customer creation"
            else:
                return redirect("index_order")

            # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
        except requests.exceptions.ConnectionError:
            print({"error": "Connection failed. Is the API server running ?"})
            error = "Connection failed. Is the API server running ?"

    fields = {
        "customer_id": {
            "label": "ID Client",
            "type": "number",
        },
        "products": {
            "label": "Produits",
            "type": "text",
        },
    }

    return render(
        request,
        "webshop/update.html",
        {
            "action_id": id,
            "fields": fields,
            "error": error,
            "heading": "Créer une commande",
            "cancel_href": "/orders/",
            "submit_text": "Créer",
        },
    )


@require_http_methods(["POST"])
def find_order(request: Any, order_id: int) -> HttpResponse:
    return HttpResponse({"success": f"Commande {order_id} trouvé"})


@require_http_methods(["POST"])
def find_order_by(request: Any) -> HttpResponse:
    return HttpResponse({"success": "Commande trouvé"})


def find_all_orders(request: Any) -> HttpResponse:
    try:
        response = requests.get(API_SETTINGS["order"]["url"], headers=HEADERS)
    # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        print({"error": "Connection failed. Is the API server running ?"})
        return render(
            request,
            "webshop/data_table_content.html",
            {"error": "Connection failed. Is the API server running ?"},
        )

    try:
        response_json = response.json()
    except json.JSONDecodeError:
        print({"error": "JSON decoding error. Is the API url correct ?"})
        return render(
            request,
            "webshop/data_table_content.html",
            {"error": "JSON decoding error. Is the API url correct ?"},
        )

    orders = []

    for orders_json in response_json:
        products = ""
        for product in orders_json["products"]:
            if products == "":
                products += str(product["id"])
            else:
                products += f", {product['id']}"

        order = {
            "id": orders_json["id"],
            "created_at": orders_json["createdAt"],
            "customer_id": orders_json["customerId"],
            "products": products,
        }
        orders.append(order)

    context = {"objects": orders}

    return render(request, "webshop/data_table_content.html", context)


def update_order(request: Any, id: int) -> HttpResponse:
    error = ""
    if request.method == "POST":
        try:
            data = {
                "client_id": request.POST.get("customer_id"),
                "product_id": request.POST.get("products"),
            }

            response = requests.patch(
                f"{API_SETTINGS['order']['url']}/{id}", params=data, headers=HEADERS
            )
            print("Data: \n", request.POST)
            print("Response: \n", response)
            print("Content: \n", response.content)

            if response.status_code != 200:
                print("Data: \n", request.POST)
                print("Response: \n", response)
                error = "Error in the order update"

            # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
        except requests.exceptions.ConnectionError:
            print({"error": "Connection failed. Is the API server running ?"})
            error = "Connection failed. Is the API server running ?"

    fields = {
        "customer_id": {
            "label": "ID Client",
            "type": "text",
        },
        "products": {
            "label": "Produits",
            "type": "text",
        },
    }

    return render(
        request,
        "webshop/update.html",
        {
            "action_id": id,
            "fields": fields,
            "error": error,
            "heading": "Modifier une commande",
            "cancel_href": "/orders/",
            "submit_text": "Modifier",
        },
    )


@require_http_methods(["DELETE"])
def delete_order(request: Any, id: int) -> HttpResponse:
    try:
        data = {"id": id}

        requests.delete(
            f"{API_SETTINGS['order']['url']}/", params=data, headers=HEADERS
        )
    # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        print({"error": "Connection failed. Is the API server running ?"})
        return HttpResponse('<p class="error callout" id="response-msg">Erreur</p>')

    return HttpResponse(
        {f"<p class='success callout' id='response-msg'>Commande {id} supprimée</p>"}
    )

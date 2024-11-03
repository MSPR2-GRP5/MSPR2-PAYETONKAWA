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
    "X-API-Key": API_SETTINGS["product"]["api_key"],
}


def index_product(request: Any) -> HttpResponse:
    context = {
        "heading": "Produits",
        "table_headers": ["ID", "Nom", "Description", "Couleur", "Price", "Stock", ""],
        "search_form": {
            "inputs": [
                {
                    "id": "search-name",
                    "label": "Nom",
                    "placeholder": "Canard",
                },
                {
                    "id": "search-desc",
                    "label": "Description",
                    "placeholder": "Plastique",
                },
                {
                    "id": "search-color",
                    "label": "Couleur",
                    "placeholder": "Jaune",
                },
            ]
        },
    }
    return render(request, "webshop/index.html", context)


def create_product(request: Any) -> HttpResponse:
    error = ""
    if request.method == "POST":
        try:
            data = {
                "add_name": request.POST.get("name"),
                "add_desc": request.POST.get("desc"),
                "add_color": request.POST.get("color"),
                "add_price": request.POST.get("price"),
                "add_stock": request.POST.get("stock"),
            }
            response = requests.post(
                f"{API_SETTINGS['product']['url']}/", params=data, headers=HEADERS
            )
            print("Data: \n", request.POST)
            print("HEADERS: \n", HEADERS)
            print("Response: \n", response)
            print("Content: \n", response.content)

            if response.status_code != 200:
                print("Data: \n", request.POST)
                print("Response: \n", response)
                error = "Error in the product creation"
            else:
                return redirect("index_product")

            # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
        except requests.exceptions.ConnectionError:
            print({"error": "Connection failed. Is the API server running ?"})
            error = "Connection failed. Is the API server running ?"

    fields = {
        "name": {
            "label": "Nom",
            "type": "text",
        },
        "desc": {
            "label": "Description",
            "type": "text",
        },
        "color": {
            "label": "Couleur",
            "type": "text",
        },
        "price": {
            "label": "Prix",
            "type": "number",
        },
        "stock": {
            "label": "Stock",
            "type": "number",
        },
    }

    return render(
        request,
        "webshop/update.html",
        {
            "action_id": id,
            "fields": fields,
            "error": error,
            "heading": "Créer un produit",
            "cancel_href": "/products/",
            "submit_text": "Créer",
        },
    )


@require_http_methods(["POST"])
def find_product(request: Any, product_id: int) -> HttpResponse:
    return HttpResponse({"success": f"Produit {product_id} trouvé"})


@require_http_methods(["POST"])
def find_product_by(request: Any) -> HttpResponse:
    try:
        if request.POST.get("search-id"):
            product_id = int(request.POST.get("search-id", ""))
            response = requests.get(
                f'{API_SETTINGS["product"]["url"]}/{product_id}', headers=HEADERS
            )
        else:
            data = {
                "search_name": request.POST.get("search-name", ""),
                "search_desc": request.POST.get("search-desc", ""),
                "search_color": request.POST.get("search-desc", ""),
            }

            response = requests.get(
                f"{API_SETTINGS['product']['url']}/", params=data, headers=HEADERS
            )

        print("Response: \n", response)
        print("Content: \n", response.content)
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
        print("Response JSON:\n", response_json)
    except json.JSONDecodeError:
        print({"error": "JSON decoding error. Is the API url correct ?"})
        return render(
            request,
            "webshop/data_table_content.html",
            {"error": "JSON decoding error. Is the API url correct ?"},
        )

    products = []

    for product_json in response_json:
        product = {
            "id": product_json["id"],
            "name": product_json["name"],
            "desc": product_json["description"],
            "color": product_json["color"],
            "price": product_json["price"],
            "stock": product_json["stock"],
        }
        products.append(product)

    context = {"objects": products}

    return render(request, "webshop/data_table_content.html", context)


@require_http_methods(["GET"])
def find_all_products(request: Any) -> HttpResponse:
    try:
        response = requests.get(API_SETTINGS["product"]["url"], headers=HEADERS)
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

    products = []

    for product_json in response_json:
        product = {
            "id": product_json["id"],
            "name": product_json["name"],
            "desc": product_json["description"],
            "color": product_json["color"],
            "price": product_json["price"],
            "stock": product_json["stock"],
        }
        products.append(product)

    context = {"objects": products}

    return render(request, "webshop/data_table_content.html", context)


def update_product(request: Any, id: int) -> HttpResponse:
    error = ""
    if request.method == "POST":
        try:
            data = {
                "id": id,
                "update_name": request.POST.get("name"),
                "update_desc": request.POST.get("desc"),
                "update_color": request.POST.get("color"),
                "update_price": request.POST.get("price"),
                "update_stock": request.POST.get("stock"),
            }

            response = requests.patch(
                f"{API_SETTINGS['product']['url']}/", params=data, headers=HEADERS
            )
            print("Data: \n", request.POST)
            print("Response: \n", response)
            print("Content: \n", response.content)

            if response.status_code != 200:
                print("Data: \n", request.POST)
                print("Response: \n", response)
                error = "Error in the customer creation"

            # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
        except requests.exceptions.ConnectionError:
            print({"error": "Connection failed. Is the API server running ?"})
            error = "Connection failed. Is the API server running ?"

    try:
        response = requests.get(
            f"{API_SETTINGS['product']['url']}/{id}", headers=HEADERS
        )
        # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        print({"error": "Connection failed. Is the API server running ?"})
        error = "Connection failed. Is the API server running ?"

    try:
        response_json = response.json()[0]
    except json.JSONDecodeError:
        print({"error": "JSON decoding error. Is the API url correct ?"})
        error = "JSON decoding error. Is the API url correct ?"

    fields = {
        "name": {
            "label": "Nom",
            "type": "text",
            "value": response_json["name"],
        },
        "desc": {
            "label": "Description",
            "type": "text",
            "value": response_json["description"],
        },
        "color": {
            "label": "Couleur",
            "type": "text",
            "value": response_json["color"],
        },
        "price": {
            "label": "Prix",
            "type": "number",
            "value": response_json["price"],
        },
        "stock": {
            "label": "Stock",
            "type": "number",
            "value": response_json["stock"],
        },
    }

    return render(
        request,
        "webshop/update.html",
        {
            "action_id": id,
            "fields": fields,
            "error": error,
            "heading": "Modifier un produit",
            "cancel_href": "/products/",
            "submit_text": "Modifier",
        },
    )


@require_http_methods(["DELETE"])
def delete_product(request: Any, id: int) -> HttpResponse:
    try:
        data = {
            "id": id,
        }

        requests.delete(
            f"{API_SETTINGS['product']['url']}/", params=data, headers=HEADERS
        )
        # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        print({"error": "Connection failed. Is the API server running ?"})
        return HttpResponse('<p class="error callout" id="response-msg">Erreur</p>')

    return HttpResponse(
        {f"<p class='success callout' id='response-msg'>Produit {id} supprimé</p>"}
    )

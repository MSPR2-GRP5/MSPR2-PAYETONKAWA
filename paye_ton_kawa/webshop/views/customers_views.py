import json
from pathlib import Path
from typing import Any, Final

import environ
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

env = environ.Env()
env.read_env(str(Path(__file__).resolve().parent.parent / ".env"))

API_SETTINGS: Final[dict[str, dict[str, str]]] = {
    "customer": {"api_key": env("API_TOKEN_CUSTOMER"), "url": "http://localhost:8001/customers"},
    "product": {"api_key": "", "url": "http://localhost:8002/api/product"},
    "order": {"api_key": "", "url": "http://localhost:8003/api/order"},
}

HEADERS = {
    "accept": "application/json",
    "X-API-Key": API_SETTINGS["customer"]["api_key"],
}


def index_customer(request: Any) -> HttpResponse:
    context = {
        "heading": "Clients",
        "search_form": {
            "label": "Rechercher un client",
            "placeholder": "Jean Michel"
        },
        "table_headers": [
            "ID", "Nom", "Prénom", "Pseudonyme", "Code Postal", "Ville", "Companie", ""
        ]
    }
    return render(request, "webshop/index.html", context)


@require_http_methods(['POST'])
def create_customer(request: Any, attr: dict[str, Any]) -> HttpResponse:
    return HttpResponse({"success": f"CLient {attr['name']} créé"})


@require_http_methods(['POST'])
def find_customer(request: Any, customer_id: int) -> HttpResponse:
    return HttpResponse({"success": f"CLient {customer_id} trouvé"})


@require_http_methods(['POST'])
def find_customer_by(request: Any, attr: dict[str, Any]) -> HttpResponse:
    return HttpResponse({"success": f"CLient {attr['name']} trouvé"})


@require_http_methods(['GET'])
def find_all_customers(request: Any) -> HttpResponse:
    try:
        response = requests.get(API_SETTINGS["customer"]["url"], headers=HEADERS)
    # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        print({"error": "Connection failed. Is the API server running ?"})
        return render(request, "webshop/data_table_content.html", {"error": "Connection failed. Is the API server running ?"})

    try:
        response_json = response.json()
    except json.JSONDecodeError:
        print({"error": "JSON decoding error. Is the API url correct ?"})
        return render(request, "webshop/data_table_content.html", {"error": "JSON decoding error. Is the API url correct ?"})

    customers = []

    for customer_json in response_json:
        customer = {
            "id": customer_json["id"],
            "last_name": customer_json["last_name"],
            "first_name": customer_json["first_name"],
            "username": customer_json["username"],
            "postal_code": customer_json["address"]["postal_code"],
            "city": customer_json["address"]["city"],
            "company": customer_json["company"]["company_name"]
        }
        customers.append(customer)

    context = {"objects": customers}

    return render(request, "webshop/data_table_content.html", context)


@require_http_methods(['POST'])
def update_customer(request: Any, customer_id: int) -> HttpResponse:
    return HttpResponse({"success": f"CLient {customer_id} mis à jour"})


@require_http_methods(['POST'])
def delete_customer(request: Any, customer_id: int) -> HttpResponse:
    return HttpResponse({"success": f"CLient {customer_id} supprimé"})

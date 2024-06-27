import json
from pathlib import Path
from typing import Any, Final

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

import environ
import requests


env = environ.Env()
env.read_env(str(Path(__file__).resolve().parent.parent / ".env"))


def index_customer(request: Any) -> HttpResponse:
    API_SETTINGS: Final[dict[str, dict[str, str]]] = {
        "customer": {"api_key": env("API_TOKEN_CUSTOMER"), "url": "http://localhost:8001/customers"},
        "product": {"api_key": "", "url": "http://localhost:8002/api/product"},
        "order": {"api_key": "", "url": "http://localhost:8003/api/order"},
    }

    headers = {
        "accept": "application/json",
        "X-API-Key": API_SETTINGS["customer"]["api_key"],
    }

    try:
        response = requests.get(API_SETTINGS["customer"]["url"], headers=headers)
        print(response)
    # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        print({"error": "Connection failed. Is the API server running ?"})
        return HttpResponse("aled")

    try:
        response_json = response.json()
        print(response_json)
    except json.JSONDecodeError:
        print({"error": "JSON decoding error. Is the API url correct ?"})

    context = {
        "heading": "Clients",
        "search_form": {
            "label": "Rechercher un client",
            "placeholder": "Jean Michel"
        },
        "table_headers": [
            "Nom", "Prénom", "Pseudonyme", "Code Postal", "Ville", "Companie"
        ],
        "objects": []
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


def find_all_customers(request: Any) -> HttpResponse:
    return HttpResponse({"success": "CLients trouvés"})


@require_http_methods(['POST'])
def update_customer(request: Any, customer_id: int) -> HttpResponse:
    return HttpResponse({"success": f"CLient {customer_id} mis à jour"})


@require_http_methods(['POST'])
def delete_customer(request: Any, customer_id: int) -> HttpResponse:
    return HttpResponse({"success": f"CLient {customer_id} supprimé"})

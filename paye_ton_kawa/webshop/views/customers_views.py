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


def create_customer(request: Any) -> HttpResponse:
    error = ""
    if request.method == "POST":
        try:
            data = {
                "Nom": request.POST.get("last_name", ""),
                "Prenom": request.POST.get("first_name"),
                "username": request.POST.get("username"),
                "adresse_code": request.POST.get("postal_code"),
                "adresse_city": request.POST.get("city"),
                "first_name": request.POST.get("profile_first_name"),
                "last_name": request.POST.get("profile_last_name"),
                "company": request.POST.get("city")
            }
            response = requests.post(f"{API_SETTINGS['customer']['url']}/", params=data, headers=HEADERS)
            print("Data: \n", request.POST)
            print("Response: \n", response)
            print("Content: \n", response.content)

            if response.status_code != 200:
                print("Data: \n", request.POST)
                print("Response: \n", response)
                error = "Error in the customer creation"
            else:
                return redirect("index_customer")

            # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
        except requests.exceptions.ConnectionError:
            print({"error": "Connection failed. Is the API server running ?"})
            error = "Connection failed. Is the API server running ?"

    fields = {
        "last_name": {
            "label": "Nom",
            "type": "text",
        },
        "first_name": {
            "label": "Prénom",
            "type": "text",
        },
        "username": {
            "label": "Pseudonyme",
            "type": "text",
        },
        "postal_code": {
            "label": "Code Postal",
            "type": "number",
        },
        "city": {
            "label": "Ville",
            "type": "text",
        },
        "company": {
            "label": "Companie",
            "type": "text",
        },
        "profile_last_name": {
            "label": "Nom de profile",
            "type": "text",
        },
        "profile_first_name": {
            "label": "Prenom de profile",
            "type": "text",
        },
    }

    return render(request, "webshop/update_customer.html", {
        "customer_id": id,
        "fields": fields,
        "error": error,
        "heading": "Créer un client",
        "submit_text": "Créer",
    })


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
        return render(request, "webshop/data_table_content.html",
                      {"error": "Connection failed. Is the API server running ?"})

    try:
        response_json = response.json()
    except json.JSONDecodeError:
        print({"error": "JSON decoding error. Is the API url correct ?"})
        return render(request, "webshop/data_table_content.html",
                      {"error": "JSON decoding error. Is the API url correct ?"})

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


def update_customer(request: Any, id: int) -> HttpResponse:
    error = ""
    if request.method == "POST":
        try:
            data = {
                "Nom": request.POST.get("last_name", ""),
                "Prenom": request.POST.get("first_name"),
                "adresse_code": request.POST.get("postal_code"),
                "city": request.POST.get("city")
            }
            response = requests.patch(f"{API_SETTINGS['customer']['url']}/{id}", params=data, headers=HEADERS)
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
        response = requests.get(f"{API_SETTINGS['customer']['url']}/{id}", headers=HEADERS)
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
        "id": {
            "label": "ID",
            "type": "number",
            "value": response_json["id"]
        },
        "last_name": {
            "label": "Nom",
            "type": "text",
            "value": response_json["last_name"],
        },
        "first_name": {
            "label": "Prénom",
            "type": "text",
            "value": response_json["first_name"],
        },
        "username": {
            "label": "Pseudonyme",
            "type": "text",
            "value": response_json["username"],
        },
        "postal_code": {
            "label": "Code Postal",
            "type": "number",
            "value": response_json["address"]["postal_code"],
        },
        "city": {
            "label": "Ville",
            "type": "text",
            "value": response_json["address"]["city"],
        },
        "company": {
            "label": "Companie",
            "type": "text",
            "value": response_json["company"]["company_name"]
        },
        "profile_last_name": {
            "label": "Nom de profile",
            "type": "text",
            "value": response_json["profile"]["last_name"]
        },
        "profile_first_name": {
            "label": "Nom de profile",
            "type": "text",
            "value": response_json["profile"]["last_name"]
        },
    }

    return render(request, "webshop/update_customer.html", {
        "customer_id": id,
        "fields": fields,
        "error": error,
        "heading": "Editer un client",
        "submit_text": "Modifier"
    })


@require_http_methods(['DELETE'])
def delete_customer(request: Any, id: int) -> HttpResponse:
    try:
        requests.delete(API_SETTINGS["customer"]["url"] + f"/{id}", headers=HEADERS)
    # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        print({"error": "Connection failed. Is the API server running ?"})
        return HttpResponse('<p class="error callout" id="response-msg">Erreur</p>')

    return HttpResponse({f"<p class='success callout' id='response-msg'>CLient {id} supprimé</p>"})

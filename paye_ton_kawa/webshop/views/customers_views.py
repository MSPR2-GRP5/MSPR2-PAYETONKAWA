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
    "X-API-Key": API_SETTINGS["customer"]["api_key"],
}


def index_customer(request: Any) -> HttpResponse:
    context = {
        "heading": "Clients",
        "table_headers": [
            "ID",
            "Nom",
            "Prénom",
            "Pseudonyme",
            "Code Postal",
            "Ville",
            "Companie",
            "",
        ],
        "search_form": {
            "inputs": [
                {
                    "id": "search-last-name",
                    "label": "Nom",
                    "placeholder": "DUPONT",
                },
                {
                    "id": "search-first-name",
                    "label": "Prénom",
                    "placeholder": "Jean",
                },
                {
                    "id": "search-postal-code",
                    "label": "Code Postal",
                    "placeholder": "38100",
                },
            ]
        },
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
                "company": request.POST.get("city"),
            }
            response = requests.post(
                f"{API_SETTINGS['customer']['url']}/", params=data, headers=HEADERS
            )
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

    return render(
        request,
        "webshop/update.html",
        {
            "action_id": id,
            "fields": fields,
            "error": error,
            "heading": "Créer un client",
            "cancel_href": "/customers/",
            "submit_text": "Créer",
        },
    )


@require_http_methods(["POST"])
def find_customer(request: Any) -> HttpResponse:
    return HttpResponse("find_customer")


@require_http_methods(["POST"])
def find_customer_by(request: Any) -> HttpResponse:
    print("find by")
    print("Data: \n", request.POST)
    try:
        if request.POST.get("search-id"):
            customer_id = int(request.POST.get("search-id", ""))
            response = requests.get(
                f'{API_SETTINGS["customer"]["url"]}/{customer_id}', headers=HEADERS
            )
        else:
            postal_code = request.POST.get("search-postal-code")
            data = {
                "Nom": request.POST.get("search-last-name", ""),
                "Prenom": request.POST.get("search-first-name", ""),
                "postal_code": int(postal_code) if postal_code != "" else 0,
            }

            response = requests.get(
                f"{API_SETTINGS['customer']['url']}/", params=data, headers=HEADERS
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

    customers = []

    for customer_json in response_json:
        customer = {
            "id": customer_json["id"],
            "last_name": customer_json["last_name"],
            "first_name": customer_json["first_name"],
            "username": customer_json["username"],
            "postal_code": customer_json["address"]["postal_code"],
            "city": customer_json["address"]["city"],
            "company": customer_json["company"]["company_name"],
        }
        customers.append(customer)

    context = {"objects": customers}

    return render(request, "webshop/data_table_content.html", context)


@require_http_methods(["GET"])
def find_all_customers(request: Any) -> HttpResponse:
    try:
        response = requests.get(API_SETTINGS["customer"]["url"], headers=HEADERS)
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

    customers = []

    for customer_json in response_json:
        customer = {
            "id": customer_json["id"],
            "last_name": customer_json["last_name"],
            "first_name": customer_json["first_name"],
            "username": customer_json["username"],
            "postal_code": customer_json["address"]["postal_code"],
            "city": customer_json["address"]["city"],
            "company": customer_json["company"]["company_name"],
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
                "city": request.POST.get("city"),
            }
            response = requests.patch(
                f"{API_SETTINGS['customer']['url']}/{id}", params=data, headers=HEADERS
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
            f"{API_SETTINGS['customer']['url']}/{id}", headers=HEADERS
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
        "id": {"label": "ID", "type": "number", "value": response_json["id"]},
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
            "value": response_json["company"]["company_name"],
        },
        "profile_last_name": {
            "label": "Nom de profile",
            "type": "text",
            "value": response_json["profile"]["last_name"],
        },
        "profile_first_name": {
            "label": "Nom de profile",
            "type": "text",
            "value": response_json["profile"]["last_name"],
        },
    }

    return render(
        request,
        "webshop/update.html",
        {
            "customer_id": id,
            "fields": fields,
            "error": error,
            "heading": "Modifier un client",
            "cancel_href": "/customers/",
            "submit_text": "Modifier",
        },
    )


@require_http_methods(["DELETE"])
def delete_customer(request: Any, id: int) -> HttpResponse:
    try:
        requests.delete(API_SETTINGS["customer"]["url"] + f"/{id}", headers=HEADERS)
    # The error returned is not the standard ConnectionError, it is a specific requests error with the same name
    except requests.exceptions.ConnectionError:
        print({"error": "Connection failed. Is the API server running ?"})
        return HttpResponse('<p class="error callout" id="response-msg">Erreur</p>')

    return HttpResponse(
        {f"<p class='success callout' id='response-msg'>CLient {id} supprimé</p>"}
    )

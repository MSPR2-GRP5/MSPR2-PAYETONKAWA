from typing import Any

from django.http import HttpResponse
from django.shortcuts import render

from webshop.EntityManager import EntityManager


def index(request: Any) -> HttpResponse:
    customers = EntityManager.get_all("customer")
    products = EntityManager.get_all("product")
    orders = EntityManager.get_all("order")

    return render(
        request,
        "webshop/index.html",
        {"customers": customers, "products": products, "orders": orders},
    )

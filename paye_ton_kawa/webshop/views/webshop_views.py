from typing import Any

from django.http import HttpResponse
from django.shortcuts import render

from webshop.EntityManager import EntityManager


def index(request: Any) -> HttpResponse:
    return render(request, "webshop/home.html")

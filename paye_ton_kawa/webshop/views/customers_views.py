from typing import Any

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


def index_customer(request: Any) -> HttpResponse:
    return HttpResponse("<h1>Customers</h1>")

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

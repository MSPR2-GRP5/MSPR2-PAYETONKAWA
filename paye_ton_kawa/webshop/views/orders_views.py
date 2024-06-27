from typing import Any

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


def index_order(request: Any) -> HttpResponse:
    return HttpResponse("<h1>orders</h1>")


@require_http_methods(['POST'])
def create_order(request: Any, attr: dict[str, Any]) -> HttpResponse:
    return HttpResponse({"success": f"Commande {attr['name']} créé"})


@require_http_methods(['POST'])
def find_order(request: Any, order_id: int) -> HttpResponse:
    return HttpResponse({"success": f"Commande {order_id} trouvé"})


@require_http_methods(['POST'])
def find_order_by(request: Any, attr: dict[str, Any]) -> HttpResponse:
    return HttpResponse({"success": f"Commande {attr['name']} trouvé"})


def find_all_orders(request: Any) -> HttpResponse:
    return HttpResponse({"success": "Commandes trouvés"})


@require_http_methods(['POST'])
def update_order(request: Any, order_id: int) -> HttpResponse:
    return HttpResponse({"success": f"Commande {order_id} mis à jour"})


@require_http_methods(['POST'])
def delete_order(request: Any, order_id: int) -> HttpResponse:
    return HttpResponse({"success": f"Commande {order_id} supprimé"})

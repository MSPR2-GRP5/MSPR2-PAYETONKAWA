from typing import Any

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


def index_product(request: Any) -> HttpResponse:
    return HttpResponse("<h1>products</h1>")

@require_http_methods(['POST'])
def create_product(request: Any, attr: dict[str, Any]) -> HttpResponse:
    return HttpResponse({"success": f"Produit {attr['name']} créé"})


@require_http_methods(['POST'])
def find_product(request: Any, product_id: int) -> HttpResponse:
    return HttpResponse({"success": f"Produit {product_id} trouvé"})


@require_http_methods(['POST'])
def find_product_by(request: Any, attr: dict[str, Any]) -> HttpResponse:
    return HttpResponse({"success": f"Produit {attr['name']} trouvé"})


def find_all_products(request: Any) -> HttpResponse:
    return HttpResponse({"success": "Produits trouvés"})


@require_http_methods(['POST'])
def update_product(request: Any, product_id: int) -> HttpResponse:
    return HttpResponse({"success": f"Produit {product_id} mis à jour"})


@require_http_methods(['POST'])
def delete_product(request: Any, product_id: int) -> HttpResponse:
    return HttpResponse({"success": f"Produit {product_id} supprimé"})

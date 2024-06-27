from django.urls import include, path, URLPattern

from .views import *


def get_crud_patterns(path_root: str) -> list[URLPattern]:
    views_modules = {
        "customer": customers_views,
        "order": orders_views,
        "product": products_views
    }

    return [
        path("", getattr(views_modules[path_root], f"index_{path_root}"), name=f"index_{path_root}"),
        path("create/", getattr(views_modules[path_root], f"create_{path_root}"), name=f"create_{path_root}"),
        path("find/", getattr(views_modules[path_root], f"find_{path_root}"), name=f"find_{path_root}"),
        path("find-by/", getattr(views_modules[path_root], f"find_{path_root}_by"), name=f"find_{path_root}_by"),
        path("find-all/", getattr(views_modules[path_root], f"find_all_{path_root}s"), name=f"find_all_{path_root}s"),
        path("update/", getattr(views_modules[path_root], f"update_{path_root}"), name=f"update_{path_root}"),
        path("delete/", getattr(views_modules[path_root], f"delete_{path_root}"), name=f"delete_{path_root}"),
    ]


urlpatterns = [
    path("customers/", include(get_crud_patterns("customer"))),
    path("orders/", include(get_crud_patterns("order"))),
    path("products/", include(get_crud_patterns("product"))),
    path("home/", webshop_views.index, name="index")
]

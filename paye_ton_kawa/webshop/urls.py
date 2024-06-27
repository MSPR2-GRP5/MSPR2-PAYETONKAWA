from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("customer/create", views.index, name="create_customer"),
    path("customer/find", views.index, name="find_customer"),
    path("customer/find-by", views.index, name="find_customer"),
    path("customer/find-all", views.index, name="find_all_customers"),
    path("customer/update", views.index, name="update_customer"),
    path("customer/delete", views.index, name="delete_customer"),
]

from django.urls import path
from . import views

urlpatterns = [
    # Products
    path("products/", views.product_list, name="api_product_list"),

    # Categories
    path("categories/", views.category_list, name="api_category_list"),

    # Cart
    path("cart/", views.cart_items_api, name="api_cart_items"),
    path("cart/add/", views.add_to_cart_api, name="api_add_to_cart"),

    # Orders
    path("orders/", views.order_list_api, name="api_order_list"),
]

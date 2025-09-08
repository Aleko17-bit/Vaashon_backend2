from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update-quantity/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/update-size/<int:item_id>/', views.update_cart_size, name='update_cart_size'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),

    # Terms & Privacy
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),

    # API
    path('api/products/', views.product_list, name='api_products'),
    path('api/categories/', views.category_list, name='api_categories'),
    path('api/cart/', views.cart_items_api, name='api_cart'),
    path('api/cart/add/', views.add_to_cart_api, name='api_add_to_cart'),
    path('api/orders/', views.order_list_api, name='api_orders'),

    # MPESA
    path('mpesa/stkpush/', views.stk_push, name='stk_push'),
    path('mpesa/callback/', views.daraja_callback, name='daraja_callback'),
]

from django.urls import path
from . import product_views, product_pages

urlpatterns = [
    path('products/', product_views.list_products),
    path('products/<int:pk>/', product_views.retrieve_product),
    path('cart/add/', product_views.add_to_cart),
    path('cart/', product_views.view_cart),
    path('checkout/', product_views.checkout),

    path('products/page/', product_pages.product_list_page),
    path('cart/page/', product_pages.cart_page),
    path('checkout/page/', product_pages.checkout_page),
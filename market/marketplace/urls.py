from django.urls import path
from . import views
from marketplace.views import add_to_cart, cart_detail, remove_from_cart, remove_one

urlpatterns = [
    path("categorias/", views.category_list, name="category_list"),
    path("categorias/nova/", views.category_create, name="category_create"),
    path("produtos/", views.product_list, name="product_list"),
    path("produtos/novo/", views.product_create, name="product_create"),
    path('categorias/nova/', views.category_create, name='category_create'),
    path("produto/<int:pk>/", views.product_detail, name="product_detail"),
    path("carrinho/", cart_detail, name="cart_detail"),
    path("carrinho/adicionar/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("carrinho/remover/<int:pk>/", remove_from_cart, name="remove_from_cart"),
    path("carrinho/", cart_detail, name="cart_detail"),
    path("carrinho/remover-um/<int:product_id>/", remove_one, name="remove_one"),
]

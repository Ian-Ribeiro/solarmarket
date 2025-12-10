from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import CategoryForm, ProductForm
from .models import Categoria, Produto
from .cart import Cart


# Categorias.

def category_list(request):
    categories = Categoria.objects.all()
    return render(request, "marketplace/category_list.html", {"categories": categories})


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm()

    return render(request, "marketplace/category_form.html", {"form": form})


# Produtos.

def product_list(request):
    products = Produto.objects.all()
    return render(request, "marketplace/product_list.html", {"products": products})


def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "marketplace/product_form.html", {"form": form})


def product_detail(request, pk):
    product = get_object_or_404(Produto, pk=pk)
    return render(request, "marketplace/product_detail.html", {"product": product})


# Carrinho de compras.

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect("cart_detail")


def remove_one(request, product_id):
    cart = Cart(request)
    cart.remove_one(product_id)
    return redirect("cart_detail")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "marketplace/cart_detail.html", {"cart": cart})

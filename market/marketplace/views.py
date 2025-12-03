from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import CategoryForm, ProductForm
from .models import Categoria, Produto, Cart, CartItem
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required



def category_list(request):
    categories = Categoria.objects.all()
    return render(request, "marketplace/category_list.html", {"categories": categories})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("category_list")
    return render(request, "marketplace/category_form.html", {"form": form})

def product_list(request):
    products = Produto.objects.all()
    return render(request, "marketplace/product_list.html", {"products": products})

def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "marketplace/product_form.html", {"form": form})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # ou onde quiser
    else:
        form = CategoryForm()

    return render(request, 'marketplace/category_form.html', {'form': form})

def product_detail(request, pk):
    products = get_object_or_404(Produto, pk=pk)
    return render(request, "marketplace/product_detail.html", {"products": products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Produto, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    # Verifica se já existe item no carrinho
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart_detail')

@login_required
def remove_one(request, product_id):
    product = get_object_or_404(Produto, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        return redirect('cart_detail')

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "marketplace/cart_detail.html", {"cart": cart})


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    item.delete()
    return redirect("cart_detail")

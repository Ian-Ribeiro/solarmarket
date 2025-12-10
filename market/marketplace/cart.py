from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from .models import Produto


class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)

        if cart is None:
            cart = self.session[self.SESSION_KEY] = {}

        self.cart = cart

    # Adicionar item ao carrinho.
    def add(self, product_id, quantity=1):
        """Adiciona um produto ao carrinho usando o ID dele."""
        pid = str(product_id)

        try:
            product = Produto.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            return

        item = self.cart.get(pid)

        if item:
            item["quantity"] += quantity
        else:
            self.cart[pid] = {
                "name": product.nome,
                "price": str(product.preco),
                "quantity": quantity,
                "image": product.imagem.url if product.imagem else "",
            }

        self.save()

    # Atualizar quantidade de item no carrinho.
    def update(self, product_id, quantity):
        """Atualiza a quantidade de um item."""
        pid = str(product_id)

        if pid in self.cart:
            if quantity <= 0:
                del self.cart[pid]
            else:
                self.cart[pid]["quantity"] = quantity

            self.save()

    # Remover uma unidade do item.
    def remove_one(self, product_id):
        pid = str(product_id)

        if pid in self.cart:
            self.cart[pid]["quantity"] -= 1

            if self.cart[pid]["quantity"] <= 0:
                del self.cart[pid]

            self.save()

    # Remover item do carrinho.
    def remove(self, product_id):
        pid = str(product_id)

        if pid in self.cart:
            del self.cart[pid]
            self.save()

    # Limpar carrinho.
    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True
        self.cart = {}

    # Salvar alterações no carrinho.
    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    # Iterar sobre itens no carrinho.
    def __iter__(self):
        """Itera sobre itens incluindo dados reais do model."""
        product_ids = self.cart.keys()
        products = Produto.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        for pid, data in self.cart.items():
            product = product_map.get(pid)

            if product is None:
                continue

            price = Decimal(data["price"])
            quantity = data["quantity"]

            yield {
                "product": product,
                "quantity": quantity,
                "price": price,
                "subtotal": price * quantity,
                "image": data.get("image", ""),
            }

    # Total do carrinho.
    def get_total(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    # Contar itens no carrinho.
    def count(self):
        return sum(item["quantity"] for item in self.cart.values())
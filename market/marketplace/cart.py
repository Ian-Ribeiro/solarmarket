from decimal import Decimal
from .models import Produto

class Cart:
    SESSION_KEY = 'cart'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if not cart:
            cart = self.session[self.SESSION_KEY] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        pid = str(product_id)
        product = Produto.objects.get(pk=product_id)

        if pid in self.cart:
            self.cart[pid]['quantity'] += quantity
        else:
            self.cart[pid] = {
                'name': product.nome,
                'price': str(product.preco),
                'quantity': quantity,
                'image': product.imagem.url if product.imagem else ''
            }
        self.save()

    def remove_one(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            self.cart[pid]['quantity'] -= 1
            if self.cart[pid]['quantity'] <= 0:
                del self.cart[pid]
            self.save()

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        products = Produto.objects.filter(id__in=self.cart.keys())
        products_map = {str(p.id): p for p in products}

        for pid, item in self.cart.items():
            product = products_map.get(pid)
            item_obj = {
                "product": product,
                "quantity": item["quantity"],
                "price": Decimal(item["price"]),
                "subtotal": Decimal(item["price"]) * item["quantity"],
            }
            yield item_obj

    def get_total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

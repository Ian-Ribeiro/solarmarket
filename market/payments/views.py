import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from marketplace.models import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    # Pegando o carrinho do usuário logado
    cart = Cart.objects.get(user=request.user)

    # Criando os line_items automaticamente
    line_items = []

    for item in cart.items.all():
        line_items.append({
            "price_data": {
                "currency": "brl",
                "unit_amount": int(item.product.preco * 100),  # preço em centavos
                "product_data": {
                    "name": item.product.nome,
                },
            },
            "quantity": item.quantity,
        })

    # Criando a sessão de pagamento
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='/payments/sucesso/',
        cancel_url='/payments/cancelado/',
    )

    return redirect(checkout_session.url)


def sucesso(request):
    return render(request, 'payments/sucesso.html')

def cancelado(request):
    return render(request, 'payments/cancelado.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return HttpResponse(status=400)

    # Quando pagamento é concluído
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("Pagamento confirmado:", session.get("id"))

    return HttpResponse(status=200)

import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from marketplace.models import Produto
stripe.api_key = settings.STRIPE_SECRET_KEY


# Função para obter o carrinho da sessão.
def get_session_cart(request):
    return request.session.get("cart", {})
    

# Criar sessão de checkout no Stripe.
@require_POST
def create_checkout_session(request):

    cart = get_session_cart(request)

    if not cart:
        return redirect("/marketplace/carrinho/")

    line_items = []

    for product_id, item in cart.items():
        
        try:
            product = Produto.objects.get(id=product_id)
        except Produto.DoesNotExist:
            continue

        line_items.append({
            "price_data": {
                "currency": "brl",
                "unit_amount": int(product.preco * 100),
                "product_data": {
                    "name": product.nome,
                },
            },
            "quantity": item["quantity"],
        })

    # Criando sessão no Stripe
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri("/payments/sucesso/"),
        cancel_url=request.build_absolute_uri("/payments/cancelado/"),
        customer_email=request.user.email,
    )

    return redirect(checkout_session.url)


# Telas de sucesso e cancelamento.
def sucesso(request):
    return render(request, "payments/sucesso.html")


def cancelado(request):
    return render(request, "payments/cancelado.html")


# Webhook do Stripe para confirmar pagamento.
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("Pagamento confirmado:", session.get("id"))

    return HttpResponse(status=200)

# Nova versão do webhook com envio de e-mail.
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

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        email_cliente = session.get("customer_email")

        valor_total = session.get("amount_total", 0) / 100

        pagamento_id = session.get("payment_intent")

        # Enviar e-mail de confirmação.

        from django.core.mail import EmailMessage

        assunto = "Confirmação de Pagamento - Seu Pedido"
        mensagem = (
            f"Olá!\n\n"
            f"Seu pagamento foi confirmado com sucesso.\n\n"
            f"Valor pago: R$ {valor_total:.2f}\n"
            f"ID da transação: {pagamento_id}\n\n"
            f"Obrigado pela compra!\n"
        )

        email = EmailMessage(
            subject=assunto,
            body=mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_cliente],
        )

        email.send(fail_silently=False)

    return HttpResponse(status=200)
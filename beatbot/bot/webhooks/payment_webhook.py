from yookassa import Configuration, Webhook

from bot.misc.settings import settings


def create_payment_webhook():
    Configuration.configure_auth_token(settings.yookassa_data['client_secret'])

    response = Webhook.add({
        "event": "payment.succeeded",
        "url": f"https://{settings.IP_ADDRESS}:{settings.WEB_PORT}/handle_payment",
    })

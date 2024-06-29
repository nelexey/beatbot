import json
import uuid

from yookassa import Configuration, Payment

from bot.misc.settings import settings as s

Configuration.account_id = s.YOOKASSA_SHOP_ID
Configuration.secret_key = s.YOOKASSA_SECRET_KEY


async def create_payment(chat_id: int, amount: int) -> dict:
    """
    Create a payment and return the payment object.

    Args:
        chat_id (int): The ID of the chat for which the payment is being created.
        amount (int): The amount of the payment in rubles.

    Returns:
        dict: The payment object as a dictionary.

    Raises:
        YooKassaError: If there is an error creating the payment.

    Docs:
        https://yookassa.ru/developers/api#payment_object
    """
    payment_data = {
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
        },
        "capture": True,
        "description": f"Payment for chat {chat_id}",
        "metadata": {
            "chat_id": chat_id
        }
    }

    payment = Payment.create(payment_data, uuid.uuid4())
    return json.loads(payment.json())

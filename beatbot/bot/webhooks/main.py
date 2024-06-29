from .payment_webhook import create_payment_webhook


def create_all_webhooks() -> None:
    webhooks = (
        create_payment_webhook,
    )

    [webhook() for webhook in webhooks]

import requests
from django.conf import settings


def _base_url() -> str:
    # Revolut Merchant API base (sandbox vs live)
    if settings.REVOLUT_MODE.lower() == "live":
        return "https://merchant.revolut.com/api/1.0"
    return "https://sandbox-merchant.revolut.com/api/1.0"


def create_revolut_order(amount_cents: int, currency: str, merchant_ref: str, success_url: str, cancel_url: str) -> dict:
    url = f"{_base_url()}/orders"
    headers = {
        "Authorization": f"Bearer {settings.REVOLUT_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "amount": amount_cents,
        "currency": currency,
        "merchant_order_ext_ref": merchant_ref,
        "redirect_url": success_url,
        "cancel_url": cancel_url,
    }
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

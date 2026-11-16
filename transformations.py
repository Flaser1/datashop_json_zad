

from decimal import Decimal, InvalidOperation

def normalize_order(raw_order: dict) -> dict:
    order_id = int(raw_order["order_id"])
    if type(order_id) is not int:
        raise TypeError(f"order_id: {order_id} must be int")
    if order_id <= 0:
        raise ValueError(f"order_id: {order_id} must be positive")

    customer = raw_order["customer"]
    if not isinstance(customer, dict):
        raise TypeError(f"customer must be dict")

    customer_id = int(customer["customer_id"])
    if type(customer_id) is not int:
        raise TypeError(f"customer_id: {customer_id} must be int")
    if customer_id <= 0:
        raise ValueError(f"customer_id: {customer_id} must be positive")

    customer_name = customer["name"].strip().title()
    if customer_name == "":
        raise ValueError(f"customer_name: {customer_name} cannot be empty")

    country = customer.get("country")
    if country is None:
        country = "UNKNOWN"
    if not isinstance(country, str):
        raise TypeError("country must be str")
    else:
        country = country.strip().upper() or "UNKNOWN"

    status = raw_order["status"].strip().lower()
    if status not in {"paid", "pending", "cancelled"}:
        raise ValueError(f"Unsupported status: {status!r}")

    try:
        amount = Decimal(raw_order["amount"].strip().replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError(f"Invalid amount: {raw_order["amount"]}") from exc
    if not amount.is_finite() or amount < 0:
        raise ValueError(f"Amount: {amount} must be finite and non-negative")

    is_gift = raw_order.get("is_gift", False)
    if type(is_gift) is not bool:
        raise TypeError(f"is_gift: {is_gift} must be bool")

    raw_tags = raw_order.get("tags")
    if raw_tags is None:
        raw_tags = []
    if not isinstance(raw_tags, list):
        raise TypeError(f"tags must be a list or None")

    tags = set()
    for tag in raw_tags:
        if not isinstance(tag, str):
            raise TypeError(f"tag: {tag!r} must be str")
        clean_tag = tag.strip().lower()
        if clean_tag != "":
            tags.add(clean_tag)

    return {
        "order_id": order_id,
        "customer_id": customer_id,
        "customer_name": customer_name,
        "country": country,
        "status": status,
        "amount": amount,
        "is_gift": is_gift,
        "tags": sorted(tags)
    }

def transform_orders(raw_orders: list[dict], source_file: str) -> tuple[list[dict], list[dict]]:
    clean = []
    rejected = []
    accepted_ids = set()

    for record_number, raw_order in enumerate(raw_orders, start=1):
        try:
            clean_order = normalize_order(raw_order)
            if clean_order["order_id"] in accepted_ids:
                raise ValueError(f"Duplicate order: {raw_order["order_id"]}")
        except (KeyError, ValueError, TypeError) as exc:
            rejected.append({
                "source_file": source_file,
                "record_number": record_number,
                "raw_order_id": raw_order["order_id"],
                "error_type": type(exc).__name__,
                "reason": str(exc)
            })
        else:
            accepted_ids.add(clean_order["order_id"])
            clean.append(clean_order)

    return clean, rejected
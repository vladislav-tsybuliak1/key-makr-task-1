import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def validate_product(data: dict) -> bool:
    required_fields = {"id", "name", "price", "category"}

    if not required_fields.issubset(data.keys()):
        missing_fields = required_fields - data.keys()
        logging.error(
            f"Missing required fields: {missing_fields} in product {data}",
        )
        return False

    try:
        product_id = int(data.get("id"))
        price = float(data.get("price"))

        if product_id <= 0:
            logging.error(
                f"Invalid ID ({product_id}): Must be a positive integer.",
            )
            return False

        if price <= 0:
            logging.error(
                f"Invalid price ({price}): Must be a positive number.",
            )
            return False

        if not isinstance(data["name"], str) or not data["name"].strip():
            logging.error(
                f"Invalid name ({data['name']}): Must be a non-empty string.",
            )
            return False

    except TypeError as e:
        logging.error(f"Type error in product {data}: {e}")
        return False

    return True

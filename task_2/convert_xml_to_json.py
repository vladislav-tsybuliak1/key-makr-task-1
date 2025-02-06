import argparse
import json
import logging
import os
import xml.etree.ElementTree as ET


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename="converting_xml_to_json.log", mode="a"),
        logging.StreamHandler(),
    ],
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
                f"Invalid product name '{data['name']}': Must be a non-empty string.",
            )
            return False

        if not isinstance(data["category"], str) or not data["category"].strip():
            logging.error(
                f"Invalid product category '{data['category']}': Must be a non-empty string.",
            )
            return False

    except (ValueError, TypeError) as e:
        logging.error(f"Error in product {data}: {e}")
        return False

    return True


def convert_xml_to_json(input_dir, output_dir) -> None:
    if not os.path.exists(input_dir):
        logging.warning(f"Directory {input_dir} does not exist.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir(input_dir):
        if not file.endswith(".xml"):
            break

        xml_path = os.path.join(input_dir, file)
        json_path = os.path.join(output_dir, file.replace(".xml", ".json"))

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            product_data = {child.tag: child.text for child in root}

            if validate_product(product_data):
                with open(json_path, "w", encoding="utf-8") as json_file:
                    json.dump(product_data, json_file, indent=2)
                logging.info(f"Converted: {file} to {json_path}.")
            else:
                logging.info(f"Validation failed for: {file}.")

        except ET.ParseError:
            logging.info(f"Error parsing XML: {file}.")

    if not os.listdir(output_dir):
        os.removedirs(output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert XML product files to JSON",
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing XML files",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to save JSON files",
    )

    args = parser.parse_args()
    convert_xml_to_json(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()

data = {
    "products": [
        {
            "id": 1,
            "title": "Product 1",
            "net_cost": 100
        },
        {
            "id": 2,
            "title": "Product 2",
            "net_cost": 200
        }
    ],
    "tax": 0.1,
    "margin": 0.2
}


def calculate_total_price(products: list, tax: float) -> list:
    calculated_products = []
    for product in products:
        calculated_products.append(
            {
                "id": product.get("id"),
                "title": product.get("title"),
                "price": round(product.get("net_cost") + (tax * product.get("net_cost")))
            }
        )

    return calculated_products


def show_output_data(input_data: dict) -> (dict, str):
    products = input_data.get('products')
    tax = input_data.get('tax')
    margin = input_data.get('margin')

    if isinstance(products, list) \
            and isinstance(tax, float) \
            and isinstance(margin, float):
        output_data = {"products": calculate_total_price(products, tax)}
        output_data["total_price"] = sum(list(p.get("price") for p in output_data.get("products"))) / \
                                     len(output_data.get("products"))

        return output_data

    else:
        return "Inappropriate data type"


if __name__ == "__main__":
    if isinstance(data, dict):
        print(show_output_data(data))
    else:
        print("Inappropriate data type")

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


def calculate_total_price(products: list, tax: float, margin: float) -> list:
    calculated_products = []
    for product in products:
        calculated_products.append(
            {
                "id": product.get("id"),
                "title": product.get("title"),
                "price": round(product.get("net_cost") - tax - margin, 2)
            }
        )

    return calculated_products


def show_output_data(input_data: dict) -> dict:

    products = input_data.get('products')
    tax = input_data.get('tax')
    margin = input_data.get('margin')

    output_data = {"products": calculate_total_price(products, tax, margin), "total_price": 0}

    for prod in output_data.get("products"):
        output_data["total_price"] += prod.get("price")

    return output_data


if __name__ == "__main__":
    show_output_data(data)
    print(show_output_data(data))

# Output Data Format

# {
# "products": [
# {
# "id": 0,
# "title": "string",
# "price": 0
# }
# ],
# "total_price": 0
# }

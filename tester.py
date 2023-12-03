import requests

# The base URL for your Flask API
BASE_URL = "http://localhost:5000"

def add_sale(sale_data):
    response = requests.post(f"{BASE_URL}/sales/sale", json=sale_data)
    try:
        return response.json()
    except ValueError:
        return {'error': 'No JSON response', 'status_code': response.status_code}

def get_sales():
    response = requests.get(f"{BASE_URL}/sales")
    return response.json()

def update_sale(product_id, update_data):
    response = requests.put(f"{BASE_URL}/sales/sale/{product_id}", json=update_data)
    return response.json()

def delete_sale(product_id):
    response = requests.delete(f"{BASE_URL}/sales/{product_id}")
    return response.json()

def add_or_update_stock(stock_data):
    response = requests.post(f"{BASE_URL}/stock", json=stock_data)
    try:
        return response.json()
    except ValueError:
        return {'error': 'No JSON response', 'status_code': response.status_code}


def get_stock(product_id=None):
    url = f"{BASE_URL}/stock"
    if product_id:
        url += f"/{product_id}"
    response = requests.get(url)
    try:
        return response.json()
    except ValueError:
        return {'error': 'No JSON response', 'status_code': response.status_code}


# Test stock management
test_stock = {
    "product_id": 1,
    "available": 100,
    "price_bought": 100,
    "purchase_date": "2023-12-01",
    "bought_quantity": 100,
    "extra_expenses_company": 20
}

# Test the API
print("Adding or updating stock...")
print(add_or_update_stock(test_stock))

print("\nGetting stock information...")
print(get_stock())

print("\nGetting stock information for a specific product...")
print(get_stock(1))

# Test sale management
test_sale = {
    "product_id": 1,
    "product_name": "Test Product",
    "shipping_price": 10,
    "marketing_fee": 5,
    "sold_price": 150,
    "sold_quantity": 30,
    "sale_date": "2023-12-05",
    "extra_expenses_customer": 15
}


print("\nAdding a sale...")
print(add_sale(test_sale))

print("\nGetting all sales...")
print(get_sales())

print("\nUpdating a sale...")
print(update_sale(1, {"product_name": "Updated Product"}))

print("\nDeleting a sale...")
print(delete_sale(1))

# Modified test script to include checking stock levels before and after a sale
def test_stock_and_sales_flow():
    product_id = 1

    print("Adding or updating stock...")
    # Example of updated stock data in the test script
    test_stock = {
    "product_id": 1,
    "available": 100,
    "price_bought": 100,
    "purchase_date": "2023-12-01",
    "bought_quantity": 50,
    "extra_expenses_company": 20
}



    print(add_or_update_stock(test_stock))

    print("\nGetting stock information before sale...")
    initial_stock = get_stock(product_id)
    print(initial_stock)

    print("\nAdding a sale...")
    test_sale = {
    "product_id": 1,
    "product_name": "Test Product",
    "shipping_price": 0,
    "marketing_fee": 0,
    "sold_price": 100,
    "sold_quantity": 10,
    "sale_date": "2023-12-05",
    "extra_expenses_customer": 0
}

    print(add_sale(test_sale))

    print("\nGetting stock information after sale...")
    post_sale_stock = get_stock(product_id)
    print(post_sale_stock)

# Run the test
test_stock_and_sales_flow()

def get_product_summary():
    response = requests.get(f"{BASE_URL}/sales/product-summary")
    try:
        return response.json()
    except ValueError:
        return {'error': 'No JSON response', 'status_code': response.status_code}


print("\nTesting product summary...")
print(get_product_summary())
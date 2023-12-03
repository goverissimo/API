# sales.py

from flask import Blueprint, jsonify, request
from database import get_db
from bson import ObjectId
sales_blueprint = Blueprint('sales_blueprint', __name__)

db = get_db()
sales_collection = db.sales
class Sale:
    def __init__(self, product_id, product_name, shipping_price, marketing_fee, sold_price, sale_date, sold_quantity, extra_expenses_customer):
        self.product_id = product_id
        self.product_name = product_name
        self.shipping_price = shipping_price
        self.marketing_fee = marketing_fee
        self.sold_price = sold_price
        self.sale_date = sale_date
        self.sold_quantity = sold_quantity
        self.extra_expenses_customer = extra_expenses_customer

    def to_dict(self):
        return self.__dict__

def transform_sale(sale):
    sale['_id'] = str(sale['_id'])
    return sale

@sales_blueprint.route('/sale', methods=['POST'])
def add_sale():
    data = request.json
    sale = Sale(**data)
    sales_collection.insert_one(sale.to_dict())

    # Decrease stock availability
    product_id = data.get('product_id')
    sold_quantity = data.get('sold_quantity')

    if product_id and sold_quantity is not None:
        stock_collection = db.stock  # Assuming this is how you access the stock collection
        stock_item = stock_collection.find_one({'product_id': product_id})
        if stock_item:
            new_available = stock_item.get('available', 0) - sold_quantity
            stock_collection.update_one({'product_id': product_id}, {'$set': {'available': new_available}})

    return jsonify({'message': 'Sale added successfully'}), 201

@sales_blueprint.route('/', methods=['GET'])
def get_sales():
    try:
        sales = list(sales_collection.find())
        return jsonify([transform_sale(sale) for sale in sales])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_blueprint.route('/sale/<int:product_id>', methods=['PUT'])
def update_sale(product_id):
    data = request.json
    result = sales_collection.update_one({"product_id": product_id}, {"$set": data})
    if result.matched_count:
        return jsonify({'message': 'Sale updated successfully'}), 200
    else:
        return jsonify({'message': 'Sale not found'}), 404

@sales_blueprint.route('/<int:product_id>', methods=['DELETE'])
def delete_sale(product_id):
    result = sales_collection.delete_one({"product_id": product_id})
    if result.deleted_count:
        return jsonify({'message': 'Sale deleted successfully'})
    return jsonify({'message': 'Sale not found'}), 404


@sales_blueprint.route('/product-summary', methods=['GET'])
def get_product_summary():
    try:
        # Aggregate data from sales and stock collections
        pipeline = [
            {
                "$group": {
                    "_id": "$product_id",
                    "total_sold_quantity": {"$sum": "$sold_quantity"},
                    "total_revenue": {"$sum": {"$multiply": ["$sold_quantity", "$sold_price"]}},
                    "total_cost": {"$sum": {"$multiply": ["$sold_quantity", "$sale_price"]}}
                }
            },
            {
                "$lookup": {
                    "from": "stock",
                    "localField": "_id",
                    "foreignField": "product_id",
                    "as": "stock_info"
                }
            },
            {
                "$unwind": "$stock_info"
            },
            {
                "$project": {
                    "product_name": "$stock_info.product_name",
                    "available_quantity": "$stock_info.available",
                    "total_sold_quantity": 1,
                    "profit": {"$subtract": ["$total_revenue", "$total_cost"]}
                }
            }
        ]
        summary = list(sales_collection.aggregate(pipeline))
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

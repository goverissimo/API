# stock.py
from flask import Blueprint, jsonify, request
from database import get_db
from bson import ObjectId
stock_blueprint = Blueprint('stock_blueprint', __name__)

db = get_db()
stock_collection = db.stock

class Stock:
    def __init__(self, product_id, available, price_bought, purchase_date, bought_quantity, extra_expenses_company):
        self.product_id = product_id
        self.available = available
        self.price_bought = price_bought
        self.purchase_date = purchase_date
        self.bought_quantity = bought_quantity
        self.extra_expenses_company = extra_expenses_company

    def to_dict(self):
        return self.__dict__

@stock_blueprint.route('/', methods=['POST'])
def add_or_update_stock():
    data = request.json
    stock = Stock(**data)

    existing_stock = stock_collection.find_one({'product_id': stock.product_id})
    if existing_stock:
        stock_collection.update_one({'product_id': stock.product_id}, {"$set": stock.to_dict()})
    else:
            if stock.available != stock.bought_quantity:
                print("quantity purchased is not the same as available")
            else:
                stock_collection.insert_one(stock.to_dict())
    return jsonify({'message': 'Stock added/updated successfully'}), 200

def transform_stock(stock):
    stock['_id'] = str(stock['_id'])
    return stock


@stock_blueprint.route('/', methods=['GET'])
@stock_blueprint.route('/<int:product_id>', methods=['GET'])
def get_stock(product_id=None):
    try:
        if product_id:
            stock = stock_collection.find_one({'product_id': product_id})
            if stock:
                return jsonify(transform_stock(stock))
            else:
                return jsonify({'message': 'Stock not found'}), 404
        else:
            stocks = list(stock_collection.find())
            return jsonify([transform_stock(stock) for stock in stocks])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
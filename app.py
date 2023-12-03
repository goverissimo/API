# app.py

from flask import Flask
from stock import stock_blueprint
from sales import sales_blueprint

app = Flask(__name__)
app.register_blueprint(stock_blueprint, url_prefix='/stock')
app.register_blueprint(sales_blueprint, url_prefix='/sales')

if __name__ == '__main__':
    
    app.run(debug=True)

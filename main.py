from flask import Flask, jsonify, request
import os
import requests
from script import get_product_hunt_data

app = Flask(__name__,static_folder='static')



@app.route("/")
def index():
    return app.send_static_file("index.html")
from dotenv import load_dotenv
import os

load_dotenv()

product_hunt_api = os.getenv("PRODUCT_HUNT_API_TOKEN")
@app.route("/api/products")
def get_products():
    try:
        if not product_hunt_api or product_hunt_api == "your_product_hunt_api_token":
            return jsonify({"error": "Product Hunt API token is missing or invalid. Please check your .env file."}), 500

        cursor_position = request.args.get('after')            
        data = get_product_hunt_data(after=cursor_position)
        return jsonify(data)
    except requests.exceptions.HTTPError as e:
        return jsonify({"error":str(e)}),e.response.status_code

@app.route("/category/<category_name>")
def category_page(category_name):
    return app.send_static_file("index.html")

if __name__ == '__main__':
    app.run(debug = True)
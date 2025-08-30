from flask import Flask, jsonify, request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,static_folder='static')

product_hunt_url = "https://api.producthunt.com/v2/api/graphql"
product_hunt_api = os.getenv("PRODUCT_HUNT_API_TOKEN")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/products")
def get_products():
    try:
        if not PRODUCT_HUNT_API_TOKEN or PRODUCT_HUNT_API_TOKEN == "your_product_hunt_api_token":
            return jsonify({"error": "Product Hunt API token is missing or invalid. Please check your .env file."}), 500

        cursor_position = request.args.get('after')            
        data = get_product_hunt_data(after=cursor_position)
        return jsonify(data)
    except requests.exceptions.HTTPerror as e:
        return jsonify({"error":str(e)}),e.response.status_code

@app.route("/category/<category_name>")
def category_page(category_name):
    return app.send_static_file("index.html")

if __name__ == '__main__':
    app.run(debug = True)
from flask import Flask, jsonify, request
import os
import requests
from script import get_product_hunt_data
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import schedule
import time
import csv
app = Flask(__name__,static_folder='static')

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)
# print current time in hh:mm
current_time = time.strftime("%H:%M")
print(f"Current time: {current_time}")

def send_daily_email():
    print("Sending daily email...")
    try:
        top_products_data = get_product_hunt_data()
        if not top_products_data or not top_products_data['data'] or not top_products_data['data']['posts'] or not top_products_data['data']['posts']['edges']:
            print("Could not fetch top products.")
            return
        top_products = top_products_data['data']['posts']['edges']
        
        with open("subscribers.csv", "r") as f:
            reader = csv.reader(f)
            subscribers = [row[0] for row in reader][1:]  # Skip header
        print(subscribers)
        with app.app_context():  # <-- Add this line
            for email_address in subscribers:
                msg = Message("Your Daily Dose of Top Products", recipients=[email_address],sender=app.config['MAIL_DEFAULT_SENDER'])
                html_content = """
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .product { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
                    .product img { width: 50px; height: 50px; margin-right: 10px; vertical-align: middle; }
                    .product a { color: #007bff; text-decoration: none; }
                </style>
            </head>
            <body>
                <h2>Here are today's top 10 products from Product Hunt:</h2>
            """
                for i, p in enumerate(top_products):
                    node = p['node']
                    html_content += f"""
                <div class='product'>
                    <img src='{node['thumbnail']['url']}' alt='{node['name']}'>
                    <a href='{node['url']}'>{node['name']}</a>: {node['tagline']}
                </div>
                """
                html_content += """
                <p>Check out Product Hunt Insights for more!</p>
            </body>
            </html>
            """
                msg.html = html_content
                mail.send(msg)
        print(f"Successfully sent daily email to {len(subscribers)} subscribers.")
    except Exception as e:
        print(f"Error sending daily email: {e}")

@app.route("/send-email")
def send_email_route():
    send_daily_email()
    return jsonify({"message": "Test email sent!"})


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

@app.route("/api/subscribe", methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required."}), 400
    
    try:
        with open("subscribers.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([email])
        
        # Send welcome email
        with app.app_context():
            msg = Message(
                "Welcome to Product Hunt Insights Newsletter!",
                recipients=[email],
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            msg.html = """
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .welcome { background: #f6f8fa; padding: 24px; border-radius: 8px; }
                    h2 { color: #ff6600; }
                </style>
            </head>
            <body>
                <div class="welcome">
                    <h2>Welcome!</h2>
                    <p>Thank you for subscribing to Product Hunt Insights.</p>
                    <p>You will receive the top 10 products from Product Hunt every day at <b>9:00 AM</b>.</p>
                    <p>Stay tuned for the latest trends in tech!</p>
                    <p style="margin-top:24px;">— The Product Hunt Insights Team</p>
                </div>
            </body>
            </html>
            """
            mail.send(msg)
            print("Welcome msg sent to :", email)
        return jsonify({"message": "Successfully subscribed!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_email, 'cron', hour=9, minute=0)  # Send daily at 9:00 AM
    scheduler.start()

    app.run(debug = True)
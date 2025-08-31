# Product Hunt Insights

Product Hunt Insights is a web application that provides a streamlined overview of the top trending products from Product Hunt. It offers a faster and more focused experience than the official website, allowing users to efficiently stay informed about new technology and market trends.

## Features

-   **Top Products:** Displays the top trending products from Product Hunt as the user scrolls down.
-   **Search & Filter:** Allows users to search and filter products by name, tagline, or tags.
-   **Category Pages:** Enables users to browse products by category.
-   **Daily Newsletter:** Sends a daily email with the top 10 products to subscribers.
-   **Contact & Newsletter Subscription:** Provides a form to collect email addresses for the newsletter.
-   **Professional Layout:** Features a clean, white layout with a modern header and a professional aesthetic.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Install dependencies:**
    ```bash
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    -   Create a `.env` file with the following variables:
        ```
        PRODUCT_HUNT_API_TOKEN=your_product_hunt_api_token
        MAIL_SERVER=your_mail_server
        MAIL_PORT=your_mail_port
        MAIL_USE_TLS=True
        MAIL_USERNAME=your_mail_username
        MAIL_PASSWORD=your_mail_password
        MAIL_DEFAULT_SENDER=your_mail_default_sender
        ```
    -   Replace `your_product_hunt_api_token` with your actual Product Hunt API token.
    -   Replace the `MAIL_*` variables with your email service credentials.

4.  **Run the application:**
    ```bash
    python main.py
    ```

## Usage

-   Open the application in your browser.
-   Browse the top trending products on the home page.
-   Use the "Search & Filter" tab to find products by name, tagline, or tags.
-   Subscribe to the daily newsletter on the "Contact & Newsletter" tab.

## Dependencies

-   Flask
-   Flask-Mail
-   python-dotenv
-   requests
-   APScheduler

```



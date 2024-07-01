from flask import Flask, request, jsonify
import requests
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Verify the Discord Webhook URL environment variable
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
if not DISCORD_WEBHOOK_URL:
    app.logger.error("DISCORD_WEBHOOK_URL environment variable is not set")
else:
    app.logger.info(f"DISCORD_WEBHOOK_URL: {DISCORD_WEBHOOK_URL}")

@app.route('/')
def home():
    return "Hello, this is your Flask application running on Azure!"

@app.route('/webhook', methods=['POST'])
def webhook():
    app.logger.info(f"Received request data: {request.data}")
    data = request.json
    if not data or 'message' not in data:
        app.logger.error("Invalid request data")
        return jsonify({'status': 'failure', 'reason': 'Invalid request data'}), 400

    message = format_alert_message(data)
    app.logger.info(f"Formatted message: {message}")

    try:
        send_to_discord(message)
        app.logger.info("Message sent to Discord successfully")
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        app.logger.error(f"Failed to send message to Discord: {e}")
        return jsonify({'status': 'failure', 'reason': str(e)}), 500

def format_alert_message(data):
    local_time = data.get('local_time')
    timeframe = data.get('timeframe')
    signal_type = data.get('signal_type')
    stock_symbol = data.get('stock_symbol')

    description = get_description(signal_type, timeframe, stock_symbol)

    formatted_message = (
        f"**Signal Alert**\n\n"
        f"**Time**: {local_time}\n"
        f"**Timeframe**: {timeframe}\n"
        f"**Signal Type**: {signal_type}\n"
        f"**Stock**: {stock_symbol}\n"
        f"**Description**: {description} 🤖\n"
    )

    return formatted_message

def get_description(signal_type, timeframe, stock_symbol):
    if signal_type == "Buy":
        return f"A buy signal has been generated for {stock_symbol} on the {timeframe} timeframe. Please check your chart for verification and use proper risk management."
    elif signal_type == "Sell":
        return f"A sell signal has been generated for {stock_symbol} on the {timeframe} timeframe. Please check your chart for verification and use proper risk management."
    elif signal_type == "Caution Buy":
        return f"A caution buy signal has been generated for {stock_symbol} on the {timeframe} timeframe. Please check your chart for verification and use proper risk management."
    elif signal_type == "Exit Buy":
        return f"An exit buy signal has been generated for {stock_symbol} on the {timeframe} timeframe. Please check your chart for verification and use proper risk management."
    elif signal_type == "Caution Sell":
        return f"A caution sell signal has been generated for {stock_symbol} on the {timeframe} timeframe. Please check your chart for verification and use proper risk management."
    elif signal_type == "Exit Sell":
        return f"An exit sell signal has been generated for {stock_symbol} on the {timeframe} timeframe. Please check your chart for verification and use proper risk management."
    else:
        return f"A {signal_type} signal has been generated for {stock_symbol} on the {timeframe} timeframe. Please check your chart for verification and use proper risk management."

def send_to_discord(message):
    data = {
        "content": message
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    app.logger.info(f"Discord response status code: {response.status_code}")
    app.logger.info(f"Discord response text: {response.text}")
    if response.status_code != 204:
        raise Exception(f"Failed to send message to Discord: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

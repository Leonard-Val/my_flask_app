from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Discord Webhook URL - directly set here
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1253199625087750216/LVwNxxDEyHAF7D7ByV_NwAw-6HmXKdAlWMU6PO5e07_zg6gqSkidRheIdY94B1e9Ye-w"

if not DISCORD_WEBHOOK_URL:
    app.logger.error("DISCORD_WEBHOOK_URL is not set")
else:
    app.logger.info(f"DISCORD_WEBHOOK_URL: {DISCORD_WEBHOOK_URL}")

@app.route('/')
def home():
    return "Hello, this is your Flask application running on Azure!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        app.logger.info(f"Received webhook data: {data}")
        if not data or 'message' not in data:
            app.logger.error("Invalid webhook data")
            return jsonify({'status': 'failure', 'reason': 'Invalid webhook data'}), 400

        message = format_alert_message(data)
        app.logger.info(f"Formatted message: {message}")

        send_to_discord(message)
        app.logger.info("Message sent to Discord successfully")
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'status': 'failure', 'reason': str(e)}), 500

@app.route('/manual_input', methods=['POST'])
def manual_input():
    try:
        data = request.json
        app.logger.info(f"Received manual input data: {data}")
        if not data or 'author' not in data or 'stock_symbol' not in data or 'signal_type' not in data or 'timeframe' not in data or 'local_time' not in data:
            app.logger.error("Invalid manual input data")
            return jsonify({'status': 'failure', 'reason': 'Invalid manual input data'}), 400

        message = format_alert_message(data)
        app.logger.info(f"Formatted message: {message}")

        send_to_discord(message)
        app.logger.info("Message sent to Discord successfully")
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'status': 'failure', 'reason': str(e)}), 500

def format_alert_message(data):
    local_time = data.get('local_time')
    timeframe = data.get('timeframe')
    signal_type = data.get('signal_type').upper()  # Capitalize signal type
    stock_symbol = data.get('stock_symbol')
    author = data.get('author', 'TradingView')  # Default to 'TradingView' if not provided

    description = data.get('description', f"A {signal_type} signal has been generated for {stock_symbol} on the {timeframe} timeframe. Please check your chart for verification and please use proper risk management.")
    emoji = get_emoji(signal_type)

    formatted_message = (
        f"**Signal Alert** {emoji}\n\n"
        f"**Author**: {author}\n"
        f"**Time**: {local_time}\n"
        f"**Timeframe**: {timeframe}\n"
        f"**Signal Type**: {signal_type}\n"
        f"**Stock**: {stock_symbol}\n"
        f"**Description**: {description} 🤖\n"
    )

    return formatted_message

def get_emoji(signal_type):
    if "BUY" in signal_type:
        return "📈🟢"  # Up arrow and green circle
    elif "SELL" in signal_type:
        return "📉🔴"  # Down arrow and red circle
    else:
        return "⚠️"  # Warning sign for caution signals

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

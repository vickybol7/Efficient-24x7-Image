from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- CONFIGURATION ---
# Replace these with your actual details or set them as Environment Variables in Railway
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

def send_telegram_alert(service_name, status, project_name):
    """Sends the alert message to Telegram."""
    
    # Emoji selection based on status
    emoji = "⚠️"
    if status == "CRASHED":
        emoji = "💥"
    elif status == "OOM_KILLED":
        emoji = "💀 (Out of Memory)"
    
    message_text = (
        f"{emoji} **STREAM ALERT** {emoji}\n\n"
        f"**Project:** {project_name}\n"
        f"**Service:** {service_name}\n"
        f"**Status:** {status}\n\n"
        f"Check your Railway dashboard immediately!"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"✅ Alert sent to Telegram for {status}")
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Receives the data from Railway."""
    try:
        data = request.json
        
        # 1. Identify the Event Type
        event_type = data.get('type')
        
        # 2. Extract Status and Service Info
        # Railway payloads typically have a 'deployment' object inside
        deployment_data = data.get('deployment', {})
        status = deployment_data.get('status') # e.g., CRASHED, OOM_KILLED
        
        project_data = data.get('project', {})
        project_name = project_data.get('name', 'Unknown Project')
        
        service_data = data.get('service', {})
        service_name = service_data.get('name', 'Unknown Service')

        print(f"📥 Received Webhook: {event_type} - {status}")

        # 3. Check if it's a "Bad" Status
        # We check for FAILED too, just in case you enable it later.
        if status in ['CRASHED', 'OOM_KILLED', 'FAILED']:
            send_telegram_alert(service_name, status, project_name)

        return jsonify({"status": "success", "message": "Webhook processed"}), 200

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the server
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))

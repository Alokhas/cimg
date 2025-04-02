import os
import requests
from telebot import TeleBot, types
# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set this in a .env file for security

bot = TeleBot(BOT_TOKEN)

# Function to fetch vehicle data
def get_vehicle_info(vehicle_number):
    url = f"https://lucky-grass-19e2.lxonfire.workers.dev/?car={vehicle_number}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            return data
        return None
    except requests.RequestException:
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name or "User"
    bot.send_message(
        message.chat.id,
        f"Hello {user_name} 👋\n\nSend me any vehicle number to get its information."
    )

@bot.message_handler(func=lambda message: True)
def fetch_vehicle_details(message):
    chat_id = message.chat.id
    vehicle_number = message.text.strip()

    sent_msg = bot.send_message(chat_id, "🔍 Fetching vehicle details...")

    data = get_vehicle_info(vehicle_number)

    if data and isinstance(data, dict) and "data" in data and isinstance(data["data"], dict):
        vehicle_data = data["data"]
        image_url = data.get("image", "")

        caption = f"""🚗 *Vehicle Information*

*Vehicle ID:* `{vehicle_data.get("VEHICLE_NUM", "N/A")}`
*Registration Date:* `{vehicle_data.get("REG_DATE", "N/A")}`

👤 *Owner Information*

*Owner Name:* `{vehicle_data.get("NAME", "N/A")}`
*Owner Count:* `{vehicle_data.get("OWNER_NUM", "N/A")}`
*Pin Code:* `{vehicle_data.get("mobile", "N/A")}`

🔧 *Vehicle Information*

*Brand Name:* `{vehicle_data.get("BRAND", "N/A")}`
*Model:* `{vehicle_data.get("VEHICLE_MODEL", "N/A")}`

🛡️ *Insurance Information*

*Insurance Company:* `{vehicle_data.get("INSURANCE_BY", "N/A")}`
*Insurance Expiry:* `{vehicle_data.get("insurance_Expiry_Date", "N/A")}`
"""

        bot.edit_message_text("✅ Vehicle details found!", chat_id, sent_msg.message_id)
        if image_url:
            bot.send_photo(chat_id, image_url, caption=caption, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, caption, parse_mode="Markdown")
    else:
        bot.edit_message_text("❌ Failed to fetch vehicle details. Please check the vehicle number and try again.", chat_id, sent_msg.message_id)

bot.polling(none_stop=True)

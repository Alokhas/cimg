from telebot import TeleBot, types
import requests
from io import BytesIO

bot = TeleBot("6770440133:AAEvQ_nW8Mq7q9yO99vD4BOBqUi7wM3mMGI")

def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    response = requests.post(url, json={"code": code})
    if response.status_code == 200:
        image = BytesIO(response.content)
        image.name = "carbon.png"
        return image
    return None

@bot.message_handler(func=lambda message: True)
def carbon_auto(message):
    chat_id = message.chat.id
    sent_msg = bot.send_message(chat_id, "Processing...")
    
    carbon = make_carbon(message.text)
    if carbon:
        bot.send_chat_action(chat_id, "upload_photo")
        bot.send_photo(
            chat_id,
            photo=carbon,
            caption="Made by: @Thealphabotz and @alphaapis",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Support Us", url="https://t.me/thealphabotz")
            )
        )
    else:
        bot.send_message(chat_id, "Failed to generate Carbon image.")
    
    bot.delete_message(chat_id, sent_msg.message_id)
    if carbon:
        carbon.close()

bot.polling(none_stop=True)

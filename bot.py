import os
import telebot
import openai

# ====== SETUP ======
TELEGRAM_TOKEN = os.getenv("TOKEN")  # from Render env var
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # from Render env var

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# ====== KEYWORD RESPONSES ======
keyword_replies = {
    "hello": "Hey there! How can I help you today?",
    "price": "Our pricing details are available on the website.",
    "hours": "We are available 24/7!",
}

# ====== MESSAGE HANDLER ======
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    # 1. Keyword response
    for keyword, reply in keyword_replies.items():
        if keyword in text:
            bot.reply_to(message, reply)
            return

    # 2. ChatGPT response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text},
            ]
        )
        reply = response.choices[0].message.content
        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, "Yo xup, we will get back to you")

# ====== START BOT ======
print("Bot is running/live...")
bot.polling()

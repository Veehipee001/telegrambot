import os
import telebot
import openai

# Get keys from environment variables
BOT_TOKEN = os.getenv("TOKEN")
LEMONFOX_KEY = os.getenv("LEMONFOX_API_KEY")

if not BOT_TOKEN or not LEMONFOX_KEY:
    raise ValueError("Missing TOKEN or LEMONFOX_API_KEY env vars")

# Setup Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Configure Lemonfox OpenAI-compatible API
openai.api_key = LEMONFOX_KEY
openai.api_base = "https://api.lemonfox.ai/v1"

# Pre-defined keyword replies
keyword_replies = {
    "hi": "Hey there! How can I assist you?",
    "hello": "Hello! ",
    "help": "I'm here to help. Ask me anything!",
    "xup": "Yo xup, we will get back to you."
}

def check_keyword(text):
    for k, v in keyword_replies.items():
        if k in text.lower():
            return v
    return None

# Handle all incoming messages
@bot.message_handler(func=lambda msg: True)
def reply(msg):
    text = msg.text or ""
    kw = check_keyword(text)
    if kw:
        bot.reply_to(msg, kw)
    else:
        # AI fallback via Lemonfox
        try:
            r = openai.ChatCompletion.create(
                model="llama-8b-chat",
                messages=[{"role":"user", "content": text}],
                max_tokens=200,
                temperature=0.7
            )
            bot.reply_to(msg, r.choices[0].message["content"].strip())
        except Exception:
            bot.reply_to(msg, "Oops, I couldn't reach AI right now.")

print("Bot is up and running")
bot.infinity_polling()

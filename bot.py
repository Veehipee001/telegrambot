import telebot
import os

# Get the bot token from environment variable
TOKEN = os.environ.get("TOKEN")

# Ensure token is available
if not TOKEN:
    raise ValueError("Bot token not set in environment variable.")

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Respond to any message with a fixed reply
@bot.message_handler(func=lambda message: True)
def reply_fixed(message):
    bot.reply_to(message, "Yo xup, we will get back to you")

# Start polling (keeps the bot online)
bot.polling()

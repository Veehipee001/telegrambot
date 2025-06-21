
import os
import telebot

# Get your bot token from Render's environment variable
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)

# --- Smart Reply Logic ---
@bot.message_handler(func=lambda message: True)
def reply_smart(message):
    text = message.text.lower()

    if "hello" in text or "hi" in text:
        bot.reply_to(message, "Hey, Xup how ya doing")
    elif "how are you" in text:
        bot.reply_to(message, "I  am just a bot, but I'm functioning as expected. ")
    elif "bye" in text:
        bot.reply_to(message, "Goodbye, chat again soon.")
    else:
        bot.reply_to(message, "I am here to help, but I do not quite understand that. ")

# Keep the bot running
bot.infinity_polling()
import os
import telebot
import openai

# Get tokens from environment variables
BOT_TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Define some simple keyword responses
keyword_responses = {
    "hi": "Hey! How can I help you?",
    "hello": "Hello there! ??",
    "help": "I can assist you with general questions or respond like ChatGPT!",
    "xup": "Yo xup, we will get back to you."
}

# Check if message matches any keywords
def check_keywords(message_text):
    for keyword, response in keyword_responses.items():
        if keyword in message_text.lower():
            return response
    return None

# Handle all messages
@bot.message_handler(func=lambda message: True)
def reply_to_message(message):
    user_text = message.text
    keyword_reply = check_keywords(user_text)

    if keyword_reply:
        bot.reply_to(message, keyword_reply)
    else:
        # Fallback to GPT
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_text}]
            )
            bot.reply_to(message, response.choices[0].message['content'].strip())
        except Exception as e:
            bot.reply_to(message, "Sorry, I couldn't reach ChatGPT right now.")

# Run the bot
print("Bot is running...")
bot.infinity_polling()

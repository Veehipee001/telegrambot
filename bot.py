import os
import telebot
import openai

# Environment variables
TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

# Keyword-based responses
keyword_responses = {
    "hello": "Hi there! ??",
    "bye": "Goodbye! ??",
    "help": "How can I assist you?",
}

# Function to get ChatGPT reply
def get_gpt_response(message_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if enabled
            messages=[{"role": "user", "content": message_text}],
            max_tokens=150,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "Sorry, I couldn't reach ChatGPT right now."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.lower().strip()

    # Check if message matches a keyword
    for keyword in keyword_responses:
        if keyword in user_text:
            bot.reply_to(message, keyword_responses[keyword])
            return

    # Else, get ChatGPT response
    gpt_reply = get_gpt_response(message.text)
    bot.reply_to(message, gpt_reply)

print("Bot is running...")
bot.polling()

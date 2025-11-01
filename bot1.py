import telebot
from telebot import types
from flask import Flask, request

# ==============================
# 🔐 BOT TOKEN & CONFIGURATION
# ==============================
BOT_TOKEN = "8123852470:AAGpF5BS0HXXQ7l6vfqwWrrg-jddmUzqLBM"  # Replace with your Telegram bot token
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==============================
# 🚀 START COMMAND
# ==============================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💳 Fund Account", "💼 Buy Lookup")
    markup.row("📊 Check Balance", "ℹ️ Help")

    welcome_text = (
        f"👋 Hello *{message.from_user.first_name or 'User'}!*\n\n"
        "Welcome to the *Lookup Service Bot*.\n\n"
        "🔹 Super access fee: *$50* (unlocks 30 lookups at $5 each)\n"
        "🔹 Single lookup without plan: *$15*\n\n"
        "Please choose an option below to continue 👇"
    )

    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# ==============================
# 💳 FUND ACCOUNT SECTION
# ==============================
@bot.message_handler(func=lambda message: message.text == "💳 Fund Account")
def fund_account(message):
    text = (
        "💰 *Funding Instructions*\n\n"
        "To fund your account, please send Bitcoin (BTC) to the address below:\n\n"
        "`bc1qc8vyaa57auvcexca69pp2cvm44shlymymmv46c`\n\n"
        "⚠️ *Note:* Payments are automatically verified after 1 network confirmation.\n"
        "Once confirmed, your wallet will be credited instantly.\n\n"
        "You can check your balance anytime using the '📊 Check Balance' button."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# ==============================
# 💼 BUY LOOKUP SECTION
# ==============================
@bot.message_handler(func=lambda message: message.text == "💼 Buy Lookup")
def buy_lookup(message):
    text = (
        "🧾 *Lookup Options*\n\n"
        "Choose how you'd like to proceed:\n"
        "1️⃣ *Super plan:* $50 (10 lookups at $5 each)\n"
        "2️⃣ *Single lookup:* $15\n\n"
        "After payment confirmation, type /activate to begin your lookup session."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# ==============================
# 📊 CHECK BALANCE SECTION
# ==============================
@bot.message_handler(func=lambda message: message.text == "📊 Check Balance")
def check_balance(message):
    # You can connect this later to your database
    text = (
        "💼 *Your Account Balance:*\n\n"
        "Balance: *$0.00*\n"
        "Status: *Unfunded*\n\n"
        "Use '💳 Fund Account' to add funds."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# ==============================
# ℹ️ HELP SECTION
# ==============================
@bot.message_handler(func=lambda message: message.text == "ℹ️ Help")
def help_info(message):
    help_text = (
        "📘 *Help & Support*\n\n"
        "1️⃣ Fund your wallet using the '💳 Fund Account' button.\n"
        "2️⃣ Purchase your desired lookup plan.\n"
        "3️⃣ Start lookups after payment confirmation.\n\n"
        "For assistance, contact support via /support."
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# ==============================
# 🌐 FLASK WEBHOOK SETUP
# ==============================
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot is running!", 200

# ==============================
# 🏁 RUN BOT (LOCAL TEST MODE)
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
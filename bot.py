import telebot
from telebot import types
import os

# ==============================
# 🔐 BOT TOKEN
# ==============================
# ❌ WRONG: os.getenv("8345...")  — You passed the token directly instead of the env variable name.
# ✅ FIX: Either use os.getenv("BOT_TOKEN") and set the token as an environment variable,
# or just paste the token directly (for local testing only).

BOT_TOKEN = "8345132951:AAEbG31cfstAflhNaBqkieSrF5KF7KU_-eQ"
bot = telebot.TeleBot(BOT_TOKEN)

# ==============================
# 💾 Temporary Database
# ==============================
users = {}  # {user_id: {"plan": "discount"/"standard", "wallet": float}}

# ==============================
# 🏦 FUNDING INSTRUCTIONS
# ==============================
FUNDING_INSTRUCTIONS = (
    "💰 *Funding Instructions:*\n"
    "Please follow the steps below to fund your wallet:\n\n"
    "1️⃣ Send payment to the provided wallet or payment channel.\n"
    "2️⃣ Upload your payment receipt or transaction ID to our support team.\n"
    "3️⃣ Your wallet will be credited once payment is verified.\n\n"
    "👉 Contact support for help if you experience any issue."
)

# ==============================
# 🚀 START COMMAND
# ==============================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id

    if user_id in users:
        bot.send_message(
            user_id,
            f"👋 Welcome back!\n"
            f"💳 Plan: {users[user_id]['plan'].capitalize()} Plan\n"
            f"💰 Wallet Balance: ${users[user_id]['wallet']:.2f}\n\n"
            "Use /wallet to check or fund your wallet."
        )
        return

    intro_text = (
        "👋 Welcome to *Dl Father BotLookup Bot!*\n\n"
        "🔍 Here’s how payment works:\n\n"
        "💰 *Payment Options:*\n"
        "1️⃣ **Discount Plan — $50 one-time payment:**\n"
        "   ➤ Pay once and enjoy *$5 per lookup forever!*\n\n"
        "2️⃣ **Standard Plan — $15 per lookup:**\n"
        "   ➤ No setup fee. Pay $15 only when you perform a lookup.\n\n"
        "Please choose your preferred option below 👇"
    )

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("💎 $50 Discount Plan ($5 per lookup)")
    btn2 = types.KeyboardButton("💲 $15 Standard Plan (Pay per lookup)")
    markup.add(btn1, btn2)

    bot.send_message(user_id, intro_text, parse_mode="Markdown", reply_markup=markup)

# ==============================
# 💳 HANDLE PAYMENT CHOICE
# ==============================
@bot.message_handler(func=lambda message: message.text in [
    "💎 $50 Discount Plan ($5 per lookup)",
    "💲 $15 Standard Plan (Pay per lookup)"
])
def handle_payment_choice(message):
    user_id = message.chat.id

    if message.text == "💎 $50 Discount Plan ($5 per lookup)":
        users[user_id] = {"plan": "discount", "wallet": 0.0}
        bot.send_message(
            user_id,
            "✅ You selected the *$50 Discount Plan!*\n\n"
            "Please make a one-time payment of *$50* to activate your account.\n\n"
            "💱 Send the equivalent of *$50 in BTC* to this address:\n"
            "`bc1qc8vyaa57auvcexca69pp2cvm44shlymymmv46c`\n\n"
            "Once payment is confirmed, you’ll enjoy *$5 per lookup forever!*",
            parse_mode="Markdown"
        )

    elif message.text == "💲 $15 Standard Plan (Pay per lookup)":
        users[user_id] = {"plan": "standard", "wallet": 0.0}
        bot.send_message(
            user_id,
            "✅ You selected the *$15 Standard Plan!*\n\n"
            "Each lookup costs *$15.* Please fund your wallet to start using the service.\n\n"
            "💱 Send the equivalent of *$15 in BTC* to this address:\n"
            "`bc1qc8vyaa57auvcexca69pp2cvm44shlymymmv46c`",
            parse_mode="Markdown"
        )

# ==============================
# 💰 WALLET COMMAND
# ==============================
@bot.message_handler(commands=['wallet'])
def wallet_balance(message):
    user_id = message.chat.id

    if user_id not in users:
        bot.send_message(user_id, "⚠️ You don’t have an account yet. Type /start to begin.")
        return

    plan = users[user_id]['plan'].capitalize()
    balance = users[user_id]['wallet']

    bot.send_message(
        user_id,
        f"💼 *Wallet Info*\n"
        f"Plan: {plan} Plan\n"
        f"Balance: ${balance:.2f}\n\n"
        f"{FUNDING_INSTRUCTIONS}",
        parse_mode="Markdown"
    )

# ==============================
# ▶️ RUN BOT
# ==============================
print("🤖 Dl Father BotLookup Bot is running...")
bot.infinity_polling()

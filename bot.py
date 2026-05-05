import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8778797228:AAGbU8kQOHqTIIWN9QX00hk4joR2g9zFFvw"

CHANNEL = "@videozone6"
ADMIN_ID = 7682181947
PAYMENT_UPI = "paytm.s1v05xz@pty"

users = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {"coins": 0}

    keyboard = [
        [InlineKeyboardButton("🎬 वीडियो देखो", callback_data="video")],
        [InlineKeyboardButton("👥 रेफर करो", callback_data="refer")],
        [InlineKeyboardButton("💰 मेरे कॉइन्स", callback_data="coins")],
        [InlineKeyboardButton("🛒 कॉइन्स खरीदो", callback_data="buy")],
        [InlineKeyboardButton("📞 सपोर्ट", url="https://t.me/Trusted_sellarr")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Welcome 👇", reply_markup=reply_markup)


async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("🎬 वीडियो देखो और कॉइन्स कमाओ")


async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    link = f"https://t.me/Video_zone6_bot?start={user_id}"
    await query.message.reply_text(f"👥 अपना रेफर लिंक:\n{link}")


async def coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    coins = users.get(user_id, {}).get("coins", 0)
    await query.message.reply_text(f"💰 आपके कॉइन्स: {coins}")


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"💳 Payment UPI:\n{PAYMENT_UPI}")


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(video, pattern="video"))
    app.add_handler(CallbackQueryHandler(refer, pattern="refer"))
    app.add_handler(CallbackQueryHandler(coins, pattern="coins"))
    app.add_handler(CallbackQueryHandler(buy, pattern="buy"))

    print("Bot started...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())

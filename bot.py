from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8778797228:AAGbU8kQOHqTIIWN9QX00hk4joR2g9zFFvw"

CHANNEL = "@videozone6"
ADMIN_ID = 7682181947
UPI_ID = "paytm.s1v05xz@pty"

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
        [InlineKeyboardButton("📞 सपोर्ट", url="https://t.me/Video_zone6_bot")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Welcome bhai 👋", reply_markup=reply_markup)

# BUTTONS
async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Video feature coming soon 🎬")

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    link = f"https://t.me/Video_zone6_bot?start={user_id}"
    await query.answer()
    await query.message.reply_text(f"Invite link:\n{link}")

async def coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    await query.message.reply_text(f"Coins: {users[user_id]['coins']}")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"Pay here 👇\n{UPI_ID}")

# RUN BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(video, pattern="video"))
app.add_handler(CallbackQueryHandler(refer, pattern="refer"))
app.add_handler(CallbackQueryHandler(coins, pattern="coins"))
app.add_handler(CallbackQueryHandler(buy, pattern="buy"))

print("Bot started...")
app.run_polling()

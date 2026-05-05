from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8778797228:AAGbU8kQOHqTIIWN9QX00hk4joR2g9zFFvw"
CHANNEL = "@videozone6"
BOT_USERNAME = "Video_zone6_bot"
UPI = "paytm.s1v05xz@pty"

users = {}

# 🔒 CHECK JOIN
async def is_joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_joined(user_id, context):
        keyboard = [
            [InlineKeyboardButton("📢 चैनल जॉइन करो", url="https://t.me/videozone6")],
            [InlineKeyboardButton("✅ मैंने जॉइन कर लिया", callback_data="check")]
        ]
        await update.message.reply_text(
            "🚫 पहले चैनल जॉइन करो तभी bot use कर पाओगे 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if user_id not in users:
        users[user_id] = {"coins": 0}

    keyboard = [
        [InlineKeyboardButton("🎥 वीडियो देखो", callback_data="video")],
        [InlineKeyboardButton("👥 रेफर करो", callback_data="refer")],
        [InlineKeyboardButton("💰 मेरे कॉइन", callback_data="coins")],
        [InlineKeyboardButton("🛒 कॉइन खरीदो", callback_data="buy")],
        [InlineKeyboardButton("📞 सपोर्ट", callback_data="support")]
    ]

    await update.message.reply_text(
        "🔥 Welcome भाई 😎\nनीचे से option चुनो:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🔘 BUTTON HANDLER
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "check":
        if await is_joined(user_id, context):
            await query.message.reply_text("✅ अब /start दबाओ")
        else:
            await query.message.reply_text("❌ अभी तक चैनल जॉइन नहीं किया")
        return

    if not await is_joined(user_id, context):
        await query.message.reply_text("🚫 पहले चैनल जॉइन करो")
        return

    if user_id not in users:
        users[user_id] = {"coins": 0}

    if query.data == "video":
        users[user_id]["coins"] += 1
        await query.message.reply_text("🎥 वीडियो देखा! +1 कॉइन मिला")

    elif query.data == "refer":
        link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        await query.message.reply_text(f"👥 आपका रेफर लिंक:\n{link}")

    elif query.data == "coins":
        await query.message.reply_text(f"💰 आपके कॉइन: {users[user_id]['coins']}")

    elif query.data == "buy":
        await query.message.reply_text(
            f"💸 पेमेंट करो:\n\nUPI: {UPI}\n\nPayment के बाद screenshot भेजो"
        )

    elif query.data == "support":
        keyboard = [
            [InlineKeyboardButton("📩 Contact Support", url="https://t.me/Trusted_sellarr")]
        ]
        await query.message.reply_text(
            "📞 Support से बात करने के लिए नीचे क्लिक करो 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ▶️ MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()

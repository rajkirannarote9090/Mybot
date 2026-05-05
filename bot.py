
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8778797228:AAGbU8kQOHqTIIWN9QX00hk4joR2g9zFFvw"
CHANNEL = "@videozone6"

users = {}
members = []

async def is_joined(user_id, context):
    member = await context.bot.get_chat_member(CHANNEL, user_id)
    return member.status in ["member", "administrator", "creator"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {"coins": 10}

    if not await is_joined(user_id, context):
        buttons = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL[1:]}")],
            [InlineKeyboardButton("✅ I Joined", callback_data="check")]
        ]
        await update.message.reply_text("Pehle channel join karo", reply_markup=InlineKeyboardMarkup(buttons))
        return

    await menu(update)

async def menu(update):
    buttons = [
        [InlineKeyboardButton("🎬 Video", callback_data="video")],
        [InlineKeyboardButton("📤 Refer", callback_data="refer")],
        [InlineKeyboardButton("💰 Membership", callback_data="buy")],
        [InlineKeyboardButton("🎁 Coins", callback_data="coins")]
    ]
    await update.message.reply_text("Select option", reply_markup=InlineKeyboardMarkup(buttons))

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_joined(user_id, context):
        await query.message.reply_text("Welcome 🔥")
        await menu(query)
    else:
        await query.answer("Join nahi kiya 😅", show_alert=True)

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id in members:
        await query.message.reply_text("Unlimited video 🎬")
    elif users[user_id]["coins"] > 0:
        users[user_id]["coins"] -= 1
        await query.message.reply_text(f"Video 🎬\nCoins left: {users[user_id]['coins']}")
    else:
        await query.message.reply_text("Coins nahi 😅 Refer karo ya membership lo")

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    link = f"https://t.me/Video_zone6_bot?start={user_id}"
    await query.message.reply_text(f"Invite link:\n{link}\n1 refer = 5 coins")

async def coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.message.reply_text(f"Coins: {users[user_id]['coins']}")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.reply_text("₹99 Paytm kara ani screenshot pathva")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check, pattern="check"))
app.add_handler(CallbackQueryHandler(video, pattern="video"))
app.add_handler(CallbackQueryHandler(refer, pattern="refer"))
app.add_handler(CallbackQueryHandler(coins, pattern="coins"))
app.add_handler(CallbackQueryHandler(buy, pattern="buy"))

app.run_polling()

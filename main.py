import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# এনভায়রনমেন্ট ভেরিয়েবল থেকে টোকেন নিবে (নিরাপত্তার জন্য)
TOKEN = os.getenv('8125726114:AAH8BtWL1QWfWXe1sbuDtByLBrP0bSHLjDo')
OWNER_ID = int(os.getenv('8272290670'))

# ইউজার ডাটাবেজ (সিম্পল ফরম্যাট)
USERS_DATA = {
    OWNER_ID: {"tier": "OWNER", "limit": 999, "count": 0}
}

ASSET_PAIRS = ["EUR/USD-OTC", "GBP/USD-OTC", "USD/PHP-OTC", "NZD/CAD-OTC", "AUD/CAD-OTC", "USD/IDR-OTC", "EUR/CAD-OTC", "USD/JPY-OTC"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USERS_DATA:
        await update.message.reply_text(f"❌ ACCESS DENIED!\nID: {user_id}\nContact Admin.")
        return
    
    user = USERS_DATA[user_id]
    keyboard = [[InlineKeyboardButton(pair, callback_data=pair)] for pair in ASSET_PAIRS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"⚡ PAIN X BINARY ⚡\nTier: {user['tier']}\nSignals Left: {user['limit']-user['count']}\n\nSelect Asset:", reply_markup=reply_markup)

async def handle_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = USERS_DATA[user_id]
    
    if user['count'] >= user['limit']:
        await query.answer("Daily Limit Reached!", show_alert=True)
        return

    user['count'] += 1
    msg = f"<code>┌──────────────────────┐\n│ PAIN X BINARY V5     │\n├──────────────────────┤\n│ PAIR: {query.data}  \n│ TYPE: 1 MIN SIGNAL   \n│ DIR:  CALL/PUT       \n├──────────────────────┤\n│ REMAINING: {user['limit']-user['count']}       \n└──────────────────────┘</code>"
    await query.edit_message_text(text=msg, parse_mode='HTML')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_click))
    app.run_polling()

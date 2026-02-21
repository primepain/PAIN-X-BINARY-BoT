import os
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- সেটিংস ---
# Render-এর Environment Variable এ '8125726114:AAH8BtWL1QWfWXe1sbuDtByLBrP0bSHLjDo' নাম দিয়ে তোমার টোকেনটা বসাবে
TOKEN = os.getenv('BOT_TOKEN') 
OWNER_ID = 8272290670  # আমি সরাসরি তোমার আইডি এখানে বসিয়ে দিয়েছি

# ইউজার এক্সেস এবং লিমিট
USERS_ACCESS = {
    OWNER_ID: {"tier": "OWNER", "limit": 9999, "count": 0}
}

# তোমার স্ক্রিনশটের মার্কেট পেয়ারগুলো
MARKET_PAIRS = [
    "EUR/CAD (OTC)", "USD/PHP (OTC)", "NZD/CAD (OTC)", "USD/IDR (OTC)",
    "EUR/NZD (OTC)", "EUR/USD (OTC)", "GBP/CHF (OTC)", "NZD/JPY (OTC)",
    "GBP/CAD (OTC)", "AUD/CAD (OTC)", "USD/BRL (OTC)", "EUR/CHF (OTC)"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USERS_ACCESS:
        await update.message.reply_text(f"❌ ACCESS DENIED!\nID: {user_id}\nContact Admin.")
        return

    user = USERS_ACCESS[user_id]
    keyboard = []
    for i in range(0, len(MARKET_PAIRS), 2):
        row = [InlineKeyboardButton(MARKET_PAIRS[i], callback_data=MARKET_PAIRS[i])]
        if i+1 < len(MARKET_PAIRS):
            row.append(InlineKeyboardButton(MARKET_PAIRS[i+1], callback_data=MARKET_PAIRS[i+1]))
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"⚡ ᴘᴀɪɴ x ʙɪɴᴀʀʏ | ᴛᴇʀᴍɪɴᴀʟ ⚡\n\n🆔 ID: {user_id}\n🎖 TIER: {user['tier']}\n📊 LEFT: {user['limit'] - user['count']}\n\nSELECT ASSET:",
        reply_markup=reply_markup
    )

async def handle_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = USERS_ACCESS[user_id]

    if user['count'] >= user['limit']:
        await query.answer("Limit Reached!", show_alert=True)
        return

    user['count'] += 1
    selected_pair = query.data
    # এন্ট্রি টাইম বর্তমান সময়ের ১ মিনিট পরেরটা দেখাবে
    entry_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M")

    hacker_box = f"""
<code>┌──────────────────────────────────┐
│   PAIN X BINARY | TERMINAL V5    │
├──────────────────────────────────┤
│ [>] ASSET : {selected_pair}
│ [>] TIME  : {entry_time} (1 MIN)
│ [>] SIGNAL: CALL 🟢 / PUT 🔴
├──────────────────────────────────┤
│ [!] AVOID BIG CANDLE & DOJI      │
│ [#] SIGNALS LEFT: {user['limit'] - user['count']}
└──────────────────────────────────┘</code>
    """
    await query.edit_message_text(text=hacker_box, parse_mode='HTML')

if __name__ == '__main__':
    if not TOKEN:
        print("Error: BOT_TOKEN not found in Render Environment!")
    else:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_signal))
        print("PAIN X BINARY IS STARTING...")
        app.run_polling()

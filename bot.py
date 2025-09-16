import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import requests
import json
import random
import time

# --- আপনার দেওয়া তথ্য ---
BOT_TOKEN = "7845699149:AAEEKpzHFt5gd6LbApfXSsE8de64f8IaGx0"
CURRENT_API = 'https://api.bdg88zf.com/api/webapi/GetGameIssue'
HISTORY_API = 'https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json'
REQUEST_DATA = { "typeId": 1, "language": 0, "random": "e7fe6c090da2495ab8290dac551ef1ed", "signature": "1F390E2B2D8A55D693E57FD905AE73A7", "timestamp": int(time.time()) }
# --- তথ্য শেষ ---


# API থেকে বর্তমান পিরিয়ড (period) সংগ্রহ করবে
async def get_current_period(api_url):
    try:
        response = requests.post(api_url, json=REQUEST_DATA)
        data = response.json()
        current_period = data['data']['issueId']
        return current_period
    except Exception as e:
        print(f"Error fetching current period: {e}")
        return None

# API থেকে খেলার ইতিহাস (history) সংগ্রহ করবে
async def get_history_results(api_url):
    try:
        response = requests.get(api_url)
        data = response.json()
        history_list = data['data']['history']
        return history_list
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

# সিগন্যাল তৈরি করবে (আপনার দেওয়া লজিক অনুযায়ী)
def generate_signal(history):
    if not history:
        return "No history available to generate a signal."
    
    latest_result = history[0]
    
    if latest_result['isBig']:
        return "Big"
    elif latest_result['isSmall']:
        return "Small"
    else:
        return "No clear signal based on history."

# /start কমান্ড হ্যান্ডেলার: এটি চারটি বাটন দেখাবে
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Get Signal", callback_data='get_signal')],
        [InlineKeyboardButton("Contact Admin", url="https://t.me/your_admin_username")],
        [InlineKeyboardButton("Rules", callback_data='rules')],
        [InlineKeyboardButton("Registration", url="https://api.bdg88zf.com/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('স্বাগতম! নিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় বাটনটি নির্বাচন করুন:', reply_markup=reply_markup)


# বাটনগুলোর জন্য হ্যান্ডেলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'get_signal':
        await get_signal(update, context)
    elif query.data == 'rules':
        await rules(update, context)

# সিগন্যাল পাওয়ার জন্য হ্যান্ডেলার
async def get_signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # ১ মিনিটের গেমের পিরিয়ড আইডি এবং হিস্টোরি API থেকে ডেটা আনা
        current_period = await get_current_period(CURRENT_API)
        history = await get_history_results(HISTORY_API)
        
        if current_period is None or not history:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I could not fetch the game information. Please try again later.")
            return
        
        signal = generate_signal(history)
        
        # মেসেজটি পিরিয়ড এবং সিগন্যাল সহ তৈরি
        signal_message = (
            f"🎯 **বর্তমান পিরিয়ড:** {current_period}\n"
            f"💡 **আমাদের সিগন্যাল:** পরবর্তী ফলাফল `{signal}` হতে পারে।"
        )
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=signal_message, parse_mode='Markdown')
        
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"সিগন্যাল পেতে সমস্যা হয়েছে। ({e})")

# রুলস দেখানোর জন্য হ্যান্ডেলার
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    rules_text = (
        "**নিয়মাবলী:**\n"
        "1. এই সিগন্যালগুলো শুধুমাত্র WinGo 1M খেলার জন্য।\n"
        "2. সিগন্যালগুলো অতীত ফলাফলের উপর ভিত্তি করে তৈরি করা হয় এবং সবসময় সঠিক নাও হতে পারে।\n"
        "3. খেলাটি নিজ দায়িত্বে খেলবেন।\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=rules_text, parse_mode='Markdown')

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    
    # কমান্ড হ্যান্ডেলার যোগ
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # বট শুরু
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

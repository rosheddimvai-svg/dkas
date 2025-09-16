import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json
import random
import time

# --- আপনার দেওয়া তথ্য ---
BOT_TOKEN = "7845699149:AAEEKpzHFt5gd6LbApfXSsE8de64f8IaGx0"
CURRENT_API = 'https://api.bdg88zf.com/api/webapi/GetGameIssue'
HISTORY_API = 'https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json'
# --- তথ্য শেষ ---

# API থেকে বর্তমান পিরিয়ড সংগ্রহ করবে (ডায়নামিক টাইমস্ট্যাম্প সহ)
async def get_current_period(api_url):
    try:
        REQUEST_DATA = { 
            "typeId": 1, 
            "language": 0, 
            "random": "e7fe6c090da2495ab8290dac551ef1ed", 
            "signature": "1F390E2B2D8A55D693E57FD905AE73A7", 
            "timestamp": int(time.time()) 
        }
        response = requests.post(api_url, json=REQUEST_DATA)
        data = response.json()
        current_period = data['data']['issueId']
        return current_period
    except Exception as e:
        print(f"Error fetching current period: {e}")
        return None

# API থেকে খেলার ইতিহাস সংগ্রহ করবে
async def get_history_results(api_url):
    try:
        response = requests.get(api_url)
        data = response.json()
        history_list = data['data']['history']
        return history_list
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

# সিগন্যাল তৈরি করবে
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
        [KeyboardButton("💰 Get Signal")],
        [KeyboardButton("👨‍💻 Contact Admin"), KeyboardButton("📜 Rules")],
        [KeyboardButton("✍️ Registration")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('স্বাগতম! নিচের মেনু থেকে আপনার প্রয়োজনীয় বাটনটি নির্বাচন করুন:', reply_markup=reply_markup)

# মেসেজ হ্যান্ডেলার: টেক্সট বার্তার জন্য
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    
    if text == "💰 Get Signal":
        await get_signal_message(update, context)
    elif text == "👨‍💻 Contact Admin":
        await contact_admin(update, context)
    elif text == "📜 Rules":
        await rules(update, context)
    elif text == "✍️ Registration":
        await registration(update, context)

# সিগন্যাল পাওয়ার জন্য হ্যান্ডেলার (বাটন থেকে কল হলে)
async def get_signal_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("সিগন্যাল তৈরি করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
        
        current_period = await get_current_period(CURRENT_API)
        history = await get_history_results(HISTORY_API)
        
        if current_period is None or not history:
            await update.message.reply_text("Sorry, I could not fetch the game information. Please try again later.")
            return
        
        signal = generate_signal(history)
        
        signal_message = (
            f"🎯 **বর্তমান পিরিয়ড:** {current_period}\n"
            f"💡 **আমাদের সিগন্যাল:** পরবর্তী ফলাফল `{signal}` হতে পারে।"
        )
        
        await update.message.reply_text(signal_message, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"সিগন্যাল পেতে সমস্যা হয়েছে। ({e})")

# কন্টাক্ট এডমিন হ্যান্ডেলার
async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👨‍💻 অ্যাডমিন এর সাথে যোগাযোগ করতে এখানে ক্লিক করুন: @Soyabur_AS_leaders")

# রুলস দেখানোর জন্য হ্যান্ডেলার
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    rules_text = (
        "**📜 নিয়মাবলী:**\n"
        "1. এই সিগন্যালগুলো শুধুমাত্র WinGo 1M খেলার জন্য।\n"
        "2. সিগন্যালগুলো অতীত ফলাফলের উপর ভিত্তি করে তৈরি করা হয় এবং সবসময় সঠিক নাও হতে পারে।\n"
        "3. খেলাটি নিজ দায়িত্বে খেলবেন।\n"
    )
    await update.message.reply_text(rules_text, parse_mode='Markdown')

# রেজিস্ট্রেশন হ্যান্ডেলার
async def registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✍️ রেজিস্ট্রেশন করতে এখানে ক্লিক করুন: https://dkwin12.com/#/register?invitationCode=82626111964")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

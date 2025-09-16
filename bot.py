import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import time
from datetime import datetime
import pytz
import random

# --- আপনার দেওয়া তথ্য ---
BOT_TOKEN = "7845699149:AAEEKpzHFt5gd6LbApfXSsE8de64f8IaGx0"
ADMIN_ID = "@Soyabur_AS_leaders" # এখানে আপনার অ্যাডমিন আইডি দিন
CHANNEL_NAME = "𝑨𝑺 𝑶𝑭𝑭𝑰𝑪𝑰𝑨𝑳 𝑪𝑯𝑨𝑵𝑵𝑬𝑳" # এখানে আপনার চ্যানেলের নাম দিন
# --- তথ্য শেষ ---

# বাংলাদেশ টাইমজোন সেট করা
BANGLADESH_TIMEZONE = pytz.timezone('Asia/Dhaka')

# প্রতিটি মিনিটের জন্য একটি নির্দিষ্ট সিগন্যাল তৈরি এবং সংরক্ষণ করার জন্য গ্লোবাল ভেরিয়েবল
current_minute_signal = None
last_minute_checked = -1

# সিগন্যাল তৈরি করবে
def generate_signal_for_minute(minute):
    random.seed(minute) # মিনিটের উপর ভিত্তি করে র্যান্ডম সিগন্যাল তৈরি করা
    return random.choice(["Big", "Small"])

# /start কমান্ড হ্যান্ডেলার: এটি ওয়েলকাম মেসেজ এবং মেনু বাটন দেখাবে
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        f"**╭── ⋅ ⋅ ── ✩ ── ⋅ ⋅ ──╮**\n"
        f"        **{CHANNEL_NAME}**\n"
        f"**╰── ⋅ ⋅ ── ✩ ── ⋅ ⋅ ──╯**\n"
        f"\n"
        f"👋 **স্বাগতম!**\n"
        f"✨ এই বটটি এক মাসের জন্য বিনামূল্যে ব্যবহার করতে পারবেন।\n"
        f"🚀 এখানে আপনি WinGo 1M গেমের জন্য সিগন্যাল পাবেন।\n"
        f"🔔 নোটিফিকেশন চালু রাখুন এবং প্রতিদিনের সিগন্যাল পেতে থাকুন।"
    )
    
    keyboard = [
        [KeyboardButton("💰 Get Signal")],
        [KeyboardButton("👨‍💻 Contact Admin"), KeyboardButton("📜 Rules")],
        [KeyboardButton("✍️ Registration")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')
    await update.message.reply_text('নিচের মেনু থেকে আপনার প্রয়োজনীয় বাটনটি নির্বাচন করুন:', reply_markup=reply_markup)

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

# সিগন্যাল পাওয়ার জন্য হ্যান্ডেলার
async def get_signal_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_minute_signal, last_minute_checked
    
    current_datetime_bst = datetime.now(BANGLADESH_TIMEZONE)
    current_minute = current_datetime_bst.minute
    
    # নতুন মিনিটে প্রবেশ করলে সিগন্যাল আপডেট করা
    if current_minute != last_minute_checked:
        current_minute_signal = generate_signal_for_minute(current_minute)
        last_minute_checked = current_minute
    
    formatted_time = current_datetime_bst.strftime('%H:%M:%S')
    
    signal_message = (
        f"**╭── ⋅ ⋅ ── ✩ ── ⋅ ⋅ ──╮**\n"
        f"        **{CHANNEL_NAME}**\n"
        f"**╰── ⋅ ⋅ ── ✩ ── ⋅ ⋅ ──╯**\n"
        f"\n"
        f"⏰ **বর্তমান সময়:** {formatted_time}\n"
        f"🔮 **আমাদের পরবর্তী সিগন্যাল:** `{current_minute_signal}`"
    )
    
    await update.message.reply_text(signal_message, parse_mode='Markdown')

# কন্টাক্ট এডমিন হ্যান্ডেলার
async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"👨‍💻 অ্যাডমিন এর সাথে যোগাযোগ করতে এখানে ক্লিক করুন: {ADMIN_ID}")

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

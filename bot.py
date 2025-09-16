import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import time
from datetime import datetime, timedelta
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
minute_signals = {}
last_updated_minute = -1

# সিগন্যাল তৈরি করবে
def generate_signal_for_minute(minute):
    random.seed(minute)
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
    global minute_signals, last_updated_minute
    
    current_datetime_bst = datetime.now(BANGLADESH_TIMEZONE)
    current_minute = current_datetime_bst.minute
    
    # নতুন মিনিটে প্রবেশ করলে সিগন্যাল আপডেট করা
    if current_minute != last_updated_minute:
        minute_signals = {}
        last_updated_minute = current_minute
        # পরবর্তী ৫ মিনিটের জন্য সিগন্যাল জেনারেট করা
        for i in range(5):
            future_minute = (current_minute + i) % 60
            minute_signals[i] = generate_signal_for_minute(future_minute)
    
    formatted_start_time = current_datetime_bst.strftime('%H:%M:%S')
    end_datetime = current_datetime_bst + timedelta(minutes=4, seconds=(59 - current_datetime_bst.second))
    formatted_end_time = end_datetime.strftime('%H:%M:%S')

    signal_list = ""
    for i, signal in minute_signals.items():
        future_time = current_datetime_bst + timedelta(minutes=i)
        future_formatted_time = future_time.strftime('%H:%M')
        signal_list += f"🎯 **{future_formatted_time}** ➡️ `{signal}`\n"
    
    signal_message = (
        f"**╭── ⋅ ⋅ ── ✩ ── ⋅ ⋅ ──╮**\n"
        f"        **{CHANNEL_NAME}**\n"
        f"**╰── ⋅ ⋅ ── ✩ ── ⋅ ⋅ ──╯**\n"
        f"\n"
        f"🔮 **ফিউচার সিগন্যাল জেনারেটর**\n"
        f"**শুরু:** `{formatted_start_time}`\n"
        f"**শেষ:** `{formatted_end_time}`\n"
        f"\n"
        f"**পরবর্তী সিগন্যালগুলো:**\n"
        f"{signal_list}"
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

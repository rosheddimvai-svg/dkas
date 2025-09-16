import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import time
from datetime import datetime
import pytz

# --- আপনার দেওয়া তথ্য ---
BOT_TOKEN = "7845699149:AAEEKpzHFt5gd6LbApfXSsE8de64f8IaGx0"
# --- তথ্য শেষ ---

# বাংলাদেশ টাইমজোন সেট করা
BANGLADESH_TIMEZONE = pytz.timezone('Asia/Dhaka')

# শেষ সিগন্যাল পাঠানোর সময় সংরক্ষণ করার জন্য একটি ভেরিয়েবল
last_signal_time = 0

# সিগন্যাল তৈরি করবে
def generate_random_signal():
    return random.choice(["Big", "Small"])

# /start কমান্ড হ্যান্ডেলার: এটি মেনু বাটন দেখাবে
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

# সিগন্যাল পাওয়ার জন্য হ্যান্ডেলার
async def get_signal_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global last_signal_time
    current_time = int(time.time())
    
    # শেষ সিগন্যাল পাঠানোর পর ৬০ সেকেন্ড পার হয়েছে কিনা তা যাচাই
    if current_time - last_signal_time < 60:
        await update.message.reply_text("দুঃখিত! আপনি একই মিনিটে একাধিক সিগন্যাল নিতে পারবেন না। দয়া করে একটু অপেক্ষা করুন।")
        return
    
    # বর্তমান পিরিয়ড আইডি তৈরি করা
    current_datetime_bst = datetime.now(BANGLADESH_TIMEZONE)
    period_id = current_datetime_bst.strftime('%Y%m%d%H%M')
    
    # একটি র্যান্ডম সিগন্যাল তৈরি করা
    signal = generate_random_signal()
    
    signal_message = (
        f"🎯 **বর্তমান পিরিয়ড:** {period_id}\n"
        f"💡 **আমাদের সিগন্যাল:** পরবর্তী ফলাফল `{signal}` হতে পারে।"
    )
    
    await update.message.reply_text(signal_message, parse_mode='Markdown')
    
    # শেষ সিগন্যাল পাঠানোর সময় আপডেট করা
    last_signal_time = current_time

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

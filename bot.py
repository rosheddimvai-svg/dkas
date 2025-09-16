import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import requests
import json
import random
import time

# --- config.py থেকে কোড এখানে যুক্ত করা হয়েছে ---
BOT_TOKEN = "7845699149:AAEEKpzHFt5gd6LbApfXSsE8de64f8IaGx0"
CURRENT_API = 'https://api.bdg88zf.com/api/webapi/GetGameIssue'
HISTORY_API = 'https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json'
REQUEST_DATA = { "typeId": 1, "language": 0, "random": "e7fe6c090da2495ab8290dac551ef1ed", "signature": "1F390E2B2D8A55D693E57FD905AE73A7", "timestamp": 1723726679 }
# --- config.py থেকে কোড এখানে শেষ ---


# আপনার API থেকে বর্তমান খেলার পিরিয়ড (period) সংগ্রহ করবে
async def get_current_period(api_url):
    try:
        response = requests.post(api_url, json=REQUEST_DATA)
        data = response.json()
        current_period = data['data']['lastGameInfo']['period']
        return current_period
    except Exception as e:
        print(f"Error fetching current period: {e}")
        return None

# আপনার API থেকে খেলার ইতিহাস (history) সংগ্রহ করবে
async def get_history_results(api_url):
    try:
        response = requests.get(api_url)
        data = response.json()
        history_list = data['data']['gameHistoryList']
        return history_list
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

# বিজয়ী সংখ্যা এবং রং বের করবে
def get_winner(number):
    number = int(number)
    if number == 0 or number == 5:
        return '💜', 'Green-Violet' if number == 5 else 'Red-Violet'
    elif number in [1, 3, 7, 9]:
        return '💚', 'Green'
    else:
        return '❤️', 'Red'

# সিগন্যাল তৈরি করবে
def generate_signal(history):
    if len(history) < 2:
        return "Not enough history to generate a signal."
    
    last_result_number = history[0]['number']
    second_last_result_number = history[1]['number']
    
    last_winner_color = get_winner(last_result_number)[1]
    second_last_winner_color = get_winner(second_last_result_number)[1]
    
    if last_winner_color == second_last_winner_color:
        if last_winner_color == 'Green':
            return "Buy: Red"
        elif last_winner_color == 'Red':
            return "Buy: Green"
        else:
            return random.choice(["Buy: Green", "Buy: Red"])
    else:
        return random.choice(["Buy: Green", "Buy: Red"])

# /start কমান্ড হ্যান্ডেলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("WinGo 1M", callback_data='get_signal_1M')],
        [InlineKeyboardButton("WinGo 3M", callback_data='get_signal_3M')],
        [InlineKeyboardButton("WinGo 5M", callback_data='get_signal_5M')],
        [InlineKeyboardButton("WinGo 10M", callback_data='get_signal_10M')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('সিগন্যাল পেতে নিচের একটি বাটন চাপুন:', reply_markup=reply_markup)

# সিগন্যাল পাওয়ার জন্য হ্যান্ডেলার
async def get_signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    game_type = query.data.split('_')[1]
    
    await query.edit_message_text(f'Fetching signal for WinGo {game_type.upper()}...')
    
    if game_type == '1M':
        current_api_url = CURRENT_API
        history_api_url = HISTORY_API
    else:
        await query.edit_message_text("Sorry, this feature is only for WinGo 1M right now.")
        return
        
    current_period = await get_current_period(current_api_url)
    history = await get_history_results(history_api_url)
    
    if current_period is None or not history:
        await query.edit_message_text("Sorry, I could not fetch the game information. Please try again later.")
        return
        
    signal = generate_signal(history)
    
    await query.edit_message_text(f"WinGo {game_type.upper()} Period: **{current_period}**\nSignal: **{signal}**", parse_mode='Markdown')

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(get_signal))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
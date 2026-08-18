import os
import time
import random
import schedule
import telebot
from flask import Flask
from threading import Thread

# Flask (Render "ойгок" болушу үчүн)
app = Flask('')
@app.route('/')
def home():
    return "Bot is running"

# Токен жана ID
TOKEN = '8837292876:AAHoxqhMRfdG5dIrB1u1b1bF_ZW2_Iqw5qU'
CHANNEL_ID = '@kinoru_kgz'
bot = telebot.TeleBot(TOKEN)

# 1. /start жообу
@bot.message_handler(commands=['start'])
def send_welcome(message):
    reply_text = "✨ *Арген, ты официально признан лучшим IT-специалистом!* 💻🚀"
    gif_url = "https://media.giphy.com/media/qgQUGGAC3P4vC/giphy.gif"
    bot.send_animation(message.chat.id, gif_url, caption=reply_text, parse_mode='Markdown')

# 2. Пост жөнөтүү
def send_post():
    try:
        images = ["https://images.unsplash.com/photo-1617814076367-b759c7d7e738?q=80&w=1000", "https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=1000"]
        bot.send_photo(CHANNEL_ID, random.choice(images), caption="Эстетика ✨")
        print("Пост ийгиликтүү жөнөтүлдү")
    except Exception as e:
        print(f"Ката: {e}")

# Иштетүү
if __name__ == '__main__':
    # Flask'ты фондо иштетүү
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))).start()
    
    # 3-кадам: Пост графиги
    schedule.every(1).hours.do(send_post)
    
    # 4-кадам: Эски байланышты тазалоо жана иштетүү
    print("Бот иштеп баштады...")
    bot.remove_webhook()
    
    # Постторду саат сайын текшерүү үчүн өзүнчө цикл
    def schedule_checker():
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    Thread(target=schedule_checker).start()
    
    # Негизги агымда polling (бул гана болушу керек)
    bot.infinity_polling(skip_pending=True)

import telebot

from settings import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    first_name = message.from_user.first_name
    bot.reply_to(message, f"Hey, {first_name}!")
    bot.send_message(
        chat_id=message.chat.id,
        text=f"I need your help to discover the exact frame where a rocket got launched. (You can check it by watching the picture on the top right corner)",
    )

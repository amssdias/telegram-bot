from bot.messages import RocketBot
from settings import BOT_TOKEN


if __name__ == "__main__":
    bot = RocketBot(BOT_TOKEN)

    bot.start()

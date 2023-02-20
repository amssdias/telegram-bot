from bot.rocket_bot import RocketBot
from settings.settings import BOT_TOKEN


if __name__ == "__main__":
    bot = RocketBot(BOT_TOKEN)

    bot.start()

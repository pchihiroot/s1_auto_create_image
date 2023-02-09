from discord.ext import commands
from discord import (
    Intents,
)
from dotenv import load_dotenv
import os

load_dotenv()

COGS = ["cogs.create_image"]

TOKEN = os.environ.get("TOKEN")


class Main(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=Intents.all())

        self.api_url = os.environ.get("API_SERVER")
        self.trans_api_url = os.environ.get("TRANS_API_SERVER")

    async def setup_hook(self) -> None:
        for cog in COGS:
            await self.load_extension(cog)

        await self.tree.sync()

    async def on_ready(self):
        print("BOTが起動しました")
        print("BOT USER NAME: ", str(self.user))
        print("BOT USER ID: ", self.user.id)


if __name__ == "__main__":
    bot = Main()
    bot.run(TOKEN)

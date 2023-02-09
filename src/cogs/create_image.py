from __future__ import annotations

from discord.ext import commands
from discord import app_commands, File

from aiohttp import ClientSession
import os


class Create_Image(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot

    @commands.hybrid_command(name="画像生成")
    async def create_image(self, ctx: commands.Context, prompt: str):
        m = await ctx.send("画像を生成しています。30秒ほどかかりますので、しばらくお待ちください。")

        async with ClientSession() as session:
            async with session.post(self.bot.trans_api_url, json={"prompt": prompt}) as resp:
                jpn_prompt = await resp.json()
        
        async with ClientSession() as session:
            async with session.post(self.bot.api_url, json={"prompt": jpn_prompt["result"]}) as resp:
                data = await resp.read()
                print("pong data")
                with open(f"./imgs/{ctx.author.id}.png", "wb") as f:
                    print("write file")
                    f.write(data)

        img = File(f"./imgs/{ctx.author.id}.png", filename=f"{prompt}.png")
        print(str(ctx.author), "の画像を生成しました")

        await m.edit(content=f"**画像の生成が完了しました。**\nキーワード: {prompt}", attachments=[img])

        os.remove(f"./imgs/{ctx.author.id}.png")


async def setup(bot):
    await bot.add_cog(Create_Image(bot))

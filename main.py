from __future__ import annotations

import logging
import os
import traceback
from typing import Any, Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import EXTENSIONS
from command_tree import JDCommandTranslator, JDCommandTree


class JDBot(commands.Bot):
    tree: JDCommandTree  # type: ignore

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        await self.tree.set_translator(JDCommandTranslator())

        for cog in EXTENSIONS:
            try:
                await self.load_extension(f"{cog}")
            except commands.errors.ExtensionError:
                traceback.print_exc()

    async def try_user(self, id: int, /) -> Optional[discord.User]:
        maybe_user = self.get_user(id)

        if maybe_user is not None:
            return maybe_user

        try:
            return await self.fetch_user(id)
        except discord.errors.NotFound:
            return None


intents = discord.Intents.all()

bot = JDBot(
    command_prefix="h$",
    intents=intents,
    chunk_guilds_at_startup=False,
    strip_after_prefix=True,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
)


@bot.event
async def on_ready():
    print(bot.user)
    print(bot.user.id)


load_dotenv()
logging.basicConfig(level=logging.INFO)
bot.run(os.environ["TOKEN"])

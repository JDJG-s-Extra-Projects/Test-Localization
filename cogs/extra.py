from __future__ import annotations

import typing

import discord
from discord import app_commands
from discord.ext import commands

from local_utils import Temperature

if typing.TYPE_CHECKING:
    from main import JDBot


class Extra(commands.Cog):
    "Uncategorized Commands, these are more random commands"

    def __init__(self, bot: JDBot):
        self.bot: JDBot = bot

    @app_commands.user_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="A command to convert temperatures to different scales")
    async def convert_temperature(
        self,
        interaction: discord.Interaction,
        temp_system: Temperature,
        temperature: float,
    ):
        temps = temp_system.convert_to(temperature)

        if temps.celsius < 20:
            color = 0x0000FF

        if temps.celsius >= 20 and temps.celsius <= 30:
            color = 0xFFA500

        if temps.celsius > 30:
            color = 0xFF0000

        temp_celsius = f"{temps.celsius:,}"
        temp_fahrenheit = f"{temps.fahrenheit:,}"
        temp_kelvin = f"{temps.kelvin:,}"
        temp_rankine = f"{temps.rankine:,}"
        temp_system_value = str(temp_system.value)

        embed = discord.Embed(title="Temperature:", color=color)
        embed.add_field(name="Celsius:", value="{temp_celsius} °C")
        embed.add_field(name="Fahrenheit:", value="{temp_fahrenheit} °F")
        embed.add_field(name="Kelvin:", value="{temp_kelvin} K")
        embed.add_field(name="Rankine:", value="{temp_rankine} °R")
        embed.set_footer(text="Chose: {temp_system_value}")

        embeds = await self.bot.tree.translator.translate_embeds(
            interaction,
            [embed],
            temp_celsius=temp_celsius,
            temp_fahrenheit=temp_fahrenheit,
            temp_kelvin=temp_kelvin,
            temp_rankine=temp_rankine,
            temp_system_value=temp_system_value,
        )
        await interaction.response.send_message(embeds=embeds)

        print(interaction.locale)
        # debug print.

    @convert_temperature.error
    async def convert_temperature_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(interaction.command)
        traceback.print_exc()


async def setup(bot: JDBot):
    await bot.add_cog(Extra(bot))

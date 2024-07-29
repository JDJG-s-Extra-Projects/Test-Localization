from __future__ import annotations

import asyncio
import traceback
import typing
import zoneinfo

import discord
from discord import app_commands
from discord.ext import commands

from local_utils import Speed, Temperature, locale_choices

if typing.TYPE_CHECKING:
    from main import JDBot


class Extra(commands.Cog):
    "Uncategorized Commands, these are more random commands"

    def __init__(self, bot: JDBot):
        self.bot: JDBot = bot

    @app_commands.command(
        description="A command to convert temperatures to different scales",
        auto_locale_strings=True,
    )
    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        temperature_unit="Select a Unit Temperature from the dropdown.",
        temperature="Please enter a number",
    )
    @app_commands.choices(
        temperature_unit=locale_choices(
            {
                "Celsius": "celsius",
                "Fahrenheit": "fahrenheit",
                "Kelvin": "kelvin",
                "Rankine": "rankine",
            },
            command_name="convert_temperature",
            option_name="temperature_unit",
        )
    )
    async def convert_temperature(
        self,
        interaction: discord.Interaction[JDBot],
        temperature_unit: app_commands.Choice[str],
        temperature: float,
    ):
        temps = Temperature[temperature_unit.value].convert_to(temperature)

        if temps.celsius < 20:
            color = 0x0000FF

        elif temps.celsius >= 20 and temps.celsius <= 30:
            color = 0xFFA500
        else:
            color = 0xFF0000

        temp_celsius = f"{temps.celsius:,}"
        temp_fahrenheit = f"{temps.fahrenheit:,}"
        temp_kelvin = f"{temps.kelvin:,}"
        temp_rankine = f"{temps.rankine:,}"

        temperature_unit_value = (
            await interaction.client.tree.translator.translate_choice_name_from_locale_key(
                interaction.locale, temperature_unit._locale_name
            )
            or temperature_unit.value
        )

        embed = discord.Embed(title="Temperature:", color=color)
        embed.add_field(name="Celsius:", value="{temp_celsius} °C")
        embed.add_field(name="Fahrenheit:", value="{temp_fahrenheit} °F")
        embed.add_field(name="Kelvin:", value="{temp_kelvin} K")
        embed.add_field(name="Rankine:", value="{temp_rankine} °R")
        embed.set_footer(text="Chose: {temperature_unit_value}")

        embeds = await self.bot.tree.translator.translate_embeds(
            interaction,
            [embed],
            temp_celsius=temp_celsius,
            temp_fahrenheit=temp_fahrenheit,
            temp_kelvin=temp_kelvin,
            temp_rankine=temp_rankine,
            temperature_unit_value=temperature_unit_value,
        )
        await interaction.response.send_message(embeds=embeds)

        print(interaction.locale)
        # debug print.

    @convert_temperature.error
    async def convert_temperature_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(interaction.command)
        traceback.print_exc()

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        speed_unit="Select a Unit of Speed from the dropdown.",
        speed="Please enter a number",
    )
    @app_commands.command(
        description="A command to convert speeds to different scales",
        auto_locale_strings=True,
    )
    @app_commands.choices(
        speed_unit=locale_choices(
            Speed,
            command_name="convert_speed",
            option_name="speed_unit",
        )
    )
    async def convert_speed(self, interaction: discord.Interaction, speed_unit: app_commands.Choice[str], speed: float):
        speeds = Speed[speed_unit.name].convert_to(speed)

        if speeds.miles <= 25:
            color = 0xFFFF00

            # 25 miles per hour in a us residence zone
            # yellow for a small speed

        if speeds.miles > 25 and speeds.miles <= 55:

            color = 0x8450

            # 55 mph speed limit on rural highways
            # green for about a not so slow speed.

        if speeds.miles > 55 and speeds.miles <= 70:

            color = 0x26F7FD

            # 70 mph is the max on rural interstate highways
            # color is choosen from the hydro thunder hurriance boost colors as close as I could match

        # https://highways.dot.gov/safety/speed-management/speed-limit-basics
        # information gathered from here.

        if speeds.miles > 70 and speeds.miles <= 85:

            # texas has the highest maximum sped limit at 85 mph according to
            # https://worldpopulationreview.com/state-rankings/speed-limit-map-by-state

            color = 0x8B

            # color choosen for faster boost color essentially

        if speeds.miles > 85 and speeds.miles <= 212.81:

            # https://rerev.com/articles/how-fast-do-nascar-cars-go
            # 212.809 miles per hour is the maximum they go up to.
            # rounded to 212.81 for convivence

            color = 0xCC0202
            # red for please don't go this speed normally.

        if speeds.miles > 212.81:
            # basically please don't go more than this speed unless you are in a plane or so other faster vehicle
            color = 0x0
            # pure black for emphasis.

        speeds_miles = f"{speeds.miles:,}"
        speeds_kilometers = f"{speeds.kilometers:,}"
        speeds_meters = f"{speeds.meters:,}"
        speeds_feet = f"{speeds.feet:,}"
        speeds_megameters = f"{speeds.megameters:,}"
        speeds_light = f"{speeds.light:,}"

        speed_unit_value = (
            await interaction.client.tree.translator.translate_choice_name_from_locale_key(
                interaction.locale, speed_unit._locale_name
            )
            or speed_unit.value
        )

        embed = discord.Embed(title="Speed:", color=color)
        embed.add_field(name="Miles:", value=f"{speeds_miles} mi")
        embed.add_field(name="Kilometers:", value=f"{speeds_kilometers} km")
        embed.add_field(name="Meters:", value=f"{speeds_meters} m")
        embed.add_field(name="Feet", value=f"{speeds_feet} ft")
        embed.add_field(name="Megameters", value=f"{speeds_megameters} Mm")
        embed.add_field(name="Constants (Speed of Light):", value=f"{speeds_light} C")

        # megameters and light speed are elite dangerous references
        # see https://www.reddit.com/r/EliteDangerous/s/1AgiKH9Xj0

        embed.set_footer(text=f"Chose: {speed_unit_value}")

        embeds = await self.bot.tree.translator.translate_embeds(
            interaction,
            [embed],
            speeds_miles=speeds_miles,
            speeds_kilometers=speeds_kilometers,
            speeds_meters=speeds_meters,
            speeds_feet=speeds_feet,
            speeds_megameters=speeds_megameters,
            speeds_light=speeds_light,
            speed_unit_value=speed_unit_value,
        )
        await interaction.response.send_message(embeds=embeds)

    @convert_speed.error
    async def convert_speed_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(interaction.command)
        traceback.print_exc()

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        timezone="Select the timezone you would like to convert to.",
    )
    @app_commands.command(description="A command to convert the message timestamp to the region's time.")
    async def convert_timezone(self, interaction: discord.Interaction, timezone: typing.Optional[str] = None):

        timezones = self.available_timezones
        # no json format exists for this yet.

        if not timezone:
            timestamp = discord.utils.format_dt(interaction.created_at)
            embed = discord.Embed(title="Time:", description=timestamp)
            embed.set_footer(text="Timezone: Not Specified")

        elif not timezone in timezones:
            timestamp = discord.utils.format_dt(interaction.created_at)
            embed = discord.Embed(title="Time:", description=timestamp)
            embed.set_footer(text="Timezone: Not Found")

        else:
            now_tz = interaction.created_at.astimezone(zoneinfo.ZoneInfo(timezone))
            am_pm_format = now_tz.strftime("%I:%M:%S %p")
            twenty_four_format = now_tz.strftime("%H:%M:%S")
            first_format = now_tz.strftime("%Y-%d-%m")
            second_format = now_tz.strftime("%d-%m-%Y")
            third_format = now_tz.strftime("%m-%d-%Y")

            # possibly do colors depending on time but not sure.

            embed = discord.Embed(
                title="Time:",
                description=f"12 hour: {am_pm_format}\n24 hour: {twenty_four_format}\n\nYYYY-DD-MM: {first_format}\nDD-MM-YYYY: {second_format}\nMM-DD-YYYY: {third_format}",
            )
            embed.set_footer(text=f"Timezone: {timezone}")

        await interaction.response.send_message(embed=embed)

    @convert_timezone.autocomplete("timezone")
    async def convert_timezone_autocomplete(self, interaction: discord.Interaction, current: str) -> list[Choice]:

        timezones = self.available_timezones
        all_choices = [Choice(name=timezone, value=timezone) for timezone in timezones]

        if not (current):
            return all_choices[0:25]

        filtered_results = fuzzy.finder(current, timezones)
        results = [Choice(name=result, value=result) for result in filtered_results]

        return results[0:25]

    @convert_timezone.error
    async def convert_timezone_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(interaction.command)
        traceback.print_exc()


async def setup(bot: JDBot):
    await bot.add_cog(Extra(bot))

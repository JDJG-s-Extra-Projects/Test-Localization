import enum
from typing import TYPE_CHECKING, Any, NamedTuple

from discord import app_commands
from discord.app_commands import locale_str


class TemperatureReadings(NamedTuple):
    celsius: int
    fahrenheit: int
    kelvin: int
    rankine: int


class Temperature(enum.Enum):
    celsius = "Celsius"
    fahrenheit = "Fahrenheit"
    kelvin = "Kelvin"
    rankine = "Rankine"

    def convert_to(self, value: float) -> TemperatureReadings:
        match self:
            case Temperature.celsius:
                c = value
                k = c + 273.15
                f = (c * 1.8) + 32
                r = f + 459.67

            case Temperature.fahrenheit:
                f = value
                c = (f - 32) * 0.5556
                k = c + 273.15
                r = f + 459.67

            case Temperature.kelvin:
                k = value
                c = k - 273.15
                f = (c * 1.8) + 32
                r = f + 459.67

            case Temperature.rankine:
                r = value
                f = r - 459.67
                c = (f - 32) * 0.5556
                k = c + 273.15

        return TemperatureReadings(round(c, 1), round(f, 1), round(k, 1), round(r, 1))

class SpeedReadings(NamedTuple):
    miles: float
    kilometers: float
    meters: float
    feet: float
    megameters: float
    light: float


class Speed(enum.Enum):
    miles = "Miles"
    kilometers = "Kilometers"
    meters = "Meters"
    feet = "Feet"
    megameters = "Megameters"
    light = "Light Speed"

    def convert_to(self, value: float) -> SpeedReadings:
        match self:
            case Speed.miles:
                miles = value
                kilometers = 1.609344 * miles
                meters = kilometers * 1000
                feet = 5280 * miles
                megameters = kilometers / 1000
                light = meters / 299792458
                # https://en.wikipedia.org/wiki/Speed_of_light

            case Speed.kilometers:
                kilometers = value
                meters = kilometers * 1000
                miles = kilometers / 1.609344
                feet = 5280 * miles
                megameters = kilometers / 1000
                light = meters / 299792458

            case Speed.meters:
                meters = value
                kilometers = meters / 1000
                megameters = kilometers / 1000
                light = meters / 299792458
                miles = kilometers / 1.609344
                feet = 5280 * miles

            case Speed.feet:
                feet = value
                miles = feet / 5280
                kilometers = miles * 1.609344
                meters = kilometers * 1000
                megameters = kilometers / 1000
                light = meters / 299792458

            case Speed.megameters:
                megameters = value
                kilometers = megameters * 1000
                meters = kilometers * 1000
                light = meters / 299792458
                miles = kilometers / 1.609344
                feet = 5280 * miles

            case Speed.light:
                light = value
                meters = light * 299792458
                kilometers = meters / 1000
                miles = kilometers / 1.609344
                feet = 5280 * miles
                megameters = kilometers / 1000

        return SpeedReadings(
            round(miles, 2),
            round(kilometers, 2),
            round(meters, 2),
            round(feet, 2),
            round(megameters, 2),
            round(light, 2),
        )


def locale_choices(
    choices: dict[str, str] | list[str], /, command_name: str, option_name: str
) -> list[app_commands.Choice]:
    if isinstance(choices, list):
        choices = {choice: choice for choice in choices}

    return [
        app_commands.Choice(
            name=locale_str(name, key=f"{command_name}:{option_name}:{i}"),
            value=value,
        )
        for i, (name, value) in enumerate(choices.items())
    ]

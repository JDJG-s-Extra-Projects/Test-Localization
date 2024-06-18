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


def locale_choices(
    choices: dict[str, str], /, command_name: str, option_name: str
) -> list[app_commands.Choice]:
    return [
        app_commands.Choice(
            name=locale_str(name, key=f"{command_name}:{option_name}:{i}"),
            value=value,
        )
        for i, (name, value) in enumerate(choices.items())
    ]

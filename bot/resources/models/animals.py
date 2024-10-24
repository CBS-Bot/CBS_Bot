import discord
from typing import Literal


ANIMAL_LITERAL = Literal["fox", "yeen", "dog", "manul", "snek", "poss", "serval", "bleat",
                         "shiba", "racc", "dook", "ott", "snep", "woof", "capy", "bear", "bun",
                         "caracal", "puma", "mane", "marten", "wah", "skunk", "jaguar", "yote"]

RATING_MAPPINGS = {"SSSS":  {"weight": 0.005, "color": discord.Color.from_rgb(192, 215, 255)},
                   "SSS+":  {"weight": 0.010, "color": discord.Color.from_rgb(255, 255, 255)},
                   "SSS":   {"weight": 0.015, "color": discord.Color.from_rgb(204, 0,   102)},
                   "SS+":   {"weight": 0.020, "color": discord.Color.from_rgb(204, 0,   0)},
                   "SS":    {"weight": 0.025, "color": discord.Color.from_rgb(255, 51,  0)},
                   "S+":    {"weight": 0.030, "color": discord.Color.from_rgb(255, 153, 51)},
                   "S":     {"weight": 0.045, "color": discord.Color.from_rgb(255, 153, 102)},
                   "A":     {"weight": 0.400, "color": discord.Color.from_rgb(153, 0,   255)},
                   "B":     {"weight": 0.200, "color": discord.Color.from_rgb(51,  51,  255)},
                   "C":     {"weight": 0.150, "color": discord.Color.from_rgb(102, 255, 51)},
                   "D":     {"weight": 0.100, "color": discord.Color.from_rgb(166, 166, 166)}}
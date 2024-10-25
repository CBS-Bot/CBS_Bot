import discord
from typing import Literal
from definitions import ROOT_DIR


ANIMAL_LITERAL = Literal["fox", "yeen", "dog", "manul", "snek", "poss", "serval", "bleat",
                         "shiba", "racc", "dook", "ott", "snep", "woof", "capy", "bear", "bun",
                         "caracal", "puma", "mane", "marten", "wah", "skunk", "jaguar", "yote"]

RATING_MAPPINGS = {"SSSS":  {"weight": 0.005, "color": discord.Color.from_rgb(192, 215, 255),
                             "filename": "SSSS.png"},
                   "SSS+":  {"weight": 0.010, "color": discord.Color.from_rgb(255, 255, 255),
                             "filename": "SSSplus.png"},
                   "SSS":   {"weight": 0.015, "color": discord.Color.from_rgb(204, 0,   102),
                             "filename": "SSS.png"},
                   "SS+":   {"weight": 0.020, "color": discord.Color.from_rgb(204, 0,   0),
                             "filename": "SSplus.png"},
                   "SS":    {"weight": 0.025, "color": discord.Color.from_rgb(255, 51,  0),
                             "filename": "SS.png"},
                   "S+":    {"weight": 0.030, "color": discord.Color.from_rgb(255, 153, 51),
                             "filename": "Splus.png"},
                   "S":     {"weight": 0.045, "color": discord.Color.from_rgb(255, 153, 102),
                             "filename": "S.png"},
                   "A":     {"weight": 0.400, "color": discord.Color.from_rgb(153, 0,   255),
                             "filename": "A.png"},
                   "B":     {"weight": 0.200, "color": discord.Color.from_rgb(51,  51,  255),
                             "filename": "B.png"},
                   "C":     {"weight": 0.150, "color": discord.Color.from_rgb(102, 255, 51),
                             "filename": "C.png"},
                   "D":     {"weight": 0.100, "color": discord.Color.from_rgb(166, 166, 166),
                             "filename": "D.png"}}

RATING_IMAGE_DIR = ROOT_DIR + "/bot/resources/media/ratings/"
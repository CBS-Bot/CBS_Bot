import typing
import discord
import msgspec
from definitions import ROOT_DIR
from msgspec import Struct


class TableFolder(Struct, kw_only=True):
    table: str = ""
    level: str = ""


class ChartData(Struct, kw_only=True):
    aiLevel: typing.Optional[str] = ""
    hashMD5: str = ""
    hashSHA256: str = ""
    notecount: int = 0
    sglEC: typing.Optional[float] = 0
    sglHC: typing.Optional[float] = 0
    tableFolders: list[TableFolder] = None


class Chart(Struct, kw_only=True):
    chartID: str = ""
    data: ChartData = None
    difficulty: str = ""
    isPrimary: bool = False
    level: str = ""
    levelNum: int = 0
    playtype: str = ""
    songID: int = 0
    versions: list[str] = list[""]

    readable_str: str = "" # Added to help search.


class SongData(Struct, kw_only=True):
    genre: typing.Optional[str] = ""
    subartist: typing.Optional[str] = ""
    subtitle: typing.Optional[str] = ""
    tableString: typing.Optional[str] = ""


class Song(Struct, kw_only=True):
    altTitles: list[str] = list[""]
    artist: str = ""
    data: SongData = None
    id: int = 0
    searchTerms: list[str] = list[""]
    title: str = ""

class Table(Struct, kw_only=True):
    default: bool = False
    description: str = ""
    folders: list[str] = list[""]
    game: str = ""
    inactive: bool = False
    playtype: str = ""
    tableID: str = ""
    title: str = ""

class ElemMatch(Struct, kw_only=True):
    level: typing.Any
    table: str = ""

class DataTableFolderData(Struct, kw_only=True):
    elemMatch: ElemMatch = None

class FolderData(Struct, kw_only=True):
    datatableFolders: DataTableFolderData = None

class Folder(Struct, kw_only=True):
    data: FolderData = None
    folderID: str = ""
    game: str = ""
    inactive: bool = False
    playtype: str = ""
    searchTerms: list[str] = list[""]
    title: str = ""
    type: str = ""

LEVEL_MAPPINGS = {"novice": {"shorthand": "NOV", "url_mapping": "1",
                             "color": discord.Color.from_rgb(145, 75, 198)},
                  "advanced": {"shorthand": "ADV", "url_mapping": "2",
                               "color": discord.Color.from_rgb(168, 163, 7)},
                  "exhaust": {"shorthand": "EXH", "url_mapping": "3",
                              "color": discord.Color.from_rgb(148, 52, 52)},
                  "maximum": {"shorthand": "MXM", "url_mapping": "5",
                              "color": discord.Color.from_rgb(112, 112, 112)},
                  "infinite": {"shorthand": "INF", "url_mapping": "4i",
                               "color": discord.Color.from_rgb(179, 37, 101)},
                  "gravity": {"shorthand": "GRV", "url_mapping": "4g",
                              "color": discord.Color.from_rgb(158, 66, 0)},
                  "heavenly": {"shorthand": "HVN", "url_mapping": "4h",
                               "color": discord.Color.from_rgb(0, 127, 166)},
                  "vivid": {"shorthand": "VVD", "url_mapping": "4v",
                            "color": discord.Color.from_rgb(184, 68, 155)},
                  "exceed": {"shorthand": "XCD", "url_mapping": "4x",
                             "color": discord.Color.from_rgb(54, 81, 145)}}

JSON_DIR = ROOT_DIR + "/bot/resources/fnc/collections/"
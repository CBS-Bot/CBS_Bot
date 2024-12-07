import re

import discord
import logging
import typing
from typing import List
from thefuzz import process, utils
from discord import app_commands
from discord.ext import commands

from bot.resources.fnc.bms.bmsviewerfncmodels import TableFolder
from bot.resources.fnc.bms.bmsviewerfncstrategy import BmsViewerFncStrategy


def get_table_str(table_folders: list[TableFolder]) -> str:
    if len(table_folders) == 0:
        return "No Table -"
    test = ', '.join([f"{x.table}{x.level}" for x in table_folders]) + " -"
    return test

class BmsViewerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.strategy = BmsViewerFncStrategy(x1_left_px=9,
                                            x2_left_px=32,
                                            y1_bottom_px=44,
                                            y2_bottom_px=0,
                                            spacing_px=117,
                                            doubles_spacing_px=None,
                                            bottom_cutoff_px=24,
                                            ocr_scale_multiplier=2,
                                            measure_oob_tol=20,
                                            game_title="bms")


    async def chart_autocomplete_bychart(self, interaction: discord.Interaction, current: str) \
            -> List[discord.app_commands.Choice[str]]:
        songs = await self.strategy.get_songs()
        song_titles = [x.title for x in songs]
        if utils.full_process(current):
            closest_matches = process.extract(current, list(set(song_titles)), limit=25)
            return [
                app_commands.Choice(name=x[0], value=x[0])
                for x in closest_matches
                ]

    async def difficulty_autocomplete_bychart(self, interaction: discord.Interaction, current: str) \
            -> List[discord.app_commands.Choice[str]]:
        songs = await self.strategy.get_song(title=interaction.namespace.chart)
        difficulties = await self.strategy.get_difficulties(songs=songs)
        logging.warning(difficulties[0])
        unique_notecounts = [x.data.notecount for x in difficulties]
        if utils.full_process(current):
            closest_matches = process.extract(current, unique_notecounts, limit=25)
            logging.warning(f"closest_matches {closest_matches}")
            return [
                app_commands.Choice(name=x[0], value=next(y.chartID for y in difficulties if x[0] == y.readable_str))
                for x in closest_matches
            ]

    async def table_autocomplete_bytable(self, interaction: discord.Interaction, current: str) \
            -> List[discord.app_commands.Choice[str]]:
        tables = await self.strategy.get_tables()
        table_names = [x.title for x in tables]
        if utils.full_process(current):
            closest_matches = process.extract(current, table_names, limit=25)
            return [
                app_commands.Choice(name=x[0], value=x[0])
                for x in closest_matches
                ]

    async def chart_autocomplete_bytable(self, interaction: discord.Interaction, current: str) \
            -> List[discord.app_commands.Choice[str]]:
        selected_table = await self.strategy.get_table(title=interaction.namespace.table)
        folders = await self.strategy.get_folders()
        selected_table_titles = [x.title for x in folders
                                 if x.folderID in selected_table.folders]

        songs = await self.strategy.get_songs()
        selected_table_songs = [x.title for x in songs if x.data.tableString in selected_table_titles]

        if utils.full_process(current):
            closest_matches = process.extract(current, list(set(selected_table_songs)), limit=25)
            return [
                app_commands.Choice(name=x[0], value=x[0])
                for x in closest_matches
                ]

    async def difficulty_autocomplete_bytable(self, interaction: discord.Interaction, current: str) \
            -> List[discord.app_commands.Choice[str]]:
        songs = await self.strategy.get_song(title=interaction.namespace.chart)
        difficulties = await self.strategy.get_difficulties(songs=songs)
        logging.warning(f"difficulties {difficulties}")
        return [
            app_commands.Choice(name=f"{get_table_str(x.data.tableFolders)} {x.data.notecount} notes - "
                                     f"{x.playtype}", value=str(x.chartID))
            for x in difficulties
            ]

    @app_commands.command(name="bmsviewer_bysong", description="Retrieve a chart from "
                                                               "https://bms-score-viewer.pages.dev/, by song.")
    @app_commands.describe(chart="Start typing for a list of suggestions based on your input.")
    @app_commands.describe(difficulty="Choose a difficulty for the song.")
    @app_commands.describe(bar_clip="Select a portion of the song, for example 20-30. The default is 1-15.")
    @app_commands.autocomplete(chart=chart_autocomplete_bychart, difficulty=difficulty_autocomplete_bychart)
    async def bmsviewer_bychart(self, ctx, chart: str, difficulty: str, bar_clip: typing.Optional[str],
                               random: typing.Optional[str]) -> None:
        await ctx.response.defer()
        await self.strategy.execute_strategy(ctx, song=chart, difficulty=difficulty, bar_clip=bar_clip,
                                             random=random)

    @app_commands.command(name="bmsviewer_bytable", description="Retrieve a chart from "
                                                       "https://bms-score-viewer.pages.dev/, by table.")
    @app_commands.describe(chart="Start typing for a list of suggestions based on your input.")
    @app_commands.describe(difficulty="Choose a difficulty for the song.")
    @app_commands.describe(bar_clip="Select a portion of the song, for example 20-30. The default is 1-15.")
    @app_commands.autocomplete(table=table_autocomplete_bytable, chart=chart_autocomplete_bytable,
                               difficulty=difficulty_autocomplete_bytable                               )
    async def bmsviewer_bytable(self, ctx, table: str, chart: str, difficulty: str, bar_clip: typing.Optional[str],
                               random: typing.Optional[str]) -> None:
        await ctx.response.defer()
        await self.strategy.execute_strategy(ctx, song=chart, table=table, difficulty=difficulty, bar_clip=bar_clip,
                                             random=random)


def setup(bot):
    logging.warning("BMS Viewer cog added.")
    bot.add_cog(BmsViewerCog(bot))

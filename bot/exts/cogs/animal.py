import logging
import requests
from discord.ext import commands

from bot.resources.animals import ANIMAL_LITERAL


def get_random_animal_image(animal: str) -> str:
    response = requests.get("https://api.tinyfox.dev/img.json", {'animal': animal})
    return "https://api.tinyfox.dev" + response.json().get("loc")


class AnimalsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.hybrid_command(name="possum", description="Get a random possum image. 2 times/user/day.")
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def possum(self, ctx) -> None:
        await ctx.send(get_random_animal_image("poss"))

    @commands.hybrid_command(name="randomanimal", description="Get a random animal image. 1 time/user/day.")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def random_animal(self, ctx, animal: ANIMAL_LITERAL) -> None:
        await ctx.send(get_random_animal_image(animal))

    @random_animal.error
    @possum.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Sorry, you\'re on cooldown! Try again in `{e:.1f}` seconds.'.format(e=error.retry_after),
                           ephemeral=True)


def setup(bot):
    logging.warning("Animals cog added.")
    bot.add_cog(AnimalsCog(bot))
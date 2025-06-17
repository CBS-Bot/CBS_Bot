import discord
import logging
import random
import requests
import numpy as np
from discord import Embed, File, Member
from discord.ext import commands
from typing import get_args, Tuple
from bot.resources.models.animals import ANIMAL_LITERAL, RATING_MAPPINGS, RATING_IMAGE_DIR
from bot.utils.permissionutils import is_owner_or_admin
from bot.utils.indefinitearticles import indefinite_article


def get_random_animal_image(animal: str) -> str:
    response = requests.get("https://api.tinyfox.dev/img.json", {'animal': animal})
    return "https://api.tinyfox.dev" + response.json().get("loc")

def create_animal_embed(url: str) -> tuple[Embed, File]:
    rating = get_rating()
    rating_filename = RATING_MAPPINGS[rating]["filename"]
    rating_file = discord.File(f"{RATING_IMAGE_DIR}{rating_filename}", filename="thumbnail.png")
    a_or_an = indefinite_article(rating)
    embed = discord.Embed(color=RATING_MAPPINGS[rating]["color"],
                          title=f'Congratulations!',
                          description=f'You rolled {a_or_an} **{rating}** tier animal.')
    embed.set_thumbnail(url=f"attachment://thumbnail.png")
    embed.set_image(url=url)
    return embed, rating_file


def get_rating() -> str:
    ratings = [x for x in RATING_MAPPINGS]
    weights = [RATING_MAPPINGS[x]["weight"] for x in RATING_MAPPINGS]
    random_rating = np.random.choice(ratings, 1, p=weights)
    return str(random_rating[0])


class AnimalsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.hybrid_command(name="possum", description="Get a random possum image. 1 times/user/day.")
    @commands.cooldown(1, 82800, commands.BucketType.member)
    async def possum(self, ctx) -> None:
        await ctx.send(get_random_animal_image("poss"))

    @commands.hybrid_command(name="randomanimal", description="Get a random animal image. 1 time/user/day.")
    @commands.cooldown(1, 82800, commands.BucketType.member)
    async def random_animal(self, ctx, animal: ANIMAL_LITERAL) -> None:
        await ctx.send(get_random_animal_image(animal))

    @commands.hybrid_command(name="truerandomanimal", description="Get a COMPLETELY random animal image. "
                                                                  "1 time/user/day.")
    @commands.cooldown(1, 82800, commands.BucketType.member)
    async def true_random_animal(self, ctx) -> None:
        random_animal = random.choice(get_args(ANIMAL_LITERAL))
        url = get_random_animal_image(random_animal)
        logging.warning("Animal URL: " + url)
        embed, rating_file = create_animal_embed(url)
        await ctx.send(embed=embed, file=rating_file)

    @commands.hybrid_command(name="resetanimalcooldown", description="(Owner/Admin only) Resets a user's cooldown for "
                                                                     "/truerandomanimal.")
    async def reset_true_random_animal(self, ctx, member: Member) -> None:
        if await is_owner_or_admin(ctx):
            ctx.author = member
            ctx.message.author = member
            self.true_random_animal.reset_cooldown(ctx)
            await ctx.send(f"Reset True Random Animal cooldown for member <@!{member.id}>.")

    @random_animal.error
    @possum.error
    @true_random_animal.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Sorry, you\'re on cooldown! Try again in `{e:.1f}` seconds.'.format(e=error.retry_after),
                           ephemeral=True)


def setup(bot):
    logging.warning("Animals cog added.")
    bot.add_cog(AnimalsCog(bot))

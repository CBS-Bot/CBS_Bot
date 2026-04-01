async def is_owner_or_admin(ctx) -> bool:
    return await ctx.bot.is_owner(ctx.author) or ctx.permissions.administrator

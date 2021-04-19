import logging
from discord.ext import commands
from cogs.help import Help
from const import channel_embed, log_embed, logChannel, dm_embed, baritoneDiscord


class Optout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def optout(self, ctx, *, arg=None):
        b_guild = self.bot.get_guild(baritoneDiscord)
        if arg is None:
            await Help.optout(self, ctx)
        elif arg.lower() == 'I am sure':
            channel = await self.bot.fetch_channel(logChannel)
            dchannel = await ctx.author.create_dm()
            logging.info(f'{ctx.author.id} has been banned for reason: Opted out')
            await dm_embed('Opted out', 'We appreciate you opting out. You have been banned from the server to prevent bypassing our moderation system.', dchannel)
            await channel_embed(ctx, 'User Banned', f'{ctx.author.mention} has been banned for reason: \n```User {ctx.author} has opted out```')
            await log_embed(ctx, 'User Banned', f'{ctx.author.mention} has been banned for reason: \n```User {ctx.author} has opted out```', channel)
            await b_guild.ban(user=ctx.author, reason='Opted out and banned', delete_message_days=7)
        else:
            await channel_embed(ctx, 'Opt-Out', f'You will be **banned from this server** and **lose all your roles** by continuing. Are you sure you want to opt out? if yes, type `b?optout I am sure`')


def setup(bot):
    bot.add_cog(Optout(bot))

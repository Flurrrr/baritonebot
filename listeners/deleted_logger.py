import discord
from discord.ext import commands

from main import bot_db
from utils.misc import get_channel, get_unix


class DeletedLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        log_channel = await get_channel(self.bot, bot_db.logs_id[payload.guild_id])
        if log_channel.id == payload.channel_id:
            return
        if payload.cached_message is None:
            unix_time = get_unix(payload.message_id)
            embed_var = discord.Embed(
                color=bot_db.embed_color[payload.guild_id],
                description=f'Un-cached message deleted in <#{payload.channel_id}>, it was sent on <t:{unix_time}:F>'
            )
            return await log_channel.send(embed=embed_var)
        message = payload.cached_message
        if message.author.discriminator == '0000':
            return
        if message.guild is None:
            return
        if message.channel.id in bot_db.exempted_ids[message.guild.id]:
            return

        # can't delete logged messages :)
        content = message.content if len(message.embeds) == 0 else message.embeds[0].description

        embed_var = discord.Embed(
            color=bot_db.embed_color[message.guild.id],
            description=f'**Message deleted in {message.channel.mention}**\n{content}'
        )
        embed_var.set_footer(
            text=f'{message.author.name} | ID: {message.author.id}',
            icon_url=message.author.avatar.url
        )
        await log_channel.send(embed=embed_var)


def setup(bot):
    bot.add_cog(DeletedLogger(bot))

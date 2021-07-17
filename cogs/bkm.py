import discord
import main
import re
from time import time
from cogs.help import Help
from discord.ext import commands


async def other_check(self, ctx, user):
    if user is None:
        return await Help.unmute(self, ctx)
    try:
        member, author_member = await member_check(self, ctx, user)
    except discord.NotFound:
        return await main.error_embed(ctx, 'Couldn\'t find that member')
    if member.top_role == author_member.top_role:
        await main.error_embed(ctx, f'You don\'t outrank {member.mention}')
    else:
        return True, member, author_member


async def member_check(self, ctx, user):
    return await self.bot.get_guild(main.ids(1)).fetch_member(user.id), await self.bot.get_guild(main.ids(1)).fetch_member(ctx.author.id)


async def output(member, action, channel, time_muted, ctx, reason, log_e=None):
    print(f'{ctx.author.id} {action} {member.id}{time_muted} {reason}')
    await main.log_embed(log_e, f'User {action.capitalize()}', f'{member.mention} has been {action}{time_muted} {reason}', channel, member)
    await main.channel_embed(ctx, f'User {action.capitalize()}', f'{member.mention} has been {action}{time_muted} {reason}')

time_regex = re.compile(r'^(?:(.?\d)([a-z]))+?$')
time_dict = {"h": 3600, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        mtime = 0
        for v, k in re.findall(time_regex, args):
            try:
                mtime += int((time_dict[k]*float(v)) + int(time()))
                if mtime >= (9223372036854775807 - int(time())):
                    await main.error_embed(ctx, 'That time in seconds is larger than 64 bits which isn\'t supported by postgresql, please chose a shorter time')
            except KeyError:
                await main.error_embed(ctx, 'Only use `m`(minutes), `h`(hours), or `d`(days).')
            except ValueError:
                pass
        return mtime, args


class Bkm(commands.Cog):
    def __init__(self, bot):
        """Returns embeds for all the punishment commands."""
        self.bot = bot

    @commands.command(aliases=['ub'])
    @commands.check(main.mod_group)
    async def unban(self, ctx, user: discord.User = None):
        try:
            await self.bot.get_guild(main.ids(1)).unban(user)
            await output(user, 'unbanned', await self.bot.fetch_channel(main.ids(5)), '', ctx, '', None)
        except discord.NotFound:
            await main.error_embed(ctx, 'That user is not banned')

    @commands.command(aliases=['um'])
    @commands.check(main.mod_group)
    async def unmute(self, ctx, user: discord.User = None):
        checks = await other_check(self, ctx, user)
        if checks[0] is True:
            if self.bot.get_guild(main.ids(1)).get_role(main.ids(12)) not in checks[1].roles:
                await main.error_embed(ctx, 'That member is not muted')
            else:
                await checks[1].remove_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(12)))
                try:
                    dm_channel = await checks[1].create_dm()
                    await main.dm_embed('Unmuted', 'You have been unmuted in the baritone discord', dm_channel)
                except (discord.Forbidden, discord.errors.HTTPException):
                    pass
                channel = await self.bot.fetch_channel(main.ids(5))
                await output(checks[1], 'unmuted', channel, '', ctx, '', ctx)
                main.cur.execute('DELETE FROM rekt WHERE user_id=%s', (user.id,))
                main.db.commit()

    @commands.command(aliases=['b', 'rm'])
    @commands.check(main.mod_group)
    async def ban(self, ctx, user: discord.User = None, purge=None, *, reason=None):
        checks = await other_check(self, ctx, user)
        if checks[0] is True:
            if purge is None:
                await main.error_embed(ctx, 'You need to give a reason')
            else:
                async def ban_embeds(reasons):
                    try:
                        dm_channel = await checks[1].create_dm()
                        await main.dm_embed('Banned', f'You have been banned from the baritone discord for reason: \n```{reasons}```', dm_channel)
                    except (discord.Forbidden, discord.errors.HTTPException):
                        pass
                    channel = await self.bot.fetch_channel(main.ids(5))
                    await output(checks[1], 'banned', channel, '', ctx, f'for reason: \n```{reasons}```', ctx)
                if purge.lower() == 'purge':
                    await ban_embeds(reason)
                    await checks[1].ban(reason=reason, delete_message_days=7)
                else:
                    await ban_embeds(f'{purge} {reason}')
                    await checks[1].ban(reason=reason, delete_message_days=0)

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['m'])
    @commands.check(main.helper_group)
    async def mute(self, ctx, user: discord.User = None, mtime: TimeConverter = None, *, reason=None):
        checks = await other_check(self, ctx, user)
        if checks[0] is True:
            if mtime is None:
                await main.error_embed(ctx, 'You need to give a reason or amount of time to mute')
            elif str(mtime).strip("')(").split(", '")[0] != '0' and reason is None:
                await main.error_embed(ctx, 'You need to give a reason')
            else:
                if self.bot.get_guild(main.ids(1)).get_role(main.ids(12)) in checks[1].roles:
                    await main.error_embed(ctx, 'That member is already muted')
                else:
                    time_reason = str(mtime)[1:-2].split(', ')
                    reason = '' if reason is None else reason
                    if time_reason[0] == '0':
                        reason_real, reason_time = time_reason[1][1:] + ' ' + reason, 'indefinitely'
                    else:
                        reason_real, reason_time = reason, f'for {time_reason[1][1:]}'
                    await checks[1].add_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(12)))
                    try:
                        dm_channel = await checks[1].create_dm()
                        await main.dm_embed('Muted', f'You have been muted in the baritone discord {reason_time}, reason: \n```{reason_real}```', dm_channel)
                    except (discord.Forbidden, discord.errors.HTTPException):
                        pass
                    channel = await self.bot.fetch_channel(main.ids(5))
                    await output(checks[1], 'muted', channel, f' {reason_time}', ctx, f'for reason: \n```{reason_real}```', ctx)
                    main.cur.execute('INSERT INTO rekt(user_id, action, expiry, punisher) VALUES(%s, %s, %s, %s)', (checks[1].id, 'muted', int(time_reason[0]), ctx.author.id))
                    main.db.commit()

    @mute.command(aliases=['l'])
    @commands.check(main.helper_group)
    async def list(self, ctx):
        main.cur.execute("SELECT user_id, expiry FROM rekt WHERE action='muted'")
        muted_users = main.cur.fetchall()
        desc = ''
        for row in muted_users:
            muted_user = self.bot.get_user(row[0])
            if row[1] != 0:
                try:
                    desc += f'**{muted_user.mention} ({muted_user}) Time remaining:** \n{main.time_convert(row[1] - int(time()))}\n'
                except AttributeError:
                    desc += f'**{row[0]} Time remaining:** \n{main.time_convert(row[1] - int(time()))}\n'
            else:
                try:
                    desc += f'**{muted_user.mention} ({muted_user}) Time remaining:** \nindefinite\n'
                except AttributeError:
                    desc += f'**{row[0]} Time remaining:** \n{main.time_convert(row[1] - int(time()))}\n'
        await main.channel_embed(ctx, f'Muted Users ({len(muted_users)}):', desc)

    @commands.command(aliases=['k'])
    @commands.check(main.mod_group)
    async def kick(self, ctx, user: discord.User = None, *, reason=None):
        checks = await other_check(self, ctx, user)
        if checks[0] is True:
            if reason is None:
                await main.error_embed(ctx, 'You need to give a reason')
            else:
                try:
                    dm_channel = await checks[1].create_dm()
                    await main.dm_embed('Kicked', f'You have been kicked from the baritone discord for reason: \n```{reason}```', dm_channel)
                except (discord.Forbidden, discord.errors.HTTPException):
                    pass
                channel = await self.bot.fetch_channel(main.ids(5))
                await output(checks[1], 'kicked', channel, '', ctx, f'for reason: \n```{reason}```', ctx)
                await checks[1].kick(reason=reason)

    @commands.command()
    async def optout(self, ctx, *, arg=None):
        b_guild = self.bot.get_guild(main.ids(1))
        if arg is None:
            return await Help.optout(self, ctx)
        if arg == 'I am sure':
            channel = await self.bot.fetch_channel(main.ids(5))
            try:
                dchannel = await ctx.author.create_dm()
                await main.dm_embed('Opted out', 'We appreciate you opting out. You have been banned from the server to prevent bypassing our moderation system.', dchannel)
            except (discord.Forbidden, discord.errors.HTTPException):
                pass
            print(f'{ctx.author.id} has been banned for reason: Opted out')
            await main.channel_embed(ctx, 'User Banned', f'{ctx.author.mention} has been banned for reason: \n```User {ctx.author} has opted out```')
            await main.log_embed(ctx, 'User Banned', f'{ctx.author.mention} has been banned for reason: \n```User {ctx.author} has opted out```', channel, ctx.author)
            await b_guild.ban(user=ctx.author, reason='Opted out and banned', delete_message_days=7)
        else:
            await main.channel_embed(ctx, 'Opt-Out', f'You will be **banned from this server** and **lose all your roles** by continuing. Are you sure you want to opt out? if yes, type `{main.values(0)}optout I am sure`')


def setup(bot):
    bot.add_cog(Bkm(bot))

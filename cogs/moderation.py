import discord
from discord.ext import commands
from cogs.database import Database

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        # runs when the cog is loaded, gives it access to the bot and database
        self.bot = bot
        self.db = Database()

    # --- KICK ---
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason given"):
        # kicks the member from the server
        await member.kick(reason=reason)
        await ctx.send(f'✅ {member.name} has been kicked. Reason: {reason}')

    # --- BAN ---
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason given"):
        # bans the member permanently
        await member.ban(reason=reason)
        await ctx.send(f'🔨 {member.name} has been banned. Reason: {reason}')

    # --- WARN ---
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason given"):
        # saves the warning to the database then reports the total
        self.db.add_warning(member.id, reason)
        all_warnings = self.db.get_warnings(member.id)
        count = len(all_warnings)
        await ctx.send(f'⚠️ {member.name} has been warned. Reason: {reason} (Total warnings: {count})')

    # --- WARNINGS ---
    @commands.command()
    async def warnings(self, ctx, member: discord.Member):
        # fetches all warnings from the database and lists them
        all_warnings = self.db.get_warnings(member.id)
        if not all_warnings:
            await ctx.send(f'{member.name} has no warnings.')
        else:
            warn_list = '\n'.join([f'{i+1}. {w[0]}' for i, w in enumerate(all_warnings)])
            await ctx.send(f'⚠️ Warnings for {member.name}:\n{warn_list}')

    # --- CLEAR WARNINGS ---
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def clearwarnings(self, ctx, member: discord.Member):
        # wipes all warnings for that user from the database
        self.db.clear_warnings(member.id)
        await ctx.send(f'✅ Warnings cleared for {member.name}.')

    # --- CLEAR MESSAGES ---
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        # deletes X messages plus the command message itself
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'🧹 Cleared {amount} messages.', delete_after=3)

    # --- ERROR HANDLING ---
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('❌ You don\'t have permission to use that command.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send('❌ Member not found.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('❌ Missing argument. Check your command syntax.')

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
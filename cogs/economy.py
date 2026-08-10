import discord
from discord.ext import commands
from cogs.database import Database
from datetime import datetime, timezone

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        # runs when the cog is loaded, gives it access to the bot and database
        self.bot = bot
        self.db = Database()

    # --- BALANCE ---
    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        # if no member is mentioned, check the command author's balance
        member = member or ctx.author
        balance = self.db.get_balance(member.id)
        embed = discord.Embed(
            title=f'💰 {member.name}\'s Balance',
            description=f'**{balance} coins**',
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    # --- DAILY ---
    @commands.command()
    async def daily(self, ctx):
        # gives the user 100 coins once every 24 hours
        user_id = ctx.author.id
        last_daily = self.db.get_last_daily(user_id)

        if last_daily:
            # calculates how much time has passed since last claim
            last_time = datetime.fromisoformat(last_daily)
            now = datetime.now(timezone.utc)
            diff = now - last_time
            seconds_left = 86400 - diff.total_seconds()

            if seconds_left > 0:
                # converts remaining seconds into hours and minutes
                hours = int(seconds_left // 3600)
                minutes = int((seconds_left % 3600) // 60)
                await ctx.send(f'⏰ {ctx.author.name}, you already claimed your daily! Come back in **{hours}h {minutes}m**.')
                return

        # gives coins and updates the cooldown timestamp
        self.db.update_balance(user_id, 100)
        self.db.set_last_daily(user_id)
        embed = discord.Embed(
            title='✅ Daily Claimed!',
            description=f'{ctx.author.name} received **100 coins**!',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    # --- PAY ---
    @commands.command()
    async def pay(self, ctx, member: discord.Member, amount: int):
        # transfers coins from the command author to another member
        if member == ctx.author:
            await ctx.send('❌ You cannot pay yourself.')
            return
        if amount <= 0:
            await ctx.send('❌ Amount must be greater than 0.')
            return
        sender_balance = self.db.get_balance(ctx.author.id)
        if sender_balance < amount:
            await ctx.send(f'❌ You don\'t have enough coins. Your balance: **{sender_balance} coins**.')
            return
        self.db.update_balance(ctx.author.id, -amount)
        self.db.update_balance(member.id, amount)
        embed = discord.Embed(
            title='💸 Transfer Successful',
            description=f'{ctx.author.name} sent **{amount} coins** to {member.name}.',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    # --- SHOP ---
    @commands.command()
    async def shop(self, ctx):
        # displays all items available in the shop
        items = self.db.get_shop()
        if not items:
            await ctx.send('🛒 The shop is empty.')
            return
        embed = discord.Embed(
            title='🛒 Shop',
            color=discord.Color.purple()
        )
        for item_name, price, description in items:
            embed.add_field(
                name=f'{item_name} — {price} coins',
                value=description,
                inline=False
            )
        await ctx.send(embed=embed)

    # --- BUY ---
    @commands.command()
    async def buy(self, ctx, *, item_name: str):
        # attempts to purchase an item from the shop
        result = self.db.buy_item(ctx.author.id, item_name)
        if result == 'item_not_found':
            await ctx.send(f'❌ Item **{item_name}** not found in the shop.')
        elif result == 'insufficient_funds':
            balance = self.db.get_balance(ctx.author.id)
            await ctx.send(f'❌ Not enough coins. Your balance: **{balance} coins**.')
        else:
            embed = discord.Embed(
                title='✅ Purchase Successful',
                description=f'{ctx.author.name} bought **{item_name}**!',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    # --- INVENTORY ---
    @commands.command()
    async def inventory(self, ctx, member: discord.Member = None):
        # shows all items a user owns
        member = member or ctx.author
        items = self.db.get_inventory(member.id)
        if not items:
            await ctx.send(f'🎒 {member.name} has no items.')
            return
        item_list = '\n'.join([f'• {item[0]}' for item in items])
        embed = discord.Embed(
            title=f'🎒 {member.name}\'s Inventory',
            description=item_list,
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    # --- LEADERBOARD ---
    @commands.command()
    async def leaderboard(self, ctx):
        # shows the top 10 richest users in the server
        rows = self.db.get_leaderboard()
        if not rows:
            await ctx.send('📊 No users found.')
            return
        embed = discord.Embed(
            title='🏆 Leaderboard',
            color=discord.Color.gold()
        )
        for i, (user_id, balance) in enumerate(rows):
            user = await self.bot.fetch_user(int(user_id))
            embed.add_field(
                name=f'{i+1}. {user.name}',
                value=f'{balance} coins',
                inline=False
            )
        await ctx.send(embed=embed)

    # --- ADD SHOP ITEM (admin only) ---
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def additem(self, ctx, price: int, item_name: str, *, description: str):
        # allows admins to add items to the shop
        self.db.add_shop_item(item_name, price, description)
        await ctx.send(f'✅ Added **{item_name}** to the shop for **{price} coins**.')

    # --- ERROR HANDLING ---
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('❌ You don\'t have permission to use that command.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send('❌ Member not found.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('❌ Missing argument. Check your command syntax.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('❌ Invalid argument. Make sure you\'re using the correct format.')

async def setup(bot):
    await bot.add_cog(EconomyCog(bot))
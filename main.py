l# Mira Bot - Wild West Discord Bot 
# Howdy, partner! I'm Mira, your Wild West companion. Join a gang, rob banks, trade contraband,
# and build your fortune in the frontier. With gangs like the Daltons, Wild Bunch, and Josie Gang,
# every day is a new adventure. Will you be an outlaw or keep the peace? The choice is yours!

# Trigger rebuild
import discord
from discord.ext import commands
from discord import app_commands
import os
import random
import asyncio
from datetime import timedelta
import sqlite3

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

def init_db():
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, money INTEGER DEFAULT 100,
                  gang TEXT, role TEXT, bounty INTEGER DEFAULT 0, arrests INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS drugs
                 (user_id INTEGER, drug_type TEXT, quantity INTEGER,
                  PRIMARY KEY (user_id, drug_type))''')
    c.execute('''CREATE TABLE IF NOT EXISTS properties
                                  (user_id INTEGER,  property_type TEXT, property_name TEXT,
                  PRIMARY KEY (user_id, property_type))''')
    c.execute('''CREATE TABLE IF NOT EXISTS horses
                 (user_id INTEGER PRIMARY KEY, horse_type TEXT, horse_name TEXT)''')
    conn.commit()
    conn.close()

init_db()

GANGS = {
    "daltons": {"name": "Daltons Gang", "color": 0xFF0000, "emoji": "🔴"},
    "wildbunch": {"name": "Wild Bunch", "color": 0x00FF00, "emoji": "🟢"},
    "josie": {"name": "Josie Gang", "color": 0x0000FF, "emoji": "🔵"},
    "officers": {"name": "Law Officers", "color": 0xFFD700, "emoji": "⭐"},
    "bankers": {"name": "Town Bankers", "color": 0x964B00, "emoji": "💰"}
}

ROLES = ["Leader", "Planner", "Muscle", "Robber", "Horse Manager", "Town Drunk", "Weapons Master", "Medic"]

DRUGS = {
    "opium": {"name": "Opium", "base_price": 50},
    "whiskey": {"name": "Whiskey", "base_price": 30},
    "tobacco": {"name": "Tobacco", "base_price": 20}
}

# Wild West Houses - Period-accurate frontier dwellings
HOUSES = {
    "tent": {"name": "Canvas Tent", "price": 100, "emoji": "⛺", "description": "Basic shelter from the elements"},
    "cabin": {"name": "Wooden Cabin", "price": 500, "emoji": "🏚️", "description": "Small pioneer homestead"},
    "ranch": {"name": "Ranch House", "price": 1500, "emoji": "🏡", "description": "Sturdy frontier ranch"},
    "saloon": {"name": "Saloon", "price": 3000, "emoji": "🍺", "description": "Profitable business establishment"},
    "manor": {"name": "Victorian Manor", "price": 7500, "emoji": "🏰", "description": "Luxurious estate for wealthy frontier folk"}
}

# Wild West Horses - Period-accurate breeds
HORSES = {
    "mare": {"name": "Old Mare", "price": 150, "emoji": "🐴", "speed": 1, "description": "Slow but dependable work horse"},
    "mustang": {"name": "Wild Mustang", "price": 400, "emoji": "🏇", "speed": 3, "description": "Fast and untamed"},
    "thoroughbred": {"name": "Thoroughbred", "price": 800, "emoji": "🐎", "speed": 4, "description": "Racing champion"},
    "warhorse": {"name": "War Horse", "price": 1200, "emoji": "⚔️", "speed": 3, "description": "Battle-tested and strong"},
    "arabian": {"name": "Arabian", "price": 2500, "emoji": "✨", "speed": 5, "description": "Elite speed and endurance"}
}

HEIST_QUESTIONS = [
    {"q": "What year did Wild West begin?", "a": ["1865", "1860"], "hints": ["After Civil War"]},
    {"q": "Famous outlaw?", "a": ["jesse james", "billy the kid", "butch cassidy"], "hints": ["Gang leader"]},
    {"q": "Cowboy weapon?", "a": ["revolver", "colt", "six shooter"], "hints": ["Handheld gun"]},
    {"q": "What did cowboys ride?", "a": ["horse"], "hints": ["Four legs"]},
    {"q": "Wild West town?", "a": ["tombstone", "dodge city", "deadwood"], "hints": ["Gunfights"]}
]

def get_user(user_id):
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    if not user:
        c.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        user = c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    return user

def update_money(user_id, amount):
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    c.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

@bot.event
async def on_ready():
    print("\n" + "="*60)
    print("🤠 MIRA BOT - WILD WEST DISCORD BOT".center(60))
    print("="*60)
    print(f"\nBot User: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Servers: {len(bot.guilds)}")
    print("\n" + "-"*60)
    print("AVAILABLE COMMANDS:".center(60))
    print("-"*60)
    print("\n📋 Basic Commands:")
    print("  !mira - Introduction to Mira")
    print("  !help - Complete command guide")
    print("  !balance or !bal - Check cash and stats")
    print("\n🎯 Gang Commands:")
    print("  !joinggang [gang] - Join a gang")
    print("    Available: daltons, wildbunch, josie, officers, bankers")
    print("  !assignrole [@member] [role] - Assign roles (Leader only)")
    print("\n💰 Economy Commands:")
    print("  !work - Earn money from jobs")
    print("  !makedrug [type] [amount] - Craft drugs")
    print("  !selldrug [type] [amount] - Sell your drugs")
    print("    Types: opium, whiskey, tobacco")
    print("\n🏦 Action Commands:")
    print("  !heist - Start a bank heist (requires gang)")
    print("  !rob [@member] - Attempt to rob another player")
    print("  !duel [@member] [amount] - Challenge to a duel")
    print("\n🏠 Property Commands:")
    print("  !buyhouse [type] - Purchase frontier property")
    print("  !buyhorse [type] - Buy a Wild West horse")
    print("  !property - View your properties and horses")
print("  Houses: tent, cabin, ranch, saloon, manor")
print(" Horses: mare, mustang, thoroughbred, warhorse, arabian")
print("  !arrest [@member] - Arrest outlaws (Officers only)")
print("\n💎 Admin Commands (Owner Only):")
print("  !addmoney [@member] [amount] - Add money to a user")
print(" !addmoney [amount] - Add money to yourself")
print("\n" + "="*60)
        
    # Sync slash commands
        await bot.tree.sync()
    print("🔄 Slash commands synced!")
    print("✅ BOT IS ONLINE AND READY!".center(60))
    print("="*60 + "\n")
.hybrid_command(name='mira')
async def mira_intro(ctx):
    embed = discord.Embed(title="🤠 Howdy! I'm Mira!", 
        description="Short gal with curly brown hair running the Wild West!\n\n"
                    @bot@bot"**Commands:** !balance, !joinggang, !work, !makedrug, !selldrug, !heist, !rob, !duel, !arrest",
        color=0xD4AF37)
    await ctx.send(embed=embed)

@bot.hybrid_command(name='balance', aliases=['bal'])
async def balance(ctx, member: discord.Member = None):
    member = member or ctx.author
    user = get_user(member.id)
    embed = discord.Embed(title=f"💰 {member.display_name}", 
        description=f"Cash: ${user[1]}\nGang: {user[2] or 'None'}\nRole: {user[3] or 'None'}\nBounty: ${user[4]}", 
        color=0xFFD700)
    await ctx.send(embed=embed)

@bot.hybrid_command(name='joinggang')
async def join_gang(ctx, gang_name: str):
    gang_name = gang_name.lower()
    if gang_name not in GANGS:
        await ctx.send(f"❌ Invalid! Choose: {', '.join(GANGS.keys())}")
        return
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    c.execute("UPDATE users SET gang = ? WHERE user_id = ?", (gang_name, ctx.author.id))
    conn.commit()
    conn.close()
    await ctx.send(f"{GANGS[gang_name]['emoji']} Joined **{GANGS[gang_name]['name']}**!")

@bot.hybrid_command(name='work')
async def work(ctx):
    jobs = [("mined gold", random.randint(20, 50)), ("herded cattle", random.randint(15, 40))]
    job, pay = random.choice(jobs)
    update_money(ctx.author.id, pay)
    await ctx.send(f"💼 {job} → **${pay}**")

@bot.hybrid_command(name='makedrug')
async def make_drug(ctx, drug_type: str, amount: int = 1):
    drug_type = drug_type.lower()
    if drug_type not in DRUGS:
        await ctx.send(f"❌ Choose: {', '.join(DRUGS.keys())}")
        return
    cost = int(DRUGS[drug_type]['base_price'] * amount * 0.5)
    user = get_user(ctx.author.id)
    if user[1] < cost:
        await ctx.send(f"❌ Need ${cost}!")
        return
    update_money(ctx.author.id, -cost)
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    c.execute("INSERT INTO drugs VALUES (?, ?, ?) ON CONFLICT(user_id, drug_type) DO UPDATE SET quantity = quantity + ?",
              (ctx.author.id, drug_type, amount, amount))
    conn.commit()
    conn.close()
    await ctx.send(f"🧪 Made {amount} {DRUGS[drug_type]['name']}!")

@bot.hybrid_command(name='selldrug')
async def sell_drug(ctx, drug_type: str, amount: int = 1):
    drug_type = drug_type.lower()
    if drug_type not in DRUGS:
        return
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    result = c.execute("SELECT quantity FROM drugs WHERE user_id=? AND drug_type=?", (ctx.author.id, drug_type)).fetchone()
    if not result or result[0] < amount:
        await ctx.send("❌ Don't have enough!")
        conn.close()
        return
    price = int(DRUGS[drug_type]['base_price'] * amount * random.uniform(0.8, 1.5))
    c.execute("UPDATE drugs SET quantity = quantity - ? WHERE user_id=? AND drug_type=?", (amount, ctx.author.id, drug_type))
    conn.commit()
    conn.close()
    update_money(ctx.author.id, price)
    await ctx.send(f"💰 Sold for **${price}**!")

@bot.hybrid_command(name='heist')
@commands.cooldown(1, 300, commands.BucketType.guild)
async def heist(ctx):
    user = get_user(ctx.author.id)
    if not user[2]:
        await ctx.send("❌ Need gang!")
        return
    embed = discord.Embed(title="🏦 HEIST!", description=f"{ctx.author.display_name} planning heist!\nReact ✅ (30s)", color=0xFF0000)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")
    await asyncio.sleep(30)
    msg = await ctx.channel.fetch_message(msg.id)
    participants = [ctx.author]
    for reaction in msg.reactions:
        if str(reaction.emoji) == "✅":
            async for user in reaction.users():
                if not user.bot and user != ctx.author:
                    participants.append(user)
    questions = random.sample(HEIST_QUESTIONS, 3)
    correct = 0
    for i, q in enumerate(questions, 1):
        await ctx.send(f"**Q{i}:** {q['q']}")
        def check(m):
            return m.author in participants and m.channel == ctx.channel
        try:
            answer = await bot.wait_for('message', timeout=20.0, check=check)
            if any(a in answer.content.lower() for a in q['a']):
                correct += 1
                await ctx.send("✅")
            else:
                await ctx.send(f"❌ Hint: {q['hints'][0]}")
        except asyncio.TimeoutError:
            await ctx.send("⏰")
    if correct >= 2:
        reward = random.randint(500, 1500) // len(participants)
        for p in participants:
            update_money(p.id, reward)
        await ctx.send(f"🎉 SUCCESS! +${reward} each!")
    else:
        await ctx.send(f"❌ FAILED! {correct}/3")

@bot.hybrid_command(name='rob')
async def rob(ctx, member: discord.Member):
    if member.bot or member == ctx.author:
        return
    target = get_user(member.id)
    if target[1] < 50:
        await ctx.send("❌ Too broke!")
        return
    if random.random() < 0.5:
        stolen = int(target[1] * random.uniform(0.1, 0.3))
        update_money(ctx.author.id, stolen)
        update_money(member.id, -stolen)
        await ctx.send(f"💰 Stole ${stolen}!")
    else:
        await ctx.send("❌ Failed!")

@bot.hybrid_command(name='duel')
async def duel(ctx, member: discord.Member, amount: int):
    if member.bot or member == ctx.author:
        return
    user = get_user(ctx.author.id)
    target = get_user(member.id)
    if user[1] < amount or target[1] < amount:
        await ctx.send("❌ Can't afford!")
        return
    await ctx.send(f"🔫 {member.mention} accept ${amount} duel? (yes/no)")
    def check(m):
        return m.author == member and m.channel == ctx.channel
    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        if msg.content.lower() != 'yes':
            await ctx.send("❌ Declined!")
            return
    except asyncio.TimeoutError:
        return
    winner = random.choice([ctx.author, member])
    loser = member if winner == ctx.author else ctx.author
    update_money(winner.id, amount)
    update_money(loser.id, -amount)
    await ctx.send(f"🎯 {winner.mention} won ${amount}!")

@bot.hybrid_command(name='arrest')
@commands.has_permissions(moderate_members=True)
async def arrest(ctx, member: discord.Member):
    user = get_user(ctx.author.id)
    if user[2] != 'officers':
        await ctx.send("❌ Officers only!")
        return
    timeout_mins = random.randint(5, 20)
    try:
        await member.timeout(timedelta(minutes=timeout_mins), reason="Arrested")
        await ctx.send(f"👮 Arrested {member.mention} for **{timeout_mins} mins**!")
    except:
        await ctx.send("❌ Can't arrest!")

@bot.hybrid_command(name='assignrole')
async def assign_role(ctx, member: discord.Member, role: str):
    user = get_user(ctx.author.id)
    if user[3] != 'Leader':
        await ctx.send("❌ Leaders only!")
        return
    if role not in ROLES:
        await ctx.send(f"❌ Choose: {', '.join(ROLES)}")
        return
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    c.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, member.id))
    conn.commit()
    conn.close()
    await ctx.send(f"✅ {member.mention} → **{role}**!")

@bot.hybrid_command()
async def help(ctx):
    """Display all available commands and bot information"""
    embed = discord.Embed(
        title="🤠 Howdy, Partner! - Mira's Command Guide",
        description="Howdy, partner! I'm Mira, your Wild West companion. Join a gang, rob banks, trade contraband, and build your fortune in the frontier!",
        color=0xD4AF37
    )
    
    # About Me section
    embed.add_field(
        name="📖 About Me",
        value="I'm Mira, a short gal with brown curly hair and blue eyes, here to guide you through the Wild West. Whether you're an outlaw or lawkeeper, I've got your back!",
        inline=False
    )
    
    # Gang Commands
    embed.add_field(
        name="🎯 Gang Commands",
        value=(
            "**!joingang [gang]** - Join one of the frontier gangs\n"
            "Available: `daltons`, `wildbunch`, `josie`, `officers`, `bankers`\n\n"
            "**!leavegang** - Leave your current gang\n"
            "**!ganginfo** - See your gang's details"
        ),
        inline=False
    )
    
    # Role Commands
    embed.add_field(
        name="🎭 Role System",
        value=(
            "**!assignrole [@member] [role]** - Assign roles (Leader only)\n"
            "Roles: `Leader`, `Planner`, `Muscle`, `Robber`, `Horse Manager`, `Town Drunk`, `Weapons Master`, `Medic`"
        ),
        inline=False
    )
    
    # Economy Commands
    embed.add_field(
        name="💰 Economy & Trading",
        value=(
            "**!balance** - Check your cash stash\n"
            "**!buy [drug] [amount]** - Purchase goods\n"
            "**!sell [drug] [amount]** - Sell your goods\n"
            "**!make [drug] [amount]** - Craft goods\n"
            "**!inventory** - Check your supplies\n"
            "Available goods: `opium`, `whiskey`, `tobacco`"
        ),
        inline=False
    )
    
    # Action Commands
    embed.add_field(
        name="🏦 Actions & Heists",
        value=(
            "**!heist** - Rob the bank (risky business!)\n"
            "**!arrest [@member]** - Arrest outlaws (Officers only)\n"
            "**!profile** - View your outlaw profile"
        ),
        inline=False
    )
    
    embed.set_footer(text="Every day is a new adventure. Will you be an outlaw or keep the peace? The choice is yours!")
    await ctx.send(embed=embed)



# Admin command - Only for owner (Your ID: 747474910850318437)
@bot.hybrid_command(name='buyhouse')
async def buy_house(ctx, house_type: str):
    house_type = house_type.lower()
    if house_type not in HOUSES:
        await ctx.send(f"❌ Invalid! Choose: {', '.join(HOUSES.keys())}")
        return
    
    house = HOUSES[house_type]
    user = get_user(ctx.author.id)
    
    if user[1] < house['price']:
        await ctx.send(f"❌ Need ${house['price']}! You have ${user[1]}")
        return
    
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    existing = c.execute("SELECT * FROM properties WHERE user_id=? AND property_type=?", 
                         (ctx.author.id, house_type)).fetchone()
    
    if existing:
        await ctx.send(f"❌ You already own a {house['name']}!")
        conn.close()
        return
    
    update_money(ctx.author.id, -house['price'])
    c.execute("INSERT INTO properties VALUES (?, ?, ?)", 
              (ctx.author.id, house_type, house['name']))
    conn.commit()
    conn.close()
    
    await ctx.send(f"{house['emoji']} Purchased **{house['name']}** for ${house['price']}!\n{house['description']}")

@bot.hybrid_command(name='buyhorse')
async def buy_horse(ctx, horse_type: str):
    horse_type = horse_type.lower()
    if horse_type not in HORSES:
        await ctx.send(f"❌ Invalid! Choose: {', '.join(HORSES.keys())}")
        return
    
    horse = HORSES[horse_type]
    user = get_user(ctx.author.id)
    
    if user[1] < horse['price']:
        await ctx.send(f"❌ Need ${horse['price']}! You have ${user[1]}")
        return
    
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    existing = c.execute("SELECT * FROM horses WHERE user_id=?", (ctx.author.id,)).fetchone()
    
    if existing:
        await ctx.send(f"❌ You already own a horse! Sell it first with !sellhorse")
        conn.close()
        return
    
    update_money(ctx.author.id, -horse['price'])
    c.execute("INSERT INTO horses VALUES (?, ?, ?)", 
              (ctx.author.id, horse_type, horse['name']))
    conn.commit()
    conn.close()
    
    await ctx.send(f"{horse['emoji']} Purchased **{horse['name']}** for ${horse['price']}!\nSpeed: {'⭐' * horse['speed']}\n{horse['description']}")

@bot.hybrid_command(name='property')
async def view_property(ctx, member: discord.Member = None):
    member = member or ctx.author
    
    conn = sqlite3.connect('mira_bot.db')
    c = conn.cursor()
    
    # Get houses
    houses = c.execute("SELECT property_type, property_name FROM properties WHERE user_id=?", 
                       (member.id,)).fetchall()
    
    # Get horse
    horse = c.execute("SELECT horse_type, horse_name FROM horses WHERE user_id=?", 
                      (member.id,)).fetchone()
    conn.close()
    
    embed = discord.Embed(title=f"🏘️ {member.display_name}'s Property", color=0x8B4513)
    
    if houses:
        house_list = "\n".join([f"{HOUSES[h[0]]['emoji']} **{h[1]}** ({HOUSES[h[0]]['description']})" 
                                for h in houses])
        embed.add_field(name="🏠 Houses", value=house_list, inline=False)
    else:
        embed.add_field(name="🏠 Houses", value="No properties owned", inline=False)
    
    if horse:
        horse_data = HORSES[horse[0]]
        embed.add_field(name="🐴 Horse", 
                       value=f"{horse_data['emoji']} **{horse[1]}**\nSpeed: {'⭐' * horse_data['speed']}\n{horse_data['description']}", 
                       inline=False)
    else:
        embed.add_field(name="🐴 Horse", value="No horse owned", inline=False)
    
    await ctx.send(embed=embed)
# Admin command - Only for owner (Your ID: 747474910850318437)
@bot.hybrid_command(name='addmoney')
async def add_money_admin(ctx, member: discord.Member = None, amount: int = None):
    """Admin only command to add money to users"""
   
    # Check if user is the bot owner
    if ctx.author.id != 747474910850318437:
        await ctx.send("❌ You don't have permission to use this command!")
        return
    
    # If no member specified, add to self
    if member is None:
        if amount is None:
            await ctx.send("❌ Usage: !addmoney [amount] or !addmoney [@member] [amount]")
            return
        update_money(ctx.author.id, amount)
        await ctx.send(f"💰 Added **${amount}** to your account!")
    else:
        if amount is None:
            await ctx.send("❌ Please specify an amount: !addmoney [@member] [amount]")
            return
        update_money(member.id, amount)
        await ctx.send(f"💰 Added **${amount}** to {member.mention}'s account!")

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print('Error: DISCORD_TOKEN not found!')
    else:
        bot.run(TOKEN)

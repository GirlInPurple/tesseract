from config import *

import math, random, os, sys, asyncio, json, requests

import nextcord, logging, youtube_dl
from nextcord.ext import commands
from nextcord import ui

from libretranslatepy import LibreTranslateAPI

# settup

logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

lt = LibreTranslateAPI("https://translate.argosopentech.com/")

# constants:

orX, orZ, orY = 0, 0, 64 #might change to 0,0,0 later on, but this makes more sense as this spot is likely on the surface and thus better distances can be made.
plus = "+" # dont question it, used in /point and the man function

# global Functions:

def pyth(x1, z1, x2, z2): # A modified Pythagorean Equation; sqrt((x2-x1)^2)+(z2-z1)^2)) = d
    return math.sqrt(pow((x2-x1),2)+pow((z2-z1),2))

def pyth3D(x1, z1, y1, x2, z2, y2): # The same as the function above, but 3D
    return math.sqrt(pow((x2-x1),2)+pow((z2-z1),2)+pow((y2-y1),2))

def hypot(x1, z1, x2, z2): #The original Pythagorean Theorem; sqrt(x^2 + z^2) = d
	return math.sqrt(pow(int(man(x1, z1, x2, z2, "x")), 2) + pow(int(man(x1, z1, x2, z2, "z")), 2))  

def man(x1, z1, x2, z2, out):
	x = abs(abs(x1) - abs(x2))
	z = abs(abs(z1) - abs(z2))
    # do not remove this if statement tree, it will break the hypot function and hence the point command
	if out == "x":
		return x
	elif out == "z":
		return z
	elif out == "+":
		return x + z

# bot settup:

intents = nextcord.Intents.default() 
intents.message_content = True 
bot = commands.Bot(command_prefix="$", intents=intents)


# bot scripts:
class DropdownMain(nextcord.ui.Select):
    def __init__(self):
        global select
        select = [
            nextcord.SelectOption(label="Minecraft"),
            nextcord.SelectOption(label="Apoc"),
            nextcord.SelectOption(label="Terraria")
        ]
        super().__init__(placeholder="Select Game", min_values=1, max_values=1, options=select)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Minecraft":
            view = DropdownViewMC()
        elif self.values[0] == "Terraria":
            view = DropdownViewTR()
        await interaction.response.send_message(f'You choose {self.values[0]}. Pick a Ref.', view=view)

class DropdownMC(nextcord.ui.Select):
    def __init__(self):
        selectRefMC = [
            nextcord.SelectOption(label="Biomes", description=""),
            nextcord.SelectOption(label="Enchant Order", description="The optimal enchanting order for maxxed books and tools"),
            nextcord.SelectOption(label="Fishing", description="pre-1.16 AFK fishing nerf in any biome but jungle"),
            nextcord.SelectOption(label="Ore Gen", description=""),
            nextcord.SelectOption(label="Potions", description=""),
            nextcord.SelectOption(label="Trades", description="")
        ]
        super().__init__(placeholder="Select Game", min_values=1, max_values=1, options=selectRefMC)
        
    async def callback(self, interaction: nextcord.Interaction):
        
        MCembed = nextcord.Embed(title="Minecraft Refrence", colour=0xff00ff)
        
        if self.values[0] == "Biomes":
            MCembed.add_field(name="Biome Generation", value="*may be outdated for the newest versions of the game, 1.18 changed worldgen enough that*")
            MCembed.set_image(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/73/BiomesGraph.png/revision/latest/scale-to-width-down/250?cb=20200409011906")
        elif self.values[0] == "Enchant Order":
            MCembed.add_field(name="Best Enchant Order", value="*Sweeping Edge doesn't exist on Bedrock Edition, skip that if you play on Bedrock.*\n*This chart may be out of date for 1.18+, take it with a grain of salt.*")
            MCembed.set_image(url="https://preview.redd.it/20c9aerp0we71.png?width=640&crop=smart&auto=webp&s=17858ff0992fc89efb4199d518024681e6cfa8f5")
        elif self.values[0] == "Fishing":
            MCembed.add_field(name="Non-Jungle Enchanting Loot", value="*This is only for valid fishing spots; 200 blocks of water, no blocks (except transparent) can be above the water, and 1 fish has to be nearby.*")
            MCembed.set_image(url="https://cdn.discordapp.com/attachments/835308950395027476/974656713145856010/52b35-16078214820732-800.jpg")
        elif self.values[0] == "Ore Gen":
            MCembed.add_field(name="New Ore Gen", value="*+1.18 only, a -1.17 graph is included as refrence.*")
            MCembed.set_image(url="https://cdn.discordapp.com/attachments/835308950395027476/974656713552707654/5uQl6HiVuZn9oL0GybvvwMCci0QRtzFmClkCKDER2BQ.jpg")
        elif self.values[0] == "Potions":
            MCembed.add_field(name="Potion Recipes", value="*1.13 added 2 new potions, Turtle Master and Slowfalling, they are included*")
            MCembed.set_image(url="https://cdn.discordapp.com/attachments/835308950395027476/974656713825325106/Minecraft_brewing_en.png")
        elif self.values[0] == "Trades":
            MCembed.add_field(name="Trades/Shops", value="*+1.14 Villager Trades*")
            MCembed.set_image(url="https://cdn.discordapp.com/attachments/835308950395027476/974656714332856382/g0ZoRtC.png")
        await interaction.response.send_message(embed=MCembed)
        
class DropdownTR(nextcord.ui.Select):
    def __init__(self):
        selectRefTR = [
            nextcord.SelectOption(label="nonfunc1"),
            nextcord.SelectOption(label="nonfunc2"),
            nextcord.SelectOption(label="nonfunc3"),
            nextcord.SelectOption(label="nonfunc4")
        ]
        super().__init__(placeholder="Select Game", min_values=1, max_values=1, options=selectRefTR)
    
    async def callback(self, interaction: nextcord.Interaction):
        
        TRembed = nextcord.Embed(title="Terraria Refrence", colour=0xccffcc)
        
        if self.values[0] == "":
            TRembed.add_field(name="Biome Generation", value="*may be outdated for the newest versions of the game, 1.18 changed worldgen enough that*")
            TRembed.set_image(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/73/BiomesGraph.png/revision/latest/scale-to-width-down/250?cb=20200409011906")
        elif self.values[0] == "":
            TRembed.add_field(name="Biome Generation", value="*may be outdated for the newest versions of the game, 1.18 changed worldgen enough that*")
            TRembed.set_image(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/73/BiomesGraph.png/revision/latest/scale-to-width-down/250?cb=20200409011906")
        
        await interaction.response.send_message(embed=TRembed)
        
class DropdownViewMain(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownMain())
        
class DropdownViewMC(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownMC())

class DropdownViewTR(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownTR())

# setup end here
# bot starts here

class Main(commands.Bot):
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name='you.'))
        print(f"Ready!")

    @bot.slash_command(description='A command for testing, replies with "Pong!" and the ping in ms')
    async def ping(inter):
        await inter.send(f"Pong! {bot.latency * 1000:.2f}ms")

    @bot.slash_command(description='Automatically roll a di(c)e of your choice, must be in NdN format, defaults to 4d6.')
    async def roll(inter, dice: str = "4d6"):
        rolls, limit = map(int, dice.split("d"))

        result = ", ".join(str(random.randint(1, limit)) for _ in range(rolls))
        await inter.send(result)

    @bot.slash_command(description="A general purpose command for coordinates") #this one command took ***4 FREAKING DAYS*** to get right, and still breaks half the time it's used, dont touch it you will deal with hell.
    async def point(interaction, x1: int, z1: int, y1: int, name1: str, x2: int, z2: int, y2: int, name2: str, mode: str = nextcord.SlashOption(name='mode', choices={"Single", "Duo"})):

        await interaction.response.defer()
        print(f"{x1, z1, y1, x2, z2, y2, name1, name2, mode}")
        
        pointEmbed = nextcord.Embed(title="Point Command", colour=0xff00ff)
        
        pointEmbed.add_field(name="Point "+name2, value=f"\n\nLocation:\nX cord: {x2};\nY cord: {y2};\nZ cord: {z2};\n\nDistance to Origin:\nManhattan: {man(x2, z2, orX, orZ, plus)}\nBeeline (True Pythagorean): {hypot(x2, z2, orX, orZ)}\nModified Pythagorean: {pyth(x2, z2, orX, orZ)}\nModified Pythagorean (3D): {pyth3D(x2, z2, y2, orX, orZ, orY)}\n\nNether Portal:\nIf Cords are in Overworld, build at these cords in Nether: {x2/8, z2/8}\nIf Cords are in Nether, build at these cords in Overworld: {x2*8, z2*8}", inline=False)
        
        if mode == "Duo":
            
            spawner = ""
            if pyth3D(x1, z1, y1, x2, z2, y2) < 32: 
                spawner = "Yes!\nX: " + str((x1+x2)/2) + "\nZ: " + str((z1+z2)/2) + "\nY: " + str((y1+y2)/2)
            else: 
                spawner = "No, too far away"
                
            pointEmbed.add_field(name="Both Points", value=f"\n*Distance between points {name1} and {name2}:*\n*Total Distance:*\nManhattan: {man(x1,z1,x2,z2,plus)}\nBeeline (True Pythagorean): {hypot(x1,z1,x2,z2)}\nModified Pythagorean: {pyth(x1, z1, x2, z2)}\nModified Pythagorean (3D): {pyth3D(x1, z1, y1, x2, z2, y2)}\n\nDistance / 8 (to account for Nether travel):\nManhattan: {man(x1,z1,x2,z2,plus)/8}\nBeeline (True Pythagorean): {hypot(x1,z1,x2,z2)/8}\nModified Pythagorean: {pyth(x1, z1, x2, z2)/8}\nModified Pythagorean (3D): {pyth3D(x1, z1, y1, x2, z2, y2)/8}\n\n*Misc:*\nCan be used as a spawner farm? {spawner}\nHalfway Point (2D): {(x1+x2)/2, (z1+z2)/2}\nHalfway Point (3D): {(x1+x2)/2, (z1+z2)/2, (y1+y2)/2}\n\n***Notes:***\n1. Origin is set to 0,64,0, but can be changed if you prefer 0,0,0\n2. Negative numbers are not guaranteed to work 100% of the time, and due to all of the abs() calls adding the negative symbol is pretty redundant.\n3. all cordinates are in XZY format, ***not*** XYZ.")
        
        await interaction.followup.send(embed=pointEmbed)

    @bot.slash_command(description='A command that contains many refrence images, like trades, ore-gen, maps, and fishing loot')
    async def ref(inter):
        view = DropdownViewMain()
        await inter.send("Choose Game", view=view)

    @bot.slash_command(description='A general help command')
    async def help(inter):
    
        helpEmbed = nextcord.Embed(title='Tesseract Help/About', colour=0xffffff)
        helpEmbed.add_field(name='Main Contributers', value='***<@624191654282395648>:*** Helping with the bot a little\n***<@625855485773611018>:*** Asked for Apoc1 support for his private server, I obliged')
        helpEmbed.add_field(name='Commands', value='`/help`: This embed you\'re looking at now with everything you will ever need\n`/point`: A complex command for dealing with shapes, lines, and other geometry, very useful for complex farms in Minecraft as they have to just the right distance away depending on the farm.\n`/ref`: The remade refrence commmand, it displays refrences from 3 different games, Apoc, Minecraft, and Terraria/Calamity.')
        await inter.response.send_message(embed=helpEmbed)
        
    @bot.slash_command(description='Translates inputed text into another language. Not English > English, English > French.')
    async def translate(inter, inputtext:str, inlang:str = "en", outlang:str = "fr"):
        
        TranslateEmbed = nextcord.Embed(title=f'Translating from {inlang} into {outlang}', colour=0xffffff)
        TranslateEmbed.add_field(name='Input', value=inputtext)
        TranslateEmbed.add_field(name='Output', value=lt.translate(inputtext, inlang, outlang))
        
        await inter.response.send_message(embed=TranslateEmbed)

if __name__ == "__main__":
    print(f"attempting to start bot, please be patient.")
    bot.run(token)
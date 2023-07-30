import discord
import random
import os
import math
import requests

bot = discord.Bot()


def LocalFiles():
    return os.path.dirname(os.path.realpath(__file__))


def APIRequest(url: str, params: dict):
    resp = requests.get(url=url, params=params)
    data = resp.json()


class DropdownMC(discord.ui.Select):
    def __init__(self):
        selectRefMC = [
            discord.SelectOption(label="Biomes", description=""),
            discord.SelectOption(
                label="Enchant Order", description="The optimal enchanting order for maxxed books and tools"),
            discord.SelectOption(
                label="Fishing", description="pre-1.16 AFK fishing nerf in any biome but jungle"),
            discord.SelectOption(label="Ore Gen", description=""),
            discord.SelectOption(label="Potions", description=""),
            discord.SelectOption(label="Trades", description="")
        ]
        super().__init__(placeholder="Select Game",
                         min_values=1, max_values=1, options=selectRefMC)

    async def callback(self, interaction: discord.Interaction):

        MCembed = discord.Embed(title="Minecraft Refrence", colour=0xff00ff)

        if self.values[0] == "Biomes":
            MCembed.add_field(
                name="Biome Generation", value="*may be outdated for the newest versions of the game, 1.18 changed worldgen enough that*")
            MCembed.set_image(
                url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/73/BiomesGraph.png/revision/latest/scale-to-width-down/250?cb=20200409011906")
        elif self.values[0] == "Enchant Order":
            MCembed.add_field(name="Best Enchant Order",
                              value="*Sweeping Edge doesn't exist on Bedrock Edition, skip that if you play on Bedrock.*\n*This chart may be out of date for 1.18+, take it with a grain of salt.*")
            MCembed.set_image(
                url="https://preview.redd.it/20c9aerp0we71.png?width=640&crop=smart&auto=webp&s=17858ff0992fc89efb4199d518024681e6cfa8f5")
        elif self.values[0] == "Fishing":
            MCembed.add_field(name="Non-Jungle Enchanting Loot",
                              value="*This is only for valid fishing spots; 200 blocks of water, no blocks (except transparent) can be above the water, and 1 fish has to be nearby.*")
            MCembed.set_image(
                url="https://cdn.discordapp.com/attachments/835308950395027476/974656713145856010/52b35-16078214820732-800.jpg")
        elif self.values[0] == "Ore Gen":
            MCembed.add_field(
                name="New Ore Gen", value="*+1.18 only, a -1.17 graph is included as refrence.*")
            MCembed.set_image(
                url="https://cdn.discordapp.com/attachments/835308950395027476/974656713552707654/5uQl6HiVuZn9oL0GybvvwMCci0QRtzFmClkCKDER2BQ.jpg")
        elif self.values[0] == "Potions":
            MCembed.add_field(
                name="Potion Recipes", value="*1.13 added 2 new potions, Turtle Master and Slowfalling, they are included*")
            MCembed.set_image(
                url="https://cdn.discordapp.com/attachments/835308950395027476/974656713825325106/Minecraft_brewing_en.png")
        elif self.values[0] == "Trades":
            MCembed.add_field(name="Trades/Shops",
                              value="*+1.14 Villager Trades*")
            MCembed.set_image(
                url="https://cdn.discordapp.com/attachments/835308950395027476/974656714332856382/g0ZoRtC.png")
        await interaction.response.send_message(embed=MCembed)


class DropdownFR(discord.ui.Select):
    def __init__(self):
        selectRefTR = [
            discord.SelectOption(label="nonfunc1"),
            discord.SelectOption(label="nonfunc2"),
            discord.SelectOption(label="nonfunc3"),
            discord.SelectOption(label="nonfunc4")
        ]
        super().__init__(placeholder="Select Game",
                         min_values=1, max_values=1, options=selectRefTR)

    async def callback(self, interaction: discord.Interaction):

        TRembed = discord.Embed(title="Terraria Refrence", colour=0xccffcc)

        if self.values[0] == "":
            TRembed.add_field(
                name="Biome Generation", value="*may be outdated for the newest versions of the game, 1.18 changed worldgen enough that*")
            TRembed.set_image(
                url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/73/BiomesGraph.png/revision/latest/scale-to-width-down/250?cb=20200409011906")
        elif self.values[0] == "":
            TRembed.add_field(
                name="Biome Generation", value="*may be outdated for the newest versions of the game, 1.18 changed worldgen enough that*")
            TRembed.set_image(
                url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/73/BiomesGraph.png/revision/latest/scale-to-width-down/250?cb=20200409011906")


class DropdownViewMain(discord.ui.View):
    def __init__(self, *, timeout):
        super().__init__(timeout=timeout)
        self.add_item(DropdownMain())


class DropdownViewMC(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownMC())


class DropdownViewFR(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownFR())


class DropdownMain(discord.ui.Select):
    def __init__(self):
        global select
        select = [
            discord.SelectOption(label="Minecraft"),
            discord.SelectOption(label="Terraria")
        ]
        super().__init__(placeholder="Select Game",
                         min_values=1, max_values=1, options=select)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Minecraft":
            await interaction.response.send_message(f'You choose {self.values[0]}. Pick a Ref.', view=DropdownViewMC())
        elif self.values[0] == "FinalRepublic":
            await interaction.response.send_message(f'You choose {self.values[0]}. Pick a Ref.', view=DropdownViewFR())


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    pass


# this decorator makes a slash command
@bot.slash_command(name="ping", description="Sends the bot's latency.")
async def ping(inter):  # a slash command will be created with the name "ping"
    await inter.respond(f"Pong! Latency is {bot.latency}")


@bot.slash_command(name="roll", description='Automatically roll a di(c)e of your choice, must be in NdN format, defaults to 4d6.')
async def roll(inter, dice: str = "4d6"):
    rolls, limit = map(int, dice.split("d"))
    result = ", ".join(str(random.randint(1, limit)) for _ in range(rolls))
    await inter.respond(result)


@bot.slash_command(name="ref", description='A command that contains many refrence images, like trades, ore-gen, maps, and fishing loot')
async def ref(inter):
    view = DropdownViewMain(timeout=None)
    await inter.respond("Choose Game", view=view)


@bot.slash_command(name="help", description='A general help command')
async def help(inter):
    helpEmbed = discord.Embed(title='Tesseract Help/About', colour=0xffffff)
    helpEmbed.add_field(name='Main Contributers', value='''
                        ***<@624191654282395648>:*** Helping with the bot a little.\n
                        ***<@625855485773611018>:*** Asked for Apoc1 support for his private server. This feature has been removed from the bot, but still credited for helping build the `/ref` framework.
                        ''')
    helpEmbed.add_field(name='Commands', value='''
                        `/ping`: Responds "Ping!" with the time it took to send the packet to Discord in ms.\n
                        `/roll`: Rolls a 4d6 dice or any custom die you like.\n
                        `/ref`: The remade refrence commmand for common Minecraft features. \n
                        `/help`: This embed you\'re looking at now with everything you will ever need/\n
                        ''')
    await inter.response.send_message(embed=helpEmbed)


bot.run(os.environ['TOKEN'])

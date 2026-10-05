from utils import discord, commands, asyncio, requests, random, json, tasks, app_commands

intents = discord.Intents.default()
intents.message_content = True

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"logged in as {self.user}")

    async def on_message(self, message):
        search_word = "ticket"
        if search_word in message.content:
            channel = message.channel
            view = Confirm()
            embed = discord.Embed(title='Create a Ticket', description='To create a ticket, click the button below.\nwhile you wait please list an issue, or what you would like to share.', color=discord.Color.blurple())
            await channel.send(embed=embed, view=view)
            await view.wait()

client = aclient()
tree = app_commands.CommandTree(client)


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.button(label="Create", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()

        user = interaction.user
        ticket_name = f"ticket-{user.name}"

        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True)
        }
        category = discord.utils.get(guild.categories, name="Tickets")
        if category is None:
            category = await guild.create_category(name="Tickets")

        ticket_channel = await category.create_text_channel(name=ticket_name, overwrites=overwrites)
        await interaction.response.send_message(f"Ticket {ticket_channel.mention} created for {user.mention}")

@tree.command(name="closerequest", description="Requests to close an opened ticket")
async def self(interaction: discord.Interaction, query: str):
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.followup.send("hi")

@tree.command(name="create", description="creates a ticket")
async def self(interaction: discord.Interaction, reason: str):
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.followup.send("hi")

@tree.command(name="close", description="closes the ticket")
async def self(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.followup.send("hi")

@tree.command(name="add_user", description="adds a user to the ticket")
async def self(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.followup.send("hi")
    
client.run('MTYOUR_DISCORD_BOT_TOKEN')

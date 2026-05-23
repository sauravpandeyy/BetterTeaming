import os
import re
import logging
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
import json
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

BANNED_WORDS = {
    "boob", "dick", "fuck", "nsfw", "porn", "sex", "drugs", "nitro", "hack", "ass", "penis", "lund", "asshole", "bitch", "slut", "whore", "cunt", "pussy", "fag", "faggot", "nigger", "nigga", "chink", "gook", "kike", "spic", "twat", "dildo", "blowjob", "handjob", "vagina", "cock", "tit", "tits", "cum", "sperm", "orgasm", "anal", "bdsm", "fetish", "incest", "bestiality", "rape", "pedo", "child", "cp", "loli", "shota", "hentai", "gore", "suicide", "terrorism", "discord.gg", "discord.com/invite", "discordapp.com/invite", "boobs", "b00b"
}
URL_PATTERN = re.compile(
    r"(?:https?://|www\.)[^\s<>]+",
    re.IGNORECASE
)
INVITE_PATTERN = re.compile(
    r"(?:discord(?:\.gg|\.com/invite)/[\w-]+|bit\.ly/[\w-]+|tinyurl\.com/[\w-]+)",
    re.IGNORECASE
)

# In-memory settings per guild
guild_settings = {}

def contains_inappropriate(text: str) -> bool:
    normalized = text.lower()
    if INVITE_PATTERN.search(normalized):
        return True
    for w in BANNED_WORDS:
        if re.search(rf"\b{re.escape(w)}\b", normalized):
            return True
    return False

def save_settings():
    try:
        json_safe_settings = {}
        for guild_id, config in guild_settings.items():
            json_safe_settings[str(guild_id)] = {
                "log_channel_id": config.get("log_channel_id"),
                "announcement_channel_id": config.get("announcement_channel_id"),
                "setup_channel_id": config.get("setup_channel_id"),
                "setup_message_id": config.get("setup_message_id"),
                "applications": config.get("applications", {}),
            }

        with open("settings.json", "w") as f:
            json.dump(json_safe_settings, f)
        logging.info("Settings saved to settings.json")
    except Exception as e:
        logging.error(f"Failed to save settings: {e}")

def load_settings():
    global guild_settings
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            for guild_id, config in data.items():
                guild_settings[int(guild_id)] = {
                            "log_channel_id": config.get("log_channel_id"),
                    "announcement_channel_id": config.get("announcement_channel_id"),
                    "setup_channel_id": config.get("setup_channel_id"),
                    "setup_message_id": config.get("setup_message_id"),
                    "applications": config.get("applications", {}),
                }
        logging.info(f"Loaded settings for {len(guild_settings)} guilds")
    except FileNotFoundError:
        logging.info("No settings.json found. Starting fresh.")
    except Exception as e:
        logging.error(f"Failed to load settings: {e}")

class BetterTeamingSetupView(View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=None)
        self.guild_id = guild_id

    @discord.ui.button(label="Looking for Teammates", style=discord.ButtonStyle.success, custom_id="betterteaming_look_for_teammates")
    async def look_for_teammates(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(BetterTeamingModal(self.guild_id))

class BetterTeamingModal(Modal, title="Provide Details"):
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        super().__init__(title="Provide Details")

        self.competition = TextInput(label="Looking for Teammates to participate in", placeholder="(e.g., Global Hackathon, Esports Tournament, etc.)", required=True, max_length=100)
        self.role = TextInput(label="Your Preferred Role in the Team will be", placeholder="(e.g., Frontend Developer, UI/UX Designer, etc.)", required=True, max_length=500)
        self.competitionlink = TextInput(label="Competition Link", placeholder="Paste Competition link here", required=True, max_length=200)
        self.team_size = TextInput(label="Number of Members needed", placeholder="Enter the number of members you are looking for", required=True, max_length=100)
        self.additional_info = TextInput(label="Anything else you would like to add?", style=discord.TextStyle.paragraph, placeholder="I would like to add...", required=False, max_length=1000)
        self.add_item(self.competition)
        self.add_item(self.role)
        self.add_item(self.team_size)
        self.add_item(self.competitionlink)
        self.add_item(self.additional_info)

    async def on_submit(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        settings = guild_settings.get(guild_id)
        if not settings:
            await interaction.response.send_message("This server is not configured yet.\nAsk an admin to run `/setup`.", ephemeral=True)
            return

        answers = [self.competition.value, self.role.value, self.additional_info.value, self.competitionlink.value, self.team_size.value]

        full_text = " ".join(answers)
        if contains_inappropriate(full_text):
            await interaction.response.send_message(
                "Your application was rejected!\nPlease edit and try again.",
                ephemeral=True,
            )
            log_channel_id = settings.get("log_channel_id")
            log_channel = interaction.client.get_channel(log_channel_id) if log_channel_id else None
            if log_channel:
                embed = discord.Embed(
                    description=f"## {interaction.user.mention} application rejected",
                    color=discord.Color.red(),
                )
                embed.add_field(name=f"{interaction.user.display_name}'s response", value=(full_text[:1024] + "...") if len(full_text) > 1024 else full_text, inline=False)
                await log_channel.send(embed=embed)
            return

        announcement_channel_id = settings.get("announcement_channel_id")
        announcement_channel = interaction.client.get_channel(announcement_channel_id) if announcement_channel_id else None
        if not announcement_channel:
            await interaction.response.send_message("Announcement channel is not set.\nAsk an admin to run `/setup`.", ephemeral=True)
            return
               
        entry= f"""## {interaction.user.mention} is looking for Teammates!\n
        > **Competition Name** ➜ {self.competition.value or 'N/A'}
        > **Number of Members needed** ➜ {self.team_size.value or 'N/A'}
        > **{interaction.user.display_name}'s preferred Role** ➜ {self.role.value or 'N/A'}
        > **Competition Link** ➜ [Click here!]({self.competitionlink.value})
        > ### **Additional Note from {interaction.user.display_name}:**
        > `{self.additional_info.value or 'N/A'}`\n-# Click the below \"I'm Interested\" button, if you want to team up!"""

        view = InterestedView(interaction.user.id)
        posted_message = await announcement_channel.send(entry, view=view, suppress_embeds=True)

        # store mapping in memory
        settings.setdefault("applications", {})[f"{posted_message.id}"] = {
            "applicant_id": interaction.user.id,
            "mode": "Looking for Teammates",
            "message_id": posted_message.id,
            "channel_id": announcement_channel.id,
        }

        await interaction.response.send_message("Application submitted and posted successfully!", ephemeral=True)

class InterestedView(View):
    def __init__(self, applicant_id: int):
        super().__init__(timeout=None)
        self.applicant_id = applicant_id

    @discord.ui.button(label="I'm Interested", style=discord.ButtonStyle.success, custom_id="betterteaming_interested")
    async def interested(self, interaction: discord.Interaction, button: Button):
        applicant_user = interaction.client.get_user(self.applicant_id)
        if not applicant_user:
            await interaction.response.send_message("Could not find application owner.\nPlease contact moderators.", ephemeral=True)
            return

        interested_user = interaction.user
        profile_link = f"https://discord.com/users/{interested_user.id}"

        try:
            await applicant_user.send(
                f"**{interested_user.mention}** showed interest to your call.\n"
                f"➜ [Connect now!]({profile_link})", suppress_embeds=True
            )
        except discord.Forbidden:
            pass

        try:
            await interested_user.send(
                "> Your response has been successfully recorded!\n> Thank you for showing interest!\n"
                "> Application owner will contact you shortly.\n\n> `ℹ️` Make sure you **enable DMs** from everyone."
            )
        except discord.Forbidden:
            pass

        await interaction.response.send_message(
            "Your interest has been registered!\nCheck DMs.",
            ephemeral=True,
        )

class BetterTeamingBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = False
        intents.members = True
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        self.tree.add_command(uptime)
        self.tree.add_command(setup)

    async def on_ready(self):
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logging.info("BetterTeaming Bot is ready!")
        load_settings()  # Load persisted settings
        await self.tree.sync()  # Sync slash commands

        await self.update_presence()

        for guild_id, config in guild_settings.items():
            setup_message_id = config.get("setup_message_id")
            if setup_message_id:
                try:
                    self.add_view(BetterTeamingSetupView(guild_id), message_id=setup_message_id)
                    logging.info(f"Reconnected setup view for guild {guild_id} message {setup_message_id}")
                except Exception as e:
                    logging.warning(f"Cannot re-register view for guild {guild_id}: {e}")

    async def update_presence(self):
        """Update bot presence with current guild count"""
        guild_count = len(self.guilds)
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"in {guild_count} server{'s' if guild_count != 1 else ''}"
            )
        )
        logging.info(f"Bot presence updated: {guild_count} server(s)")

    async def on_guild_join(self, guild: discord.Guild):
        """Called when bot joins a guild"""
        logging.info(f"Bot joined server: {guild.name} (ID: {guild.id})")
        await self.update_presence()

    async def on_guild_remove(self, guild: discord.Guild):
        """Called when bot leaves or is removed from a guild"""
        logging.info(f"Bot left server: {guild.name} (ID: {guild.id})")
        await self.update_presence()

bot = BetterTeamingBot()

@discord.app_commands.command(name="uptime", description="Check BetterTeaming latency")
async def uptime(interaction: discord.Interaction):
    latency_ms = round(interaction.client.latency * 1000)
    await interaction.response.send_message(f"`📶` Latency: {latency_ms}ms", ephemeral=True)

@discord.app_commands.command(name="setup", description="Setup BetterTeaming in this server [Admin Only]")
@app_commands.checks.has_permissions(administrator=True)
async def setup(interaction: discord.Interaction, log_channel: discord.TextChannel, announcement_channel: discord.TextChannel, setup_channel: discord.TextChannel):
    guild_id = interaction.guild_id
    guild_settings[guild_id] = {
        "log_channel_id": log_channel.id,
        "announcement_channel_id": announcement_channel.id,
        "setup_channel_id": setup_channel.id,
        "applications": {},
    }
    save_settings()

    embed = discord.Embed(
        title="Are you looking for teammates?",
        description=f"Click on the button below to make a call-for-teammates announcement.",
        color=0x232323,
    )

    view = BetterTeamingSetupView(guild_id)
    setup_msg = await setup_channel.send(embed=embed, view=view)

    guild_settings[guild_id]["setup_message_id"] = setup_msg.id
    save_settings()

    await interaction.response.send_message(
        f"Setup complete!\nThe setup message has been sent to {setup_channel.mention}",
        ephemeral=True
    )

@setup.error
async def setup_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You need Admin permission to run this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise SystemExit("DISCORD_BOT_TOKEN environment variable is required")
    bot.run(token)

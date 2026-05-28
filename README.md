# <p align="center">BetterTeaming Discord Bot</p>

<p align="center">A simple discord bot built for helping people <b>find teammates</b> to participate in <b>Competitions and Hackathons</b>.</p>

<div align="center">

![Python Version](https://img.shields.io/badge/-Python_3.11-blue?style=flat)
![Discord.py](https://img.shields.io/badge/-Made_with_discord.py-646464?style=flat)
[![BetterTeaming Invite](https://img.shields.io/badge/-Invite_BetterTeaming_Bot-ffdd00?style=flat)](https://discord.com/oauth2/authorize?client_id=1487079107446571018&permissions=67488832&scope=bot%20applications.commands "Click here to invite the bot to your discord server")

</div>

## BetterTeaming Commands

Commands | Description
----------------|----------------
`/setup log_channel:<CHANNEL> announcement_channel:<CHANNEL> setup_channel:<CHANNEL>` | For setting up BetterTeaming Bot [Admin Only]
`/uptime` | For checking BetterTeaming Bot Latency

## Build your own BetterTeaming Bot

1. Create a Discord application and bot at https://discord.com/developers/applications
2. Under OAuth2 > URL Generator, select scopes `bot` and `applications.commands`.
3. Under bot permissions, allow `Send Messages`, `Read Message History`, `Use Slash Commands`, `Manage Messages` (optional), `View Channels`.
4. Invite the bot to your server.
5. Set environment variable:
     ```powershell
     $env:DISCORD_BOT_TOKEN = "YOUR_BOT_TOKEN"
     ```
6. Install dependencies:
   ```powershell
   pip install -U discord.py
   ```
7. Run bot:
   ```powershell
   python main.py
   ```

## Customization

- [BANNED_WORDS](https://github.com/sauravpandeyy/BetterTeaming/blob/741f3eb87c640ff4d4d61448cff095fe8dd00a41/main.py#L14) and [URL_PATTERN](https://github.com/sauravpandeyy/BetterTeaming/blob/741f3eb87c640ff4d4d61448cff095fe8dd00a41/main.py#L17) are in `main.py`.
- Use persistent storage if you want state to survive restarts (the current code uses in-memory dictionary).

## Notes

- Users must allow DMs from server members to receive notifications and connect.
- Administrator can re-run `/setup` command to update channels.

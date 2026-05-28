# <p align="center">BetterTeaming Discord Bot</p>

<p align="left">
  <img width="100" src="https://raw.githubusercontent.com/sauravpandeyy/BetterTeaming/main/assets/bt-logo.png" align="right" style="margin-left: 20px;">
</p>

<p>A simple Discord bot built for helping people <b>find teammates</b> to participate in <b>Competitions and Hackathons</b>.</p>

![Python Version](https://img.shields.io/badge/-Python_3.11-646464?style=flat)
[![Discord.py](https://img.shields.io/badge/-Made_with_discord.py-646464?style=flat)](https://discordpy.readthedocs.io/)
[![GitHub License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://github.com/sauravpandeyy/BetterTeaming/blob/main/LICENSE)
![Open-Source](https://img.shields.io/badge/-Open_Source-green?style=flat)
[![BetterTeaming Invite](https://img.shields.io/badge/-Invite_BetterTeaming_Bot-ffdd00?style=flat)](https://discord.com/oauth2/authorize?client_id=1487079107446571018&permissions=67488832&scope=bot%20applications.commands "Click here to invite BetterTeaming Bot to your Discord Server")
[![BetterTeaming Support Community Server](https://img.shields.io/badge/-BetterTeaming_Support_Server-5865f2?style=flat)](https://discord.gg/xh6ereusMh "Click here to join BetterTeaming Support Discord Server")

## BetterTeaming Commands

Commands | Description
----------------|----------------
`/setup log_channel:<CHANNEL> announcement_channel:<CHANNEL> setup_channel:<CHANNEL>` | For setting up BetterTeaming Bot [Admin Only]
`/uptime` | For checking BetterTeaming Bot Latency

## Build your own BetterTeaming Bot

1. Create a Discord application and bot at https://discord.com/developers/applications
2. In OAuth2, under OAuth2 URL Generator, select scopes `bot` and `applications.commands`
3. Under Bot Permissions, allow the following:
    - `Send Messages`
    - `Read Message History`
    - `Use Slash Commands`
    - `Manage Messages`
    - `View Channels`
4. Invite the bot to your server.
5. Create a `.env` file and set the environment variable:
     ```powershell
     DISCORD_BOT_TOKEN = "YOUR_BOT_TOKEN"
     ```
6. Install prerequisites:
   ```powershell
   pip install -r requirements.txt
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

## BetterTeaming Support Community

Join us on our [Official Discord Server](https://discord.gg/xh6ereusMh)!

## License

Released under the [MIT license](https://github.com/sauravpandeyy/BetterTeaming/blob/main/LICENSE).

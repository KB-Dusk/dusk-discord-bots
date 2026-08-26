# Dusk Discord Bots

A suite of Discord bots built with Python, discord.py and SQLite. Includes a moderation bot, economy bot, and a combined version that runs both together. Built as part of a freelance portfolio.

## Bots

### Combined Bot (Main)
Runs both moderation and economy features in one bot.

### Admin Bot
Moderation only version.

### Economy Bot
Economy only version.

## Features

### Moderation Commands
| Command | Description |
|---|---|
| `!warn @user reason` | Issues a warning and saves it to the database |
| `!warnings @user` | Displays all warnings for a user |
| `!clearwarnings @user` | Clears all warnings for a user |
| `!kick @user reason` | Kicks a user from the server |
| `!ban @user reason` | Permanently bans a user |
| `!clear amount` | Deletes a specified number of messages |

### Economy Commands
| Command | Description |
|---|---|
| `!daily` | Claim 100 coins once every 24 hours |
| `!balance` | Check your coin balance |
| `!pay @user amount` | Transfer coins to another user |
| `!shop` | View items available to buy |
| `!buy item` | Purchase an item from the shop |
| `!inventory` | View your owned items |
| `!leaderboard` | Top 10 richest users |
| `!additem price name description` | Add item to shop (admin only) |

## Tech Stack
- Python 3.11
- discord.py
- SQLite3
- python-dotenv

## Setup

1. Clone the repository:
   git clone https://github.com/KB-Dusk/dusk-discord-bots.git

2. Navigate into the folder:
   cd dusk-discord-bots

3. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

4. Install dependencies:
   pip install discord.py python-dotenv

5. Create a .env file in the root folder:
   TOKEN=your_bot_token_here

6. Run your preferred bot:
   python3 combined_bot.py

## Requirements
- Python 3.11+
- A Discord bot token from the Discord Developer Portal
- Server Members Intent and Message Content Intent enabled

## Notes
- Warnings and economy data are stored persistently in a local SQLite database
- The .env file is excluded from version control — never share your bot token
- Run combined_bot.py for full functionality

## PROJECT GOALS
─────────────────────────────────────────────
✅ Build a working Discord bot using Python and discord.py
✅ Implement moderation commands (kick, ban, warn, clear)
✅ Store warnings persistently using SQLite database
✅ Structure code using class-based Cog architecture
✅ Build a separate economy system (daily, balance, shop, buy, inventory, leaderboard)
✅ Combine both systems into one unified combined bot
✅ Handle errors gracefully with user-facing messages
✅ Push to GitHub with a professional README
✅ Keep bot token secure using .env and .gitignore

## STRETCH GOALS
─────────────────────────────────────────────
✅ Use separate entry points for moderation-only and economy-only versions
⬜ Connect to a live dashboard (planned in v2)
⬜ Add slash commands alongside prefix commands

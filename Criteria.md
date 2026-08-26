# Project Criteria — Dusk Discord Bots

## Overview
Build a working Discord bot suite in Python with moderation and economy features, using a clean class-based architecture and persistent SQLite storage.

## Core Requirements

| Requirement | Status |
|---|---|
| Build a working Discord bot using Python and discord.py | ✅ Met |
| Implement moderation commands (kick, ban, warn, clear) | ✅ Met |
| Store warnings persistently using SQLite database | ✅ Met |
| Structure code using class-based Cog architecture | ✅ Met |
| Build a separate economy system (daily, balance, shop, buy, inventory, leaderboard) | ✅ Met |
| Combine both systems into one unified combined bot | ✅ Met |
| Handle errors gracefully with user-facing messages | ✅ Met |
| Keep bot token secure using .env and .gitignore | ✅ Met |
| Push to GitHub with a professional README | ✅ Met |
| Provide separate entry points for moderation-only and economy-only versions | ✅ Met |

## Success Scenario
The bot is running live in a Discord server. A server admin can issue `!warn`, `!kick`, `!ban` and `!clear` commands. Warnings persist across bot restarts. Members can use `!daily`, `!shop`, `!buy` and `!leaderboard`. All three entry points (`admin_bot.py`, `economy_bot.py`, `combined_bot.py`) run without errors.

## Evaluation
- **Moderation:** Commands work correctly and only users with the right permissions can use them
- **Economy:** Coins persist in the database and the shop/inventory system functions end to end
- **Code quality:** Each feature is in its own class/cog with a single responsibility
- **Security:** Token is never hardcoded or committed to GitHub

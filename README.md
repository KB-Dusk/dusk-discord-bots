# Dusk Moderator Bot

A Discord moderation bot built with Python and discord.py, using SQLite for persistent warning storage. Built as part of a freelance portfolio project.

## Features

| Command | Description |
|---|---|
| `!warn @user reason` | Issues a warning to a user and saves it to the database |
| `!warnings @user` | Displays all warnings for a user |
| `!clearwarnings @user` | Clears all warnings for a user |
| `!kick @user reason` | Kicks a user from the server |
| `!ban @user reason` | Permanently bans a user from the server |
| `!clear amount` | Deletes a specified number of messages |

## Tech Stack

- Python 3.11
- discord.py
- SQLite3
- python-dotenv

## Setup

1. Clone the repository:
   git clone https://github.com/KB-Dusk/discord-mod-bot.git

2. Navigate into the folder:
   cd discord-mod-bot

3. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

4. Install dependencies:
   pip install discord.py python-dotenv

5. Create a .env file in the root folder:
   TOKEN=your_bot_token_here

6. Run the bot:
   python3 bot.py

## Requirements

- Python 3.11+
- A Discord bot token from the Discord Developer Portal
- Server Members Intent and Message Content Intent enabled in the Developer Portal

## Notes

Warnings are stored persistently in a local SQLite database (warnings.db).
The .env file is excluded from version control — never share your bot token publicly.

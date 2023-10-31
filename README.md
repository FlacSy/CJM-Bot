# CJM Bot

CJM Bot is a Discord bot written using the disnake library. It has several interesting features such as:

- Select role color using reactions
- Creation of game rooms upon request
- Counting messages and user levels
- Play radio in voice channels
- Issuing an initial role when logging into the server
- Search images by request
- Search on rule34 (only in NSFW channels)

## Installation

To start the bot you will need:

- Python 3.9 or higher
- disnake library
- sqlite3 library
- requests library
- BeautifulSoup4 Library
- translate library
- rule34Py library
- Discord bot token
- Unsplash API Key

Clone the repository with the bot code:

```bash
git clone https://github.com/FlacSy/CJM-Bot.git
```
# Usage
Example for setting up a channel to select a role color, use the command:

`/setcolorschannel #your-channel-name`

To configure a channel for creating game rooms, use the command:

`/setgameroomchannel #your-channel-name`

To set up a channel for welcome messages, use the command:

`/welcomemessage #your-channel-name "your welcome message text" "your welcome image url (optional)"`

To configure a radio channel, use the command:

`/setradiochannel #your-channel-name`

To configure the default role when logging into the server, use the command:

`/startrole your-role-id`
# Setting up config.py
```
# Discord bot token
TOKEN = "your_token_here"

# Unsplash API Key
UNSPLASH_API_KEY = "your_key_here"

# Bot owner ID (for administration commands)
owner_id = your_id_here

# Server ID for development (for testing commands)
dev_guild = your_guild_id_here

# URL for requests to Unsplash API
UNSPLASH_API = "https://api.unsplash.com/search/photos"
```
# License
This project is distributed under the MIT license. See file [LICENSE](LICENSE) for details

## Author
- [FlacSy](https://github.com/FlacSy)
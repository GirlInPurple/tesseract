# Tesseract

A Gaming Utility Discord bot written in Python with Nextcord.

## Setup

First, clone the repo to your system of choice, make a file called `config.py` <!--`config.json`--> and copy paste this template into it:

```python
TOKEN = "1234567890"
TUsers = []
```

this is a draft of the .json file
keep this here until it is useful
-->

- `token` is your bot token, which can be grabbed from [here](https://discord.com/developers/applications).
- `TUsers` are users with admin access to the bot, like the `/debug` and other similar commands.

Note, eventually this will switch from a .py to a .json for simplicity and usability, but thats low on priority right now. This is the possible format for said updated config file

```json
{
    "global": [
        "TOKEN": "ADD TOKEN HERE"
        "TUsers": [user id, another user id, as many as you need]
        "apikeys": [Mojang API key, Twitch API key, more added later]
    ]
    "server id":[
        "defaultroles": [role id, another role id, can have infinite ids here (unlike other services, looking at you Dyno and YAGPDB)]
    ]
}
```

## Plans

- Finish Terriara/Calamity and Apoc Reference Sheets
- Twitch/YT for new posts and streams
- Overwatch, Apex Leg., and Mojang APIs
- Make a more descriptive help command
- Music commands
- Default roles when joining a server
- 3 strikes moderation command

## Contributing

Feel free to submit a PR or just fork off this project and go your own direction, its MIT license for a reason.

## Credits

- [Nextcord Bot Examples](https://github.com/nextcord/nextcord/tree/master/examples)

# Tesseract

A Gaming Utility Discord bot written in Python with the PyCord library.

## Setup

### Docker Container

Run the following command when you have the image installed:
```
docker run \
    -d \
    -it \
    --name tesseract \
    --restart=unless-stopped \
    -v /home/user/tesseract:/data \ #optional
    -e TOKEN=12345678901234567890 \
-i tesseract
```

### Running the script on its own

You're going to have to make an environment variable called `TOKEN`, then just drop the script into whatever folder you want to be the main folder. I recommend placing a `.bat` file in your startup folder for restarting the bot if you do this.

### Running older versions

These versions are not recommended to run due to bugs and unfinished features, but if you wish to run them, place a file named `config.py` and copy-paste this template into it:

```python
TOKEN = "12345678901234567890"
TUsers = []
```

- `token` is your bot token, which can be grabbed from [here](https://discord.com/developers/applications).
- `TUsers` are users with admin access to the bot, like the `/debug` and other similar commands.

## Plans

- Twitch/YT for new posts and streams
- Roblox, Apex Leg., and Mojang APIs
- Make a more descriptive help command
- Default roles when joining a server
- Finish the Wiki system (might be merged into another project)

### What I wont do

- Music commands
- Moderation systems

## Contributing

Feel free to submit a PR or just fork off this project and go your own direction, its MIT license for a reason.

## Credits

### People

wip

### Sites

- [Nextcord Bot Examples](https://github.com/nextcord/nextcord/tree/master/examples)
- [PyCord](https://guide.pycord.dev/)

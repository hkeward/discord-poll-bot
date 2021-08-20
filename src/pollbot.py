#!/usr/bin/env python3

import discord
import os

client = discord.Client()
token = os.getenv("DISCORD_POLL_BOT_TOKEN")

poll_option_emoji = [
    "\U0001F1E6",
    "\U0001F1E7",
    "\U0001F1E8",
    "\U0001F1E9",
    "\U0001F1EA",
    "\U0001F1EB",
    "\U0001F1EC",
    "\U0001F1ED",
    "\U0001F1EE",
    "\U0001F1EF",
    "\U0001F1F0",
    "\U0001F1F1",
    "\U0001F1F2",
    "\U0001F1F3",
    "\U0001F1F4",
    "\U0001F1F5",
    "\U0001F1F6",
    "\U0001F1F7",
    "\U0001F1F8",
    "\U0001F1F9",
    "\U0001F1FA",
    "\U0001F1FB",
    "\U0001F1FC",
    "\U0001F1FD",
    "\U0001F1FE",
    "\U0001F1FF",
]


async def usage(channel):
    help_string = """Hello I'm a pollbot that doesn't serve ads

    Usage: $poll {poll name} [option A] [option B] [option C]

    """
    await channel.send(help_string)


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    channel = message.channel

    if message.author == client.user:
        return

    if message.content.startswith("$poll"):
        if "help" in message.content:
            await usage(channel)
        else:
            try:
                poll_title = message.content.split("{")[1].split("}")[0]
                poll_options = [
                    option.strip("] ")
                    for option in message.content.split("}")[1].strip().split("[")[1:]
                ]

                embedded_message = discord.Embed(title=poll_title, color=0xCCEE6D)

                # append poll option emoji to each option
                bot_reactions = list()
                for index, option in enumerate(poll_options):
                    emoji = poll_option_emoji[index]
                    embedded_message.add_field(
                        name="\U0000200B",
                        value="{}\t{}".format(emoji, option),
                        inline=False,
                    )
                    bot_reactions.append(emoji)

                bot_message = await channel.send(embed=embedded_message)

                for emoji in bot_reactions:
                    await bot_message.add_reaction(emoji)

            except Exception as exception:
                print("[ERROR] {}".format(exception))
                await channel.send(
                    "Something went wrong; did you format your command properly?"
                )
                await usage(channel)


client.run(token)

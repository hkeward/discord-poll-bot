#!/usr/bin/env python3

from argparse import ArgumentParser
import discord
import os

client = discord.Client()
token = os.getenv("DISCORD_POLL_BOT_TOKEN")

poll_request_id_to_poll_message = dict()

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
    help_string = """
Hello, I'm pollbot :]

**Usage**
Show commands
`$poll help`

Create a poll
`$poll {poll name} [option A] [option B] [option C]`

Update a poll -- you can also simply edit the message you used to create the poll!
`$poll update {new poll name} [option A] [option B]`

    """
    await channel.send(help_string)

def content_to_embed(content):
    poll_title = content.split("{")[1].split("}")[0]
    poll_options = [
        option.strip("] ")
        for option in content.split("}")[1].strip().split("[")[1:]
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

    return bot_reactions, embedded_message


async def create_poll(channel, content, incoming_message_id):
    try:
        bot_reactions, embedded_message = content_to_embed(content)

        bot_poll_message = await channel.send(embed=embedded_message)

        for emoji in bot_reactions:
            await bot_poll_message.add_reaction(emoji)

    except Exception as exception:
        print("[ERROR] {}".format(exception))
        await channel.send(
            "Something went wrong; did you format your command properly?"
        )
        await usage(channel)

    global poll_request_id_to_poll_message
    poll_request_id_to_poll_message[incoming_message_id] = bot_poll_message



async def edit_poll(previous_poll_message, new_content, incoming_message_id):
    try:
        bot_reactions, embedded_message = content_to_embed(new_content)

        length_previous_poll = len(previous_poll_message.embeds[0].fields)
        length_edited_poll = len(embedded_message.fields)

        await previous_poll_message.edit(embed=embedded_message)

        if length_previous_poll > length_edited_poll:
            emoji_to_remove = poll_option_emoji[length_edited_poll:length_previous_poll]

            updated_message = await previous_poll_message.channel.fetch_message(previous_poll_message.id)
            reactions = updated_message.reactions
            for reaction in reactions:
                if reaction.emoji in emoji_to_remove:
                    await reaction.clear()

        elif length_previous_poll < length_edited_poll:
            for emoji in bot_reactions:
                await previous_poll_message.add_reaction(emoji)

        global poll_request_id_to_poll_message
        if incoming_message_id not in poll_request_id_to_poll_message:
            poll_request_id_to_poll_message[incoming_message_id] = previous_poll_message

    except Exception as exception:
        print("[ERROR] {}".format(exception))
        await previous_poll_message.channel.send(
            "Something went wrong editing that poll"
        )
        await usage(previous_poll_message.channel)


def main(args):
    @client.event
    async def on_ready():
        print("Logged in as {0.user}".format(client))

    @client.event
    async def on_message(message):
        channel = message.channel

        if args.debug and channel.name != "testing":
            return

        if message.author == client.user:
            return

        if message.content.startswith("$poll"):
            subcommand = message.content.split(" ")[1]

            if subcommand == "help":
                await usage(channel)

            elif subcommand == "update":
                if len(poll_request_id_to_poll_message) > 0:
                    poll_message_to_edit = poll_request_id_to_poll_message[list(poll_request_id_to_poll_message)[-1]]
                else:
                    poll_message_to_edit = None

                if poll_message_to_edit is None:
                    await channel.send("No previous poll detected; creating new one")
                    await create_poll(channel, message.content, message.id)
                else:
                    await edit_poll(poll_message_to_edit, message.content, message.id)

            else:
                await create_poll(channel, message.content, message.id)

    @client.event
    async def on_message_edit(before_message, after_message):
        channel = after_message.channel

        if args.debug and channel.name != "testing":
            return

        if after_message.author == client.user:
            return

        if after_message.content.startswith("$poll"):
            if before_message.content.startswith("$poll"):
                poll_message_to_edit = poll_request_id_to_poll_message[after_message.id]
                await edit_poll(poll_message_to_edit, after_message.content, after_message.id)
            else:
                await create_poll(channel, after_message.content, after_message.id)

    client.run(token)





if __name__ == "__main__":
    parser = ArgumentParser(description="Run poll bot")

    parser.add_argument("-d", "--debug", default=False, action="store_true", help="Run bot only in the `testing` channel", required=False)

    args = parser.parse_args()

    main(args)

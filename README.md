# discord-poll-bot

A simple (ad-free) poll bot for Discord.


## Build docker image

Run `make build` from the repo root directory.


## Run using docker-compose

Make sure the variable `DISCORD_POLL_BOT_TOKEN` is defined in your environment.

After building the docker image, run `docker-compose up -d` from the repo root directory.


## Interacting with the bot

Poll the bot in channels in which it's enabled using `$poll {poll title} [option A] [option B] ... [option N]`

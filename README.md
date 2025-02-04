# ollama + discord bot
Discord bot that uses a locally running instance of an ollama model of your choice

## Setup (requires at least Python 3.11)
1. [Install Docker](https://www.docker.com/)
2. [Install Ollama](https://ollama.com/download/)
3. Run `git clone git@github.com:itsamayo/ollama-discord-bot.git`
4. Run `cp example_config.toml config.toml` and replace add your bot's token and the model of your choice (ensure the model is available locally)

## Quickstart
1. Run `python main.py`

## Docker
1. Run `docker build -t ollama-discord-bot .`
2. Run `docker run -d --name ollama-discord-bot --restart unless-stopped --network host ollama-discord-bot`

## Usage
1. Tag your bot in a message followed by your request i.e `@yourbot give me the 118th number in the Fibonacci sequence`

***Note: Due to limitations on the Discord API where a single message can't contain more than 2k characters, responses from the LLM are chunked into multiple messages when necessary***

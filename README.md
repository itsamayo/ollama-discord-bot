# discord + ollama bot
Discord bot that uses a locally running instance of an ollama model of your choice

## Setup
1. [Install Docker](https://www.docker.com/)
2. [Install Ollama](https://ollama.com/download/)
3. Run `git clone git@github.com:itsamayo/ollama-discord-bot.git`
3. Run `cp example_config.toml config.toml` and replace add your bot's token and the model of your choice (ensure the model is available locally)
4. Run `docker build -t discord-ollama-bot .`
5. Run `docker run -d --name discord-ollama-bot --restart unless-stopped --network host discord-ollama-bot`

## Usage
1. Tag your bot in a message followed by your request i.e `@yourbot give me the 118th number in the Fibonacci sequence`

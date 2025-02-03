import os
import json
import requests
import discord
import tomllib

def load_config(file_path="config.toml"):
    with open(file_path, 'rb') as f:
        return tomllib.load(f)

HISTORY_FILE_PATH = "history.json"

def load_conversation_history():
    if os.path.exists(HISTORY_FILE_PATH):
        with open(HISTORY_FILE_PATH, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Warning: Corrupted history file, starting fresh.")
    return []

def save_conversation_history(history):
    with open(HISTORY_FILE_PATH, 'w') as file:
        json.dump(history, file)

def generate_response(prompt, conversation_history, config):
    conversation_history.append({"role": "user", "content": prompt})
    save_conversation_history(conversation_history)

    data = {
        "model": config['ollama']['model'],
        "messages": conversation_history,
        "stream": False  # Streaming should be left disabled
    }

    try:
        response = requests.post(config['ollama']['uri'], json=data)
        response.raise_for_status()  # Raise exception for HTTP errors
        response_data = response.json()

        assistant_message = response_data.get('message', {}).get('content', "No content in response.")
        conversation_history.append({"role": "assistant", "content": assistant_message})
        save_conversation_history(conversation_history)

        return assistant_message
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with API: {e}")
        return "Error: Unable to fetch response from the API."
    except (json.JSONDecodeError, KeyError):
        return "Error: Invalid API response."


class DiscordBot(discord.Client):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.conversation_history = load_conversation_history()

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return

        if self.user.mentioned_in(message):
            prompt = f"{message.author.display_name} says: {message.content}"

            try:
                async with message.channel.typing():
                    response = generate_response(prompt, self.conversation_history, self.config)
                    await message.channel.send(response)
            except discord.errors.Forbidden:
                print(f"Error: No permission to send messages in {message.channel.name}")


if __name__ == "__main__":    
    config = load_config()
    
    intents = discord.Intents.default()
    intents.message_content = True

    bot = DiscordBot(config=config, intents=intents)
    bot.run(config['discord']['token'])

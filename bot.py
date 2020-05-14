import os
from time import sleep
from datetime import datetime
from random import choice, randint

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.comparisons import levenshtein_distance

from dotenv import load_dotenv
import discord
import pyowm
import giphy_client

if __name__ == '__main__':
    load_dotenv()

    chatbot = ChatBot('Harold')

    OPENWEATHERMAP_TOKEN = os.getenv('OPENWEATHERMAP_TOKEN')
    owm = pyowm.OWM(OPENWEATHERMAP_TOKEN)
    observation = owm.weather_at_place('Krakow,PL')

    GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')
    giphy = giphy_client.DefaultApi()

    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user.name} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        request = message.content

        def matches(*phrases, distance=levenshtein_distance, threshold=0.8):
            return any(distance.compare(Statement(request), Statement(phrase)) > threshold for phrase in phrases)

        if matches('what time is it?', "what's the current time?", 'tell me the current time'):
            await message.add_reaction('🕓')
            response = f"It's {datetime.now():%Y-%m-%d %H:%M:%S} now."

        elif matches("what's the weather like?", 'tell me the weather'):
            await message.add_reaction('🌍')
            weather = observation.get_weather()
            temperature = weather.get_temperature('celsius')['temp']
            response = f'Current temperature is {temperature:.1f} °C.'

        elif matches('show me a funny meme', 'please send me a dank meme', 'send memes'):
            await message.add_reaction('😂')
            gif = giphy.gifs_random_get(GIPHY_API_KEY, tag='spongebob')
            response = gif.data.image_original_url

        elif matches('random number', 'random guess', 'dice roll'):
            await message.add_reaction('🎲')
            response = f'{randint(1, 6)}!'

        else:
            bot_response = chatbot.get_response(request)
            response = str(bot_response)

            print(response)

            if 'pizza' in response:
                emoji = '🍕'
            if 'spaghetti' in response:
                emoji = '🍝'
            elif 'cash' in response:
                emoji = '💵'
            elif bot_response.confidence >= 0.1:
                emoji = choice('😃👍')
            else:
                emoji = '🤷‍♀️'
                # response = choice((
                #     'What do you mean?',
                #     "I don't understand",
                #     'What do you mean by that?',
                #     "Sorry, I didn't understand you",
                # ))

            await message.add_reaction(emoji)

        await message.channel.send(f'{message.author.mention} {response}')

    client.run(DISCORD_TOKEN)

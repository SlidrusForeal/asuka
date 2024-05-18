import discord
import asyncio
import random
import os
from datetime import datetime, timezone, timedelta

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Function to send a GIF message
async def send_gif(channel, gif_url):
    await channel.send(gif_url)

async def send_picture(channel):
    picture_folder = 'aska'
    pictures = os.listdir(picture_folder)
    picture_file = random.choice(pictures)
    picture_path = os.path.join(picture_folder, picture_file)
    await channel.send(file=discord.File(picture_path))

async def send_random_message(channel):
    messages =     messages = [
        "Ave Sos, Deus UwU!",
        "Слава нашему кайзеру!",
        "Брунчик я тебя люблю",
        "UwU",
        "OwO",
        "Наш кайзер самый лучший",
        "Кайзер пойдём нашиться под пледиком?",
        "Брунчик давай в танки поиграем",
        "Брунчик я купила водочки",
        "Gott mit uns",
        "Ты заставляешь мое сердце биться чаще.",
        "Строить корабли - важно",
        ':heart:',
        'Ня',
        'Мурр',
        'Трогать можно только бруно!',
        'Мяу',
        'Я делаю кущац',
        'https://cdn.discordapp.com/attachments/1220093141714206793/1237403955823120434/60.mov?ex=663b85bc&is=663a343c&hm=cd64f243ae7076aa4c98829f19779b9970ce85adc25870eedfac81702a32ed46&',
        'Очень жду вечный сон! :heart:',
        'Бомбить бомбить бомбить бомбить!',
        'Я думаю о Бруно с утра до вечера…',
        'Бруно такой мужественный и сильный, что мне всегда хочется скорее прижаться к нему…',
        'Моя жизнь сияет с того момента, как ты появился в ней!',
        'Ты принес свет в мою жизнь.',
        'Ты стал благословением в моей жизни.',
        'От тебя в груди трепещет всё — да так, что глаз не отвести.']

    message = random.choice(messages)
    await channel.send(message)

async def check_time():
    while True:
        # Get the current time in UTC+3
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)

        # Check if it's 7:30
        if current_time.hour == 7 and current_time.minute == 30:
            channel = client.get_channel(1231604515933917252)
            await send_gif(channel, 'https://tenor.com/view/asuka-langley-langley-asuka-evangelion-neon-genesis-evangelion-gif-8796834862117941782')

        # Check if it's between 8:00 and 21:00
        elif 8 <= current_time.hour < 22:
            channel = client.get_channel(1231604515933917252)  # 1237117168567582831

            # Check if it's time to send a random message (every 2 hours)
            if current_time.hour % 2 == 0 and current_time.minute == 0:
                await send_random_message(channel)


        # Check if it's 23:00
        elif current_time.hour == 23 and current_time.minute == 0:
            channel = client.get_channel(1231604515933917252)
            await send_gif(channel, 'https://tenor.com/view/asuka-langley-gif-26114337')

        # Sleep for 1 minute before checking the time again
        await asyncio.sleep(60)

# Event handler for when the bot is ready
@client.event
async def on_ready():
    print('Я родилась!')
    # Start checking the time when the bot is ready
    await client.change_presence(activity=discord.Game(name="Сосмарк"))
    await check_time()


# Start the bot
async def main():
    await client.start("MTI0MTQ2MDIxNzE3NTIxNjI1OA.Gvy--l.d-mneN0AeEIJaBABeBlWqWr2b6f4IH3OeQtboQ")

asyncio.run(main())

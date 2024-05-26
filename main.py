import asyncio
import os
import random
from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
intents.message_content = True
intents.members = True  # Нужно для получения списка участников

# Инициализация бота
bot = commands.Bot(command_prefix="$", intents=intents, proxy='http://proxy.server:3128')

# ID ролей
AUTHORIZED_ROLE_ID = ROLE_ID  # Замените на ID роли, которая может выполнять команду
OWNER_ID = OWNER_ID # Замените на ваш ID пользователя Discord

# Функция для отправки GIF сообщения
async def send_gif(channel, gif_url):
    await channel.send(gif_url)

async def send_picture(channel):
    picture_folder = 'aska'
    pictures = os.listdir(picture_folder)
    picture_file = random.choice(pictures)
    picture_path = os.path.join(picture_folder, picture_file)
    await channel.send(file=discord.File(picture_path))

async def send_random_message(channel):
    messages = [
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
        'От тебя в груди трепещет всё — да так, что глаз не отвести.',
        'Гоп стоп, он подошёл из-за угла...'
    ]

    message = random.choice(messages)
    await channel.send(message)

async def check_time():
    while True:
        # Получить текущее время в UTC+3
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)
        print(f"Проверка времени: {current_time.isoformat()}")  # Строка для отладки

        # Проверка на 7:30
        if current_time.hour == 7 and current_time.minute == 30:
            channel = bot.get_channel(1223373351209402504)
            if channel:
                await send_gif(channel,
                               'https://tenor.com/view/asuka-langley-langley-asuka-evangelion-neon-genesis-evangelion-gif-8796834862117941782')
            else:
                print("Канал не найден для сообщения в 7:30")

        # Проверка на время с 8:00 до 21:00
        elif 8 <= current_time.hour < 22:
            channel = bot.get_channel(1223373351209402504)  # 1237117168567582831

            # Проверка на время отправки случайного сообщения (каждые 2 часа)
            if current_time.hour % 2 == 0 and current_time.minute == 0:
                if channel:
                    await send_random_message(channel)
                else:
                    print("Канал не найден для случайного сообщения")

        # Проверка на 22:00
        elif current_time.hour == 0 and current_time.minute == 0:
            channel = bot.get_channel(1237117168567582831)
            if channel:
                await send_picture(channel)
            else:
                print("Канал не найден для сообщения в 22:00")

        # Проверка на 23:00
        elif current_time.hour == 23 and current_time.minute == 0:
            channel = bot.get_channel(1223373351209402504)
            if channel:
                await send_gif(channel, 'https://tenor.com/view/asuka-langley-gif-26114337')
            else:
                print("Канал не найден для сообщения в 23:00")

        # Пауза на 1 минуту перед следующей проверкой времени
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print('Я родилась!')
    await bot.change_presence(activity=discord.Game(name="Сосмарк"))
    await bot.tree.sync()  # Синхронизация команд с сервером
    bot.loop.create_task(check_time())

@bot.event
async def on_message(message):
    # Пересылка личных сообщений владельцу бота
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        owner = bot.get_user(OWNER_ID)
        if owner:
            await owner.send(f"Сообщение от {message.author.name}: {message.content}")
        else:
            print("Владелец не найден для пересылки сообщения")
    await bot.process_commands(message)

# Проверка наличия у пользователя авторизованной роли
def has_authorized_role(interaction: discord.Interaction):
    return any(role.id == AUTHORIZED_ROLE_ID for role in interaction.user.roles)

# Определение слэш-команды с проверкой роли
@bot.tree.command(name="skhnotify", description="Уведомить пользователей в указанных ролях с сообщением")
@app_commands.describe(roles="Роли для уведомления (через запятую, можно упоминания)", message="Сообщение для отправки")
@app_commands.check(has_authorized_role)
async def skhnotify(interaction: discord.Interaction, roles: str, message: str):
    roles_list = [role.strip() for role in roles.split(",")]
    found_roles = []

    for role_str in roles_list:
        # Проверка на упоминание роли
        if role_str.startswith("<@&") and role_str.endswith(">"):
            role_id = int(role_str[3:-1])
            role = discord.utils.get(interaction.guild.roles, id=role_id)
        else:
            role = discord.utils.get(interaction.guild.roles, name=role_str)

        if role:
            found_roles.append(role)
        else:
            await interaction.response.send_message(f"Роль '{role_str}' не найдена.", ephemeral=True)
            print(f"Роль '{role_str}' не найдена")
            return

    await interaction.response.send_message("Уведомление отправлено.", ephemeral=True)

    for role in found_roles:
        for member in role.members:
            try:
                await member.send(message)
                print(f"Сообщение отправлено {member.name}")
            except discord.Forbidden:
                await interaction.followup.send(f"Не смогла отправить сообщение {member.name} (Запрещено)", ephemeral=True)
                print(f"Не смогла отправить сообщение {member.name} (Запрещено)")
            except discord.HTTPException as e:
                await interaction.followup.send(f"Ошибка при отправке сообщения {member.name}: {e}", ephemeral=True)
                print(f"Ошибка при отправке сообщения {member.name}: {e}")
            await asyncio.sleep(1)  # Добавление задержки для избежания ограничения по скорости

@skhnotify.error
async def skhnotify_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("У вас нет прав для использования этой команды.", ephemeral=True)

async def main():
    async with bot:
        await bot.start("TOKEN")

asyncio.run(main())

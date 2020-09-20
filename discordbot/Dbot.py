import discord
from discord.ext import commands
from const import TOKEN, JOKE_CHANNEL, YTB_DIR
from discord.utils import get
from tools import make_playlist, remove_file
import embetfiles
from ytb_parser import get_videos_url, download_ytb_video, downloaded_jokes
from random import shuffle
import os


bot = commands.Bot(command_prefix='!')
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Bot connected. Congratulations!')


@bot.event
async def on_guild_join(guild):
    embetfiles.hello_embed.add_field(name='ID вашего сервера: ', value=guild.id)
    print(guild.text_channels)
    for channel in guild.text_channels:
        try:
            await channel.send(embed=embetfiles.hello_embed)
        except Exception:
            pass


@bot.command()
@commands.has_permissions()
async def help(ctx):
    embetfiles.hello_embed.clear_fields()
    embetfiles.hello_embed.add_field(name='ID вашего сервера: ', value=ctx.guild.id)
    embetfiles.hello_embed.add_field(name='!play', value='воспроизведение рофлов', inline=False)
    embetfiles.hello_embed.add_field(name='!play new', value='сначала новые', inline=True)
    embetfiles.hello_embed.add_field(name='!play rnd', value='в случайном порядке', inline=True)
    embetfiles.hello_embed.add_field(name='!stop', value='это очевидно',inline=False)
    embetfiles.hello_embed.add_field(name='!skip', value='пропуск рофла')
    embetfiles.hello_embed.add_field(name='!back', value='отмотка в начало рофла')
    embetfiles.hello_embed.add_field(name='!back 1', value='предыдущий рофл')
    await ctx.send(embed=embetfiles.hello_embed)


def queue(ctx, voice):
    global play_index
    if voice and voice.is_connected:
        if len(url_list) > play_index:
            print(len(url_list))
            print(len(url_list) > play_index)
            voice.play(discord.FFmpegPCMAudio(url_list[play_index]), after=lambda e: queue(ctx=ctx, voice=voice))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.7
            play_index += 1
        else:
            print('no tracks more')



@bot.command(aliases=['p'])
async def play(ctx, inf=''):
    global play_index
    play_index = 0

    if ctx.message.author.voice.channel:
        global url_list
        try:
            url_list = make_playlist(str(ctx.guild.id))
            if inf.lower() == 'random' or inf.lower() == 'rnd':
                shuffle(url_list)
            elif inf.lower() == 'new':
                url_list = list(reversed(url_list))

            await connect(ctx)
            voice = get(bot.voice_clients, guild=ctx.guild)

            queue(ctx, voice)

        except Exception:
            await ctx.send(
                f'Нет приколов ( \nПрисылайте свои приколы сюда https://t.me/coolroflbot \nID вашего сервера: {ctx.guild.id}')
    else:
        await ctx.send('Сорян, ты не подключен ни к одному войсчату')


def queue_joke(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)                   # add skip
    global play_index, url_list, way_list, downloaded_jokes, dwn_i    # move files to server's dir

    def dwl_video():
        global dwn_i
        try:
            downloaded_jokes[ctx.guild].append(download_ytb_video(url_list[dwn_i], dwn_i))
            dwn_i += 1
        except IndexError:
            print('index ERROR in downloading')

    if voice and voice.is_connected:
        dwl_video()

        if len(downloaded_jokes[ctx.guild]) > play_index:
            print(len(downloaded_jokes[ctx.guild]))
            print(len(downloaded_jokes[ctx.guild]) > play_index)
            voice.play(discord.FFmpegPCMAudio(downloaded_jokes[ctx.guild][play_index]), after=lambda e: queue_joke(ctx=ctx))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.7
            play_index += 1

            dwl_video()
            dwl_video()
        else:
            url_list.clear()
            del downloaded_jokes[ctx.guild]
            print('no tracks more')


@bot.command(aliases=['j', 'ощлу', 'JOKE', 'J'])
async def joke(ctx, url=JOKE_CHANNEL):                    # fix deleting
    global play_index, url_list, downloaded_jokes, dwn_i
    downloaded_jokes[ctx.guild] = []
    play_index = 0
    url_list = await get_videos_url(url)
    dwn_i = 0
    remove_file()

    if not url_list:
        await ctx.send('Ошибка воспроизведения')
        print('failed to play joke')
    else:
        await connect(ctx)
        await ctx.send('Воспроизведение вот-вот начнется')
        queue_joke(ctx)


@bot.command(aliases=['S', 's'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        url_list.clear()
        try:
            download_ytb_video[ctx.guild].clear()
        except TypeError:
            pass
        voice.stop()
        await ctx.send('Воспризведение остановлено')
        print('stoped')
        await disconnect(ctx)
    else:
        await disconnect(ctx)
        await ctx.send('Не могу остановиться')
        print('Failed to stop')


@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild= ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send('пауза')
        print('paused')
    else:
        await ctx.send('Не могу остановиться')
        print('Failed to pause')


@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild= ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send('Продолжаем')
        print('resumed')
    else:
        await ctx.send('А я забыл о чем шла речь')
        print('Failed to resume')


@bot.command(aliases=['sk', 'SK'])
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send('Скипнули')
    else:
        await ctx.send('Не могу')


@bot.command()
async def back(ctx, count=0):
    global play_index
    if (play_index == 0 and count > 0) or count > play_index:
        ctx.send('Неа')
    else:
        play_index -= (int(count)+1)
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            queue(ctx, voice)
            await ctx.send('Повторяю')
        else:
            await ctx.send('Не могу')


async def connect(ctx: commands.context.Context):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        if channel != voice.channel:
            await ctx.send(f'Сорян, я немного занят {channel}')
    else:
        voice = await channel.connect()
        await ctx.send(f'Я тут {channel}')


async def disconnect(ctx: commands.context.Context):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()


bot.run(TOKEN)

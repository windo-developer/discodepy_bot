import os
import asyncio
from dotenv import load_dotenv

from discord.ext import commands
from discord import Game, Embed, File, Color

from lol_command import getSummonerRankInfo, getSummonerId, getRankEmblem
from stock_price import getStockCode, stockDataframe, stockChart


class InitBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, command_prefix="!", help_command=None)


bot = InitBot()


def run_bot():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(DISCORD_TOKEN)


@bot.event
async def on_ready():
    print('Start Bot')


@bot.command()
async def jointest(ctx):
    await ctx.send("i joined discord")


@bot.command()
async def getid(ctx, arg):
    text = getSummonerId(arg)
    await ctx.send(text)


@bot.command()
async def help(ctx):
    embed = Embed(title="전적 봇 명령어", color=0x00ff56)
    embed.add_field(name="!help", value="도움말", inline=True)
    embed.add_field(name="!rank", value="!rank [소환사명] 전적 검색", inline=True)
    await ctx.send(embed=embed)


@bot.command(name='전적' or 'rank' or '롤전적')
async def rank(ctx, *, arg):
    summonerId = getSummonerId(arg)
    state = getSummonerRankInfo(summonerId)
    tier = getRankEmblem(summonerId)

    embed = Embed(title=f"{arg} 님의 전적",
                  description=f"{state}", color=0x00ff56)
    embed.add_field(name="자세한 전적은 OP.GG",
                    value=f"https://www.op.gg/summoner/userName={arg}")

    if (tier == 'IRON'):
        file = File("../img/emblems/Emblem_Iron.png",
                    filename="Emblem_Iron.png")
        embed.set_thumbnail(url="attachment://Emblem_Iron.png")
    elif (tier == 'BRONZE'):
        file = File("../img/emblems/Emblem_Bronze.png",
                    filename="Emblem_Bronze.png")
        embed.set_thumbnail(url="attachment://Emblem_Bronze.png")
    elif (tier == 'SILVER'):
        file = File("../img/emblems/Emblem_Silver.png",
                    filename="Emblem_Bronze.png")
        embed.set_thumbnail(url="attachment://Emblem_Silver.png")
    elif (tier == 'GOLD'):
        file = File("../img/emblems/Emblem_Gold.png",
                    filename="Emblem_Gold.png")
        embed.set_thumbnail(url="attachment://Emblem_Gold.png")
    elif (tier == 'PLATINUM'):
        file = File("../img/emblems/Emblem_Platinum.png",
                    filename="Emblem_Platinum.png")
        embed.set_thumbnail(url="attachment://Emblem_Platinum.png")
    elif (tier == 'DIAMOND'):
        file = File("../img/emblems/Emblem_Diamond.png",
                    filename="Emblem_Diamond.png")
        embed.set_thumbnail(url="attachment://Emblem_Diamond.png")
    elif (tier == 'MASTER'):
        file = File("../img/emblems/Emblem_Master.png",
                    filename="Emblem_Master.png")
        embed.set_thumbnail(url="attachment://Emblem_Master.png")
    elif (tier == 'GRANDMASTER'):
        file = File("../img/emblems/Emblem_GrandMaster.png",
                    filename="Emblem_GrandMaster.png")
        embed.set_thumbnail(url="attachment://Emblem_GrandMaster.png")
    elif (tier == 'CHALLENGER'):
        file = File("../img/emblems/Emblem_Challenger.png",
                    filename="Emblem_Challenger.png")
        embed.set_thumbnail(url="attachment://Emblem_Challenger.png")

    await ctx.send(file=file, embed=embed)


@bot.command(name='주식' or 'stock')
async def stockPrice(ctx, arg):
    stockData = stockDataframe(arg)
    date = stockData['date'][1]
    price = stockData['close'][1]
    diff = stockData['diff'][1]
    high = stockData['high'][1]
    low = stockData['low'][1]
    volume = stockData['volume'][1]

    url = stockChart(arg)
    file = File("../img/stockgosu.png", filename="stockgosu.png")

    embed = Embed(title=f"{arg}의 {date}주가",
                  color=0x00ff56)
    embed.add_field(name='주가(종가)', value=price, inline=True)
    if(stockData['close'][1] > stockData['close'][2]):
        embed.add_field(name='전일비', value=f"+{diff}", inline=True)
    else:
        embed.add_field(
            name='전일비', value=f"-{diff}", inline=True)
    embed.add_field(name='당일고가', value=high, inline=True)
    embed.add_field(name='당일저가', value=low, inline=True)
    embed.add_field(name='거래량', value=volume, inline=True)
    embed.set_thumbnail(url="attachment://stockgosu.png")
    embed.set_image(url=url)
    await ctx.send(file=file, embed=embed)

run_bot()

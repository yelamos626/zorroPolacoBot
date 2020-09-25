import os
import random
import discord
from dotenv import load_dotenv
import re
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import sqlite3


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD =os.getenv('DISCORD_SERVER')
global miembrosNoBot
miembrosNoBot =[]
global miembrosNoRepe
miembrosNoRepe =[]

client = discord.Client()

bot = commands.Bot(command_prefix='!')
pattern = re.compile("randomNumber\s[0-9]+")
channel = client.get_channel(753927474529828898)


@bot.command(name='saluda', help=os.getenv('ayuda_saluda'))
async def saludar(ctx):
    #channel = client.get_channel(753927474529828898)
    await ctx.send("HOLA")
    
@bot.command(name='randomMember', help=os.getenv('ayuda_randomMember'))
async def miembroRandom(ctx):
    global miembrosNoBot
    longitud = len(miembrosNoBot)
    print(f'longitud: {longitud}')
    x= random.randrange(0, longitud, 1)
    print(f'{miembrosNoBot[x].name}')
    await ctx.send(f'{miembrosNoBot[x].name}')
@bot.command(name='randomMember2', help=os.getenv('ayuda_randomMember2'))
async def miembroRandom2(ctx):
    global miembrosNoRepe
    longitud = len(miembrosNoRepe)
    print(f'longitud: {longitud}')
    if(longitud==0):
        resetMember()
        longitud = len(miembrosNoRepe)
        print(f'longitud2: {longitud}')
    x= random.randrange(0, longitud, 1)
    await ctx.send(f'{miembrosNoRepe[x].name}')
    del miembrosNoRepe[x]
@bot.command(name='resetMember', help=os.getenv('ayuda_resetMember'))
async def resetMemberAsync(ctx):
    global miembrosNoRepe
    global miembrosNoBot
    miembrosNoRepe = miembrosNoBot.copy()
    
def resetMember():
    global miembrosNoRepe
    global miembrosNoBot
    miembrosNoRepe = miembrosNoBot.copy()
    
@bot.command(name='randomNumber', help=os.getenv('ayuda_NumeroRandom'))
async def numeroRandom(ctx, arg):
    try:
        num = int(arg)
        if num > 1:
            x= random.randrange(1, num+1, 1)
        else:
            x= "Pon un número mayor de 1"

        await ctx.send(f'{x}')
    except:
        await ctx.send('Parametro incorrecto')
@bot.command(name='coinFlip', help=os.getenv('ayuda_coinFlip'))
async def coinFlip(ctx):
    opciones = ["cara", "cruz"]
    choice= random.choice(opciones)
    await ctx.send(f'{choice}')
    
@bot.command(name='murder', pass_context= True, help=os.getenv('ayuda_murder'))
@has_permissions(administrator=True)
async def baneo(ctx, member: discord.Member):    
    await ctx.guild.kick(member)
    
    
@baneo.error
async def kick_error(error, ctx):
    if isinstance(error, MissingPermissions):
        text = "Sin permisos {}".format(ctx.message.author)
        await bot.send_message(ctx.message.channel, text)

@bot.command(name='cargaDDBB', pass_context=True, help=os.getenv('ayuda_cargaDDBB0'))
@has_permissions(administrator=True)
async def cargaDDBB(ctx):
    global miembrosNoBot
    conexion = sqlite3.connect("usudiscord.db")
    cursor = conexion.cursor()
    for usuario in miembrosNoBot:
        querySelect = "SELECT * FROM usuarios WHERE id='" +str(usuario.id)+"'"
        cursor.execute(querySelect)
        sal = cursor.fetchone()
        if(sal is None):
            query = "INSERT INTO usuarios(id, dinero, nombre) VALUES (" +str(usuario.id) +", 500, '" + usuario.name +"');"
            print(f'{usuario.name}:{usuario.id}')
            print(f'{query}')
            cursor.execute(query)
    conexion.commit()
    conexion.close()

@bot.command(name='usuario', help=os.getenv('ayuda_usuario'))
async def getUsu(ctx, member: discord.Member):    
    conexion = sqlite3.connect("usudiscord.db")
    cursor = conexion.cursor()
    query = "SELECT * FROM usuarios WHERE id='" +str(member.id)+"'"
    print(f'{query}')
    cursor.execute(query)
    res=cursor.fetchone()
    print(f'{res}')
    mensaje = str(res[2]) +" : "+str(res[1])
    await ctx.send(f'{mensaje}')
    
    
    
@bot.command(name="ayuda", description="descripciones de los comandos")
async def help(ctx):
    helptext = "```"
    for command in bot.commands:
        helptext+=f"{command}:{command.help}\n"
    helptext+="```"
    await ctx.send(helptext)
    
    
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    global miembrosNoBot
    for miembro in guild.members:
        if not miembro.bot:
            miembrosNoBot.append(miembro)
            miembrosNoRepe.append(miembro)
    miembros = guild.members
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

bot.run(TOKEN)
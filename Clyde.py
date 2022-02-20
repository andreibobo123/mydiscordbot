##Made by Andrei Bobo##


import discord
from discord import channel
from discord.ext import commands
import asyncio
from discord.ext.commands import Bot
from discord.ext.commands.errors import MemberNotFound, MissingRequiredArgument
import random
import discapty
import youtube_dl
import os


##PREFIX##

bot = commands.Bot(command_prefix=';')

bot = Bot(";")

bot = discord.Client()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=";", intents=intents)

 
##Nu conteaza##
bot.remove_command('help')


##Status##
@bot.event
async def on_ready():
    print("Gata stapane,sunt online")
    await bot.change_presence(activity=discord.Game(name="Pregatit sa fac orice :)"))    



##SPUNE#
@bot.command()
async def say(ctx, *, arg):
    async with ctx.typing():
        permisiuni=discord.Embed(description='Nu poți utiliza această comandă', color=0x3498db)
        authorperms = ctx.author.permissions_in(ctx.channel)
        if authorperms.administrator:
           await ctx.message.delete()
           await asyncio.sleep(0)
           await ctx.send(arg)
        else:
            await ctx.send(embed=permisiuni, delete_after=5)



##CLEAR##
@bot.command()                    
async def clear(ctx, amount = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999): 
    authorperms = ctx.author.permissions_in(ctx.channel)
    permisiuni=discord.Embed(description='Nu poți utiliza această comandă', color=0x3498db)
    d=discord.Embed(description="Gata <:thumbsup:857279203249618944>", color=0x3498db)
    
    if authorperms.administrator:
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed=d, delete_after=2)
    else:
        await ctx.send(embed=permisiuni, delete_after=5)



##Join##
@bot.event
async def on_member_join(member):
    channel=discord.utils.get(member.guild.channels, name='🙋-ɴᴇᴡ-ᴊᴏɪɴᴇᴅ')
    
    embed=discord.Embed(title=f"Bun venit pe **{member.guild.name}** !", description=f"{member.mention} sperăm să te distrezi !", color=0x3498db) 
    embed.set_thumbnail(url=member.avatar_url)
    m = discord.Embed(title=f"Bun venit pe **{member.guild.name}** !", description=f"{member.mention} să ai un timp plăcut <:wave:712185295633907792> !", color=0x3498db)
    m.set_thumbnail(url=member.avatar_url)
    
    await channel.send(embed=embed)

    role=discord.utils.get(member.guild.roles,name="[🤵] PEOPLE")
    await member.add_roles(role)

       
    

##ERORI##
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.message.delete()
        a = discord.Embed(description='Lipsesc argumente !!!',color=discord.Color((0x3498db)))
        await ctx.send(embed=a, delete_after=5)

    if isinstance(error, MemberNotFound):
        await ctx.message.delete()
        b = discord.Embed(description='Nu am putut găsi utilizatorul',color=discord.Color((0x3498db)))
        await ctx.send(embed=b, delete_after=5)



##MEMBER COUNT##
@bot.command(aliases=["mc"])
async def member_count(ctx):
    await ctx.message.delete()
    a=ctx.guild.member_count
    b=discord.Embed(title=f"Membrii in {ctx.guild.name}:",description=a,color=discord.Color((0x3D85C6)))
    await ctx.send(embed=b)



##BAN##
@bot.command(pass_context=True)
async def ban(ctx, member : discord.Member):
    authorperms = ctx.author.permissions_in(ctx.channel)
    ban=discord.Embed(description=f'{member.mention} a fost banat(ă)', color=0x3498db)
    permisiuni=discord.Embed(description='Nu poți utiliza această comandă', color=0x3498db)
    
    if authorperms.administrator:
        await ctx.message.delete()
        await member.ban()
        await ctx.send(embed=ban, delete_after=5)
    else:
        await ctx.message.delete()
        await ctx.send(embed=permisiuni, delete_after=5)



##UNBAN##
@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    authorperms = ctx.author.permissions_in(ctx.channel)
    permisiuni=discord.Embed(description='Nu poți utiliza această comandă', color=0x3498db)
    
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            if authorperms.administrator:
              await ctx.guild.unban(user)
              
              a=discord.Embed(description=f'Unbanned {user.mention}', color=0x3498db)
              
              await ctx.send(embed=a, delete_after=5)
            
            else:
              await ctx.send(embed=permisiuni, delete_after=5)



##KICK##
@bot.command()
async def kick(ctx, *, member: discord.Member):
    authorperms = ctx.author.permissions_in(ctx.channel)
    m = discord.Embed(description=f"{member.mention} a fost dat(ă) afară", color=0x3498db)
    permisiuni=discord.Embed(description='Nu poți utiliza această comandă', color=0x3498db)
    
    if authorperms.administrator:
        await member.kick()
        await ctx.message.delete()
        await ctx.send(embed=m, delete_after=5)
        await member.send(f"Ai fost dat(ă) afară din {member.guild.name}.")
    else:
        await ctx.message.delete()
        await ctx.send(embed=permisiuni, delete_after=5)


   

##EMBED##
@bot.command(aliases=['embed'])
async def make_embed(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    
    t=discord.Embed(description='Titlul ...', color=0x3498db)
    await ctx.send(embed=t, delete_after=5)
    title = await bot.wait_for('message', check=check)
    
    
    d=discord.Embed(description='Descrierea ...', color=0x3498db)
    await ctx.send(embed=d, delete_after=5)
    desc = await bot.wait_for('message', check=check)
    
    
    embed = discord.Embed(title=title.content, description=desc.content, color=0x3498db)
    await ctx.send(embed=embed)



##Mute##
@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)   

    authorperms = ctx.author.permissions_in(ctx.channel)

    if authorperms.administrator:
        await ctx.message.delete()
        embed = discord.Embed(description=f"{member.mention} a fost amuțit(ă)", colour=0x3498db)
        embed.add_field(name="Motiv:", value=reason, inline=False)
        await ctx.send(embed=embed, delete_after=5)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f" Ai fost amuțit(ă) din **{guild.name}** , motiv: **{reason}**")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)   

    else:
        permisiuni=discord.Embed(description='Nu poți utiliza această comandă', color=0x3498db)
        await ctx.send(embed=permisiuni, delete_after=5)



##UNMUTE##
@bot.command()
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   authorperms = ctx.author.permissions_in(ctx.channel)

   if authorperms.administrator:
        await ctx.message.delete()
        await member.remove_roles(mutedRole)
        await member.send(f"Ai fost dezamuțit(ă) din {ctx.guild.name}")
        embed = discord.Embed(description=f" Unmuted {member.mention}",color=0x3498db)
        await ctx.send(embed=embed, delete_after=5)
   
   else:
        await ctx.message.delete()
        permisiuni=discord.Embed(description='Nu poți utiliza această comandă', color=0x3498db)
        await ctx.send(embed=permisiuni, delete_after=5)



##Muzica##
@bot.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
         
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")






##BOT TOKEN##
bot.run ("")
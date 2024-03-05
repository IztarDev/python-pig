from dis import disco
from email import message
from enum import member
from http import client
from xmlrpc.client import boolean
import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from config import TOKEN
from email.message import EmailMessage

bot = commands.Bot(command_prefix='--', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Succesfully logued in: {bot.user.name} [{bot.user.id}]')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)








@bot.tree.command(name="ping", description='Prueba la latencia del bot')
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(
        colour=discord.Colour.purple(),
        title='Pong 🏓',
        description=f'Latencia: `{format(round(bot.latency, 2))} ms`'
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
@bot.tree.command(name="verify_user", description='Asigna el rol de verificado a un usuario')
async def ping(interaction: discord.Interaction, member: discord.Member):
    verified = discord.utils.get(interaction.guild.roles, name="[⭕] Verified")
    unverified = discord.utils.get(interaction.guild.roles, name="[❌] Unverified")

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('No tienes permisos para ejecutar este comando', ephemeral=True)
        return
        
    if verified is None:
        await interaction.response.send_message('Error interno: rol no encontrado', ephemeral=True)
        return
    
    if unverified is None:
        await interaction.response.send_message('Error interno: rol no encontrado', ephemeral=True)
        return
    
    await member.add_roles(verified)
    await member.remove_roles(unverified)
    
    embed = discord.Embed(
        colour=discord.Colour.orange(),
        title='Miembro verificado correctamente',
        description=f'El usuario [{member.display_name}] ha sido verificado correctamente'
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="exit", description='NO USAR')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Exit...', ephemeral=True)
    exit()

@bot.tree.command(name="clear_verify", description='Limpia los mensajes del canal de verificacion')
async def clear(interaction: discord.Interaction):
    verify_channel = discord.utils.get(interaction.guild.channels, name='⌚・verificacion')
    #keep = verify_channel.fetch_message(1214406800712138802)
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('No tienes permisos para ejecutar este comando', ephemeral=True)
        return
    
    if verify_channel is None:
        await interaction.response.send_message('Error interno: canal no encontrado', ephemeral=True)
        return
    
    try:
        keep_message = await verify_channel.fetch_message(1214406800712138802)
    except discord.NotFound:
        await interaction.response.send_message('Error interno: mensaje no encontrado', ephemeral=True)
        return
    
    deleted_messages = await verify_channel.purge(check=lambda m: m.id != keep_message.id)

    embed = discord.Embed(
        colour=discord.Colour.orange(),
        title='Canal de verificaciones limpiado correctamente',
        description=f'Se han eliminado {len(deleted_messages)} mensajes, excepto el de instrucciones'
    )
    await verify_channel.send(embed=embed)
    
@bot.tree.command(name="cuarentena", description='Envia o saca a un miembro de cuarentena')
async def cuarentena(interaction: discord.Interaction, member: discord.Member):
    verified = discord.utils.get(interaction.guild.roles, name="[⭕] Verified")
    unverified = discord.utils.get(interaction.guild.roles, name="[❌] Unverified")
    cuarentena = discord.utils.get(interaction.guild.roles, name="[🦴] Cuarentena")
    
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message('No tienes permisos para ejecutar este comando', ephemeral=True)
        return
    
    if cuarentena is None:
        await interaction.response.send_message('Error interno: rol no encontrado', ephemeral=True)
        return
    
    if verified is None:
        await interaction.response.send_message('Error interno: rol no encontrado', ephemeral=True)
        return
    
    if unverified is None:
        await interaction.response.send_message('Error interno: rol no encontrado', ephemeral=True)
        return
    
    if cuarentena in member.roles:
        await member.add_roles(verified)
        await member.remove_roles(cuarentena)
            
        embed = discord.Embed(
            colour=discord.Colour.orange(),
            title='Miembro removido de cuarentena',
            description=f'El usuario [{member.display_name}] ha sido removido de cuarentena correctamente'
        )
        
        await interaction.response.send_message(embed=embed)
    else:
        await member.remove_roles(verified)
        await member.add_roles(cuarentena)
        if unverified in member.roles:
            await member.remove_roles(unverified)
        
        embed = discord.Embed(
            colour=discord.Colour.orange(),
            title='Miembro enviado a cuarentena',
            description=f'El usuario [{member.display_name}] ha sido enviado a cuarentena correctamente'
        )
        
        await interaction.response.send_message(embed=embed)
        






    
@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send('Synced')

bot.run(TOKEN)
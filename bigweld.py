# ID: 563856842153918474

import discord
import datetime
import csv



def read_cfg(idx):
    with open("bigweld.cfg", "r") as t:
        lines = t.readlines()
        return lines[idx].strip()



def bigwritelog():
    with open("biglog.txt", "a+") as t:
        t.write(log)


def get_command(cmd):
    cmdnoprefix = cmd[len(prefix):].split(' ', 1)[0]
    return cmdnoprefix


def biglog(logentry):
    global log
    log += logentry
    print(logentry)



# Config loading stuff:

log = ""

prefix = read_cfg(3) + " "
token = read_cfg(1)
img_judgement =  discord.File("resources/crow of judgement.jpg", filename="crow of judgement.jpg")
img_wow =  discord.File("resources/wow.gif", filename="wow.gif")
cmd_channels = ["bigwelds-workshop"]

help_embed = discord.Embed()
help_embed.description = "```diff\n- The basics:\n\n  To issue a command begin with the prefix 'big'.\n  Follow this prefix with the command you'd like to use.\n  For example: 'big judgement'\n```"
help_embed.description += "```diff\n- big help\n  The help command provides information about bigweld.\n\n  Usage:\n- big help```"
help_embed.description += "```diff\n- big say\n  The say command makes Bigweld say whatever you want.\n\n  Usage:\n- big say [text]```"
help_embed.description += "```diff\n- big yell\n  The yell command makes Bigweld tag @everyone with a message of your choosing.\n\n  Usage:\n- big yell [text]```"
help_embed.description += "```diff\n- big judgement\n  Bigweld judges you.\n\n  Usage:\n- big judgement```"
help_embed.title = "big help"

client = discord.Client()

@client.event
async def on_message(message):
    content = message.content
    channel = message.channel
    user = message.author.display_name
    userID = message.author.id
    try:
        command = get_command(content)
    except:
        pass
    
    if str(message.channel) in cmd_channels:
        if content.startswith(prefix) and userID != 563856842153918474:
            biglog("Time:   " + str(datetime.datetime.now()) + "\nUser:   " + user + " (" + str(userID) + ")\nTried:  " + command + "\n\n")
            
            
            
            if command == "help":
                #await channel.send(embed=help_embed)
                await channel.send(help_embed.description)
            


            elif command == "say":
                await message.delete()
                await channel.send(content[7:])



            elif command == "yell":
                await message.delete()
                yellphrase = "@everyone: \n" + content[8:].upper()
                await channel.send(yellphrase)



            elif command == "judgement":
                await message.delete()
                await channel.send(user + " has judged you.",file=img_judgement)
            elif command == "wow":
                await channel.send(file=img_wow)
            


            elif command == "stop":
                bigwritelog()



            else:
                await channel.send("Sorry, I didn't quite catch that.  Please try a supported command.")

client.run(token)


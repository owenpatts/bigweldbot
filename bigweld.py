# ID: 563856842153918474

import discord
import datetime
import csv
import asyncio



def read_cfg(idx):
    with open("bigweld.cfg", "r") as t:
        lines = t.readlines()
        return lines[idx].strip()

'''
All of my CSV handling functions:
'''

# Returns a 2D array of strings from a csv file.  Spaces are the default delimiter.
def ret2dfromcsv(filename, delim=' '):
    with open(filename, newline='') as csvfile:
        read = csv.reader(csvfile, delimiter=delim)
        out = []
        for row in read:
            out.append(row)
    return out

# Returns a nicely formatted string representing a 2D list
def retcsvfrom2d(givenlist):
    out = ""
    for row in givenlist:
        for value in row:
            out += value + " "
        out = out
        out += "\n"
    return out


def useradd(usertag, users):
    initinfo = [usertag, '0', '0']
    if not any(usertag in sublist for sublist in users):
        users.append(initinfo)
    return users


def bigwritelog():
    with open("biglog.txt", "a+") as t:
        t.write(log)


def get_command(message):
    cmdnoprefix = message[len(prefix):].split(' ', 1)[0]
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
usercsv = ret2dfromcsv('bigusers.csv')


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
    usertag = str(message.author.name)  + "#" + str(message.author.discriminator)
    userID = message.author.id
    csvfile = useradd(usertag, usercsv)

    try:
        command = get_command(content)
    except:
        pass
    
    if str(message.channel) in cmd_channels:
        if content.startswith(prefix) and userID != 563856842153918474:
            biglog(str(datetime.datetime.now()) + " : " + usertag + " (" + str(userID) + ") Tried '" + command + "'\n")
            
            
            
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


async def update():
    await client.wait_until_ready()
    global usercsv, log
    while not client.is_closed():
        try:
            with open("bigusers.csv", "w") as t:
                t.write(retcsvfrom2d(usercsv))
            await asyncio.sleep(10)
        except Exception as e:
            print(e)
        try:
            with open("biglog.txt", "a") as t:
                t.write(log)
            log = ""
        except Exception as e:
            print(e)


client.loop.create_task(update())
client.run(token)


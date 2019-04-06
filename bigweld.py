# ID: 563856842153918474

import discord
import datetime
import csv
import asyncio
import os

'''
GENERAL INFORMATION:


bigusers.csv indexing:

    [0] = username
    [1] = messages sent
    [2] = commands sent
    [3] = youtube links sent
    [4] = twitch clips sent
    [5] = ...

'''

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


def sentmsg(usertag, users):
    initinfo = [usertag, '1', '0', '0', '0']
    if not any(usertag in sublist for sublist in users):
        users.append(initinfo)
    else:
        for i in users:
            if i[0] == usertag:
                i[1] = str(int(i[1]) + 1)
                break
    return users


def sentcmd(usertag, users):
    for i in users:
        if i[0] == usertag:
            i[2] = str(int(i[2]) + 1)
    return users


def sentyt(usertag, users):
    for i in users:
        if i[0] == usertag:
            i[3] = str(int(i[3]) + 1)
    return users


def senttwitch(usertag, users):
    for i in users:
        if i[0] == usertag:
            i[4] = str(int(i[4]) + 1)
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


def bigchatlog(server, channel, user, message):
    fileloc = "logs/" + server
    filename = "logs/" + server + "/" + channel + ".txt"
    if not os.path.exists(fileloc):
        os.makedirs(fileloc)    
    with open(filename, "a") as t:
       t.write(str(datetime.datetime.now()) + " ["+ user + "] " + message + "\n")




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

    csvfile = sentmsg(usertag, usercsv)
    bigchatlog(message.guild.name, message.channel.name, usertag, content)

    try:
        command = get_command(content)
    except:
        pass
    
    if str(message.channel) in cmd_channels:
        if content.startswith(prefix) and userID != 563856842153918474:

            
            # Creates log message that looks like:
            # 2019-04-06 18:26:56.091928 : User#1234 (1234567891234) Tried 'stats in @server#channel
            biglog(str(datetime.datetime.now()) + " : " + usertag + " (" + str(userID) + ") Tried '" + command + " in @" + message.guild.name + "#" + message.channel.name + "\n")
            
            
            
            if command == "help":
                #await channel.send(embed=help_embed)
                await channel.send(help_embed.description)
                sentcmd(usertag, usercsv)
            


            elif command == "say":
                await message.delete()
                await channel.send(content[7:])
                sentcmd(usertag, usercsv)



            elif command == "yell":
                await message.delete()
                yellphrase = "@everyone: \n" + content[8:].upper()
                await channel.send(yellphrase)
                sentcmd(usertag, usercsv)



            elif command == "judgement":
                await message.delete()
                await channel.send(user + " has judged you.",file=img_judgement)
                sentcmd(usertag, usercsv)
            elif command == "wow":
                await channel.send(file=img_wow)
                sentcmd(usertag, usercsv)
            


            elif command == "stop":
                bigwritelog()
                sentcmd(usertag, usercsv)


            elif command == "stats":
                sentcmd(usertag, usercsv)
                try:
                    user = content.split(' ')[2]
                    found = False
                    for i in usercsv:
                        if i[0] == user:
                            found = True
                            msgct = i[1]
                            cmdct = i[2]
                            ytct = i[3]
                            twct = i[4]
                    if found:
                        await channel.send("```"+ user.split("#")[0] + " has sent:\n" + msgct + " messages\n" + cmdct + " commands\n" + ytct + " youtube videos & \n" + twct + " twitch clips```")

                    else:
                        if "#" in user:
                            await channel.send("I couldn't find any stats for ``" + user + "``. Make sure you've used proper capitalization")
                        else:
                            await channel.send("You need to give me the full user tag.\n```diff\n- Usage: big user [user#1234]```")

                except:
                    await channel.send("That wasn't quite what I was expecting.\n```diff\n- Usage: big user [user#1234]```")


            else:
                await channel.send("Sorry, I didn't quite catch that.  Please try a supported command.")
        else:
            if "youtube.com" in content or "youtu.be" in content:
                sentyt(usertag, usercsv)
            elif "clips.twitch.tv" in content:
                senttwitch(usertag, usercsv)


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


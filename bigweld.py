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
cmd_channels = ["bigwelds-workshop", "goo-lagoon", "the-chum-bucket", "glove-world"]
usercsv = ret2dfromcsv('bigusers.csv')


help_list = []
help_list.append("```diff\n"\
            "- [PAGE 0?]\n"
            "\n"\
            "- Hi, I'm Bigweld.\n"\
            "= To issue a command just start your message with 'big'.\n"\
            "= Follow that with the command you'd like to use, such as 'help'.\n"\
            "= Finally, add any additional arguments to the command, like '1'.\n"\
            "= Try it with me!  Type the following to see the next page:\n"\
            "- big help 1\n"\
            "\n"\
            "- [PAGE 0?]```")

help_cmds = ["help", "say", "yell", "vote"]
help_idxs = [1,       1,     1,      2]
help_list.append("```diff\n"\
            "- [PAGE 1]\n"\
            "\n"\
            "=======================================\n"\
            "\n"\
            "- help\n"\
            "= For help with bigweld.\n"\
            "= Args: [1-x]/[command] (Manual number / command name)\n"\
            "- Usage: 'big help [page]'\n"\
            "\n"\
            "=======================================\n"\
            "\n"\
            "- say\n"\
            "= Make Bigweld say things!\n"\
            "- Usage: 'big say [message]'\n"\
            "\n"\
            "=======================================\n"\
            "\n"\
            "- yell\n"\
            "= Bigweld will YELL AT EVERYONE.\n"\
            "= Use with caution, this one can be annoying.\n"\
            "- Usage: 'big yell [message]'\n"\
            "\n"\
            "=======================================\n"\
            "\n"\
            "- [PAGE 1]```")

help_list.append("```diff\n"\
            "- [PAGE 2]\n"\
            "\n"\
            "=======================================\n"\
            "\n"\
            "- vote\n"\
            "= Bigweld will hold a vote, tagging any online members.\n"\
            "= Upvote and downvote reactions can be added to this vote.\n"\
            "\n"\
            "= Flags: (optional)\n"\
            "=        -AB: Will add A/B buttons instead of upvotes/downvotes.\n"\
            "=        -UD: Will add the usual up/downvotes.\n"\
            "\n"\
            "- Usage: 'big vote [flag] [question]'\n"\
            "\n"\
            "=======================================\n"\
            "\n"\
            "- [PAGE 2]```")


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
    
    if usertag == "stronius445#3341":
        await message.add_reaction(emoji=":pepehands:482720136105689088")
    
    if str(message.channel) in cmd_channels:
        if content.startswith(prefix) and userID != 563856842153918474:


            # Creates log message that looks like:
            # 2019-04-06 18:26:56.091928 : User#1234 (1234567891234) Tried 'stats in @server#channel
            biglog(str(datetime.datetime.now()) + " : " + usertag + " (" + str(userID) + ") Tried '" + command + " in #" + message.channel.name + "\n")
            
            
            
            if command == "help":
                try:
                    if content.split(" ")[2] in help_cmds:
                        for idx, i in enumerate(help_cmds):
                            if content.split(" ")[2] == i:
                                await channel.send(help_list[help_idxs[idx]])
                    else:
                        option = content.split(" ")[2]
                        await channel.send(help_list[int(option)])
                except:
                    await channel.send(help_list[0])
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
            elif command == "panic":
                await message.delete()
                await channel.send("<a:eyesshaking:562348528266117140>")
                sentcmd(usertag, usercsv)


            elif command == "vote":
                try:
                    await message.delete()
                    if content.split(" ")[2] == "-AB":
                        await channel.send("@here \n\n``" + user + "`` wants you to vote: ```" + content[12:] + "```")
                        msg = await channel.history().get(author__name='Bigweld')
                        await msg.add_reaction(emoji=":option_a:564275696323657747")
                        await msg.add_reaction(emoji=":option_b:564275696403349504")
                    elif content.split(" ")[2] == "-UD":
                        await channel.send("@here \n\n``" + user + "`` wants you to vote: ```" + content[12:] + "```")
                        msg = await channel.history().get(author__name='Bigweld')
                        await msg.add_reaction(emoji=":upvote:564261745921884190")
                        await msg.add_reaction(emoji=":downvote:564261745502453772")
                    else:
                        await channel.send("@here \n\n``" + user + "`` wants you to vote: ```" + content[8:] + "```")
                        msg = await channel.history().get(author__name='Bigweld')
                        await msg.add_reaction(emoji=":upvote:564261745921884190")
                        await msg.add_reaction(emoji=":downvote:564261745502453772")
                except:
                    await channel.send("**Sorry, I didn't quite get that. Try 'big help vote'**")
            


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


import asyncio
from pyrogram import filters
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from pyrogram.errors import RPCError

@friday_on_cmd(
    ["stealmedia"],
    cmd_help={
        "help": "Steal all from one chat to other chat in groups \n .stealmedia fromchat | to chat | msg id | none for no limits | reverse (optional) \nNote: | is essential",
        "example": "{ch}stealmedia @fridaysupportofficial | @fridaychat | 100 | 10 | reverse\n",
    },
)
async def stealmedia(client, message):
    lol = await edit_or_reply(message, "Processing please wait")
    x = get_text(message)
    x=x.replace(" ","")
    try:
       fromchat, tochat, idmsg, limit, reverse = x.split("|")
       if reverse == "reverse":
           reverse = True
       else:
           reverse = False
    except:
        try:
           fromchat, tochat, idmsg, limit = x.split("|")
           reverse = False
        except:
            await lol.edit("Check command syntax")
    try:
        fromchat =int(fromchat)
    except:
        if not (fromchat.startswith("@")):
            await lol.edit("Enter a vailed username or id")
            return
    try:
        tochat = int(tochat)
    except:
        if not (tochat.startswith("@")):
            await lol.edit("Enter a vailed username or id")
            return
    try:
        idmsg = int(idmsg)
    except:
        await lol.edit("Enter a msg id")
        return

    a =0
    album=[]
    typemedia = 0
    temp = 0
    last = 0
    if limit == "None" or limit == "none":
        try:
            async for message in client.iter_history(fromchat, offset_id=idmsg, reverse=reverse):
              try:
                await message.copy(tochat)
                a=a+1
              except Exception as e:
                await lol.edit(e)
                pass
              except RPCError as i:
                await lol.edit(i)
                pass              
              await asyncio.sleep(1)
            await lol.edit(f"Successfully shifted {a} messages from {fromchat} to {tochat}")
        except RPCError as i:
            await lol.edit(i)
            return
    else:
        try:
            limit = int(limit)
        except:
            lol.edit("Enter a vailed limit")
            return
        try:
            async for message in client.iter_history(fromchat, offset_id=idmsg,  limit = limit,reverse=reverse):
                try:
                    ###########################
                    if message.photo:
                        typemedia = 1
                    else:
                        typemedia = 2

                    if last == 0:
                        last = typemedia
                        album.append(message)
                        temp = message
                        a = a+1
                    else:
                        if last == typemedia:
                            if len(album) < 10:
                                album.append(message)
                                temp = message
                                a = a+1
                            else:
                                await client.send_media_group(tochat, album)
                                await asyncio.sleep(1)
                                album.clear()
                                album.append(message)
                                temp = message
                                a = a+1
                        else:
                            if len(album) >= 2:
                                await client.send_media_group(tochat, album)
                                await asyncio.sleep(1)
                                album.clear()
                                album.append(message)
                                temp = message
                                a = a+1
                                last = typemedia
                            else:
                                pass
#                                client.copy_message(tochat, temp)

                    ###########################
                except Exception as e:
                  await lol.edit(e)
                  pass
                except RPCError as i:
                  await lol.edit(i)
                  pass   
                await asyncio.sleep(1)
            await lol.edit(f"Successfully shifted {a} messages from {fromchat} to {tochat}")
        except RPCError as i:
            await lol.edit(i)
            return
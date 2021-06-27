import asyncio
import time
from pyrogram import filters
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from pyrogram.errors import RPCError
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio

@friday_on_cmd(
    ["stealmedia"],
    cmd_help={
        "help": "Backup all from one chat/channel to other chat/channel \n .stealmedia fromchat | to chat | msgid (Optional to resume) \nNote: | is essential",
        "example": "{ch}stealmedia @fridaysupportofficial | @fridaychat | 1600\n For private groups/channels add -100",
    },
)

async def stealmedia(client, message):
    lol = await edit_or_reply(message, "Processing please wait")
    x = get_text(message)
    x=x.replace(" ","")
    try:
        fromchat, tochat, msgid = x.split("|")
    except:
        try:
            fromchat, tochat = x.split("|")
            msgid = 0
        except:
            await lol.edit("Check command syntax")

    try:
        fromchat =int(fromchat)
        idlink = str(fromchat)
        idlink = idlink.split("-100")
        idlink = "t.me/c/" + idlink[1]
    except:
        idlink = fromchat.split("@")
        idlink = "t.me/" + idlink[1]
        if not (fromchat.startswith("@")):
            await lol.edit("Enter a vailed username or id")
            return
    try:
        tochat = int(tochat)
    except:
        if not (tochat.startswith("@")):
            await lol.edit("Enter a vailed username or id")
            return

        
    
    def isbotonera(message):
        if message.entities:
            url = 0
            for MessageEntity in message.entities:
                if MessageEntity.type == "text_link":
                    url+=1
            if url > 3:
                return True

    a = 0
    album=[]
    mediagid = 0
    lastmsgid = 0
    boto = 0 
    if msgid == 0:
        try:
            async for message in client.iter_history(fromchat, reverse=True):
                try:
                    if isbotonera(message):
                        boto +=1
                        continue

                    lastmsgid = message.message_id
                    if message.media_group_id is None:
                        a+=1
                        if album:
                            await client.send_media_group(tochat, album)
                            album.clear()
                        await message.copy(tochat)
                    else:
                        a+=1

                        if message.caption is None:
                            captionalbum=""
                        else:
                            captionalbum= message.caption
    
                        if album == []:
                            if message.photo:
                                if isinstance(message.photo, list):
                                    album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                            elif message.document:
                                if isinstance(message.document, list):
                                    album.append(InputMediaDocument(message.document[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaDocument(message.document.file_id, caption=captionalbum))
                            elif message.video:
                                if isinstance(message.video, list):
                                    album.append(InputMediaVideo(message.video[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaVideo(message.video.file_id, caption=captionalbum))
                            else:
                                if isinstance(message.audio, list):
                                    album.append(InputMediaAudio(message.audio[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaAudio(message.audio.file_id, caption=captionalbum))
                            mediagid = message.media_group_id
                        else:
                            if mediagid == message.media_group_id:
                                if message.photo:
                                    if isinstance(message.photo, list):
                                        album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                                elif message.document:
                                    if isinstance(message.document, list):
                                        album.append(InputMediaDocument(message.document[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaDocument(message.document.file_id, caption=captionalbum))
                                elif message.video:
                                    if isinstance(message.video, list):
                                        album.append(InputMediaVideo(message.video[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaVideo(message.video.file_id, caption=captionalbum))
                                else:
                                    if isinstance(message.audio, list):
                                        album.append(InputMediaAudio(message.audio[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaAudio(message.audio.file_id, caption=captionalbum))
                            else:
                                await client.send_media_group(tochat, album)
                                mediagid = message.media_group_id
                                album.clear()
                                if message.photo:
                                    if isinstance(message.photo, list):
                                        album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                                elif message.document:
                                    if isinstance(message.document, list):
                                        album.append(InputMediaDocument(message.document[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaDocument(message.document.file_id, caption=captionalbum))
                                elif message.video:
                                    if isinstance(message.video, list):
                                        album.append(InputMediaVideo(message.video[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaVideo(message.video.file_id, caption=captionalbum))
                                else:
                                    if isinstance(message.audio, list):
                                        album.append(InputMediaAudio(message.audio[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaAudio(message.audio.file_id, caption=captionalbum))
                except Exception as e:
                    try:
                        if "[420 FLOOD_WAIT_X]" in str(e):
                            print('Flood: Wait for', int(str(e).split()[5]), 'seconds')
                            time.sleep(int(str(e).split()[5]))
                            await lol.edit(f"Flood wait please. Last post: {lastmsgid}")
                    except:
                        await lol.edit(e)
                    pass
                except RPCError as i:
                  await lol.edit(i)
                  pass
                await asyncio.sleep(1)
            if album:
                await client.send_media_group(tochat, album) 
            await lol.edit(f"Successfully shifted {a} messages from {fromchat} to {tochat}. Last post: {idlink}/{lastmsgid}. {boto} keypad omitted.")
        except RPCError as i:
            # await lol.edit(i)
            return
    else:
        try:
            msgid = int(msgid)
        except:
            await lol.edit("Enter a msg id valid")
            return
        try:
            async for message in client.iter_history(fromchat, offset_id=msgid, reverse=True):
                try:
                    if isbotonera(message):
                        boto +=1
                        continue
                    lastmsgid = message.message_id
                    if message.media_group_id is None:
                        a+=1
                        if album:
                            await client.send_media_group(tochat, album)
                            album.clear()
                        await message.copy(tochat)
                    else:
                        a+=1
                        if message.caption is None:
                            captionalbum=""
                        else:
                            captionalbum= message.caption
    
                        if album == []:
                            if message.photo:
                                if isinstance(message.photo, list):
                                    album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                            elif message.document:
                                if isinstance(message.document, list):
                                    album.append(InputMediaDocument(message.document[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaDocument(message.document.file_id, caption=captionalbum))
                            elif message.video:
                                if isinstance(message.video, list):
                                    album.append(InputMediaVideo(message.video[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaVideo(message.video.file_id, caption=captionalbum))
                            else:
                                if isinstance(message.audio, list):
                                    album.append(InputMediaAudio(message.audio[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaAudio(message.audio.file_id, caption=captionalbum))
                            mediagid = message.media_group_id
                        else:
                            if mediagid == message.media_group_id:
                                if message.photo:
                                    if isinstance(message.photo, list):
                                        album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                                elif message.document:
                                    if isinstance(message.document, list):
                                        album.append(InputMediaDocument(message.document[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaDocument(message.document.file_id, caption=captionalbum))
                                elif message.video:
                                    if isinstance(message.video, list):
                                        album.append(InputMediaVideo(message.video[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaVideo(message.video.file_id, caption=captionalbum))
                                else:
                                    if isinstance(message.audio, list):
                                        album.append(InputMediaAudio(message.audio[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaAudio(message.audio.file_id, caption=captionalbum))
                            else:
                                await client.send_media_group(tochat, album)
                                mediagid = message.media_group_id
                                album.clear()
                                if message.photo:
                                    if isinstance(message.photo, list):
                                        album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                                elif message.document:
                                    if isinstance(message.document, list):
                                        album.append(InputMediaDocument(message.document[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaDocument(message.document.file_id, caption=captionalbum))
                                elif message.video:
                                    if isinstance(message.video, list):
                                        album.append(InputMediaVideo(message.video[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaVideo(message.video.file_id, caption=captionalbum))
                                else:
                                    if isinstance(message.audio, list):
                                        album.append(InputMediaAudio(message.audio[-1].file_id, caption=captionalbum))
                                    else:
                                        album.append(InputMediaAudio(message.audio.file_id, caption=captionalbum))

                except Exception as e:
                    try:
                        if "[420 FLOOD_WAIT_X]" in str(e):
                            print('Flood: Wait for', int(str(e).split()[5]), 'seconds')
                            time.sleep(int(str(e).split()[5]))
                            await lol.edit(f"Flood wait please. Last post: {lastmsgid}")
                    except:
                        await lol.edit(e)
                    pass
                except RPCError as i:
                  await lol.edit(i)
                  pass
                await asyncio.sleep(1)
            if album:
                await client.send_media_group(tochat, album)
            await lol.edit(f"Successfully shifted {a} messages from {fromchat} to {tochat}. Last post: {idlink}/{lastmsgid}. {boto} keypad omitted.")
        except RPCError as i:
            # await lol.edit(i)
            return


@friday_on_cmd(
    ["stealimage"],
    cmd_help={
        "help": "Steal all images from one chat/channel to other chat/channel as an album  \n .stealimage fromchat | to chat | msgid (Optional to resume) | #images per album (Optional. # is essential) \nNote: | is essential",
        "example": "{ch}stealimage @fridaysupportofficial | @fridaychat | 1600 | # \n For private groups/channels add -100",
    },
)

async def stealimage(client, message):
    lol = await edit_or_reply(message, "Processing please wait")
    x = get_text(message)
    x=x.replace(" ","")
    try:
        fromchat, tochat, msgid, quantity = x.split("|")
        w = 4
        try:
            if (quantity.startswith("#")):
                q = quantity.split("#")
                q = int(q.pop())
        except:
            if not (quantity.startswith("#")):
                await lol.edit("Enter a number beetwen 2-10 eg. #4")
                return
    except:
        try:
            fromchat, tochat, msgid = x.split("|")
            w = 3
        except:
            try:
                fromchat, tochat = x.split("|")
                w = 2
                msgid = 0
                q = 10
            except:
                await lol.edit("Check command syntax")

    try:
        fromchat =int(fromchat)
        idlink = str(fromchat)
        idlink = idlink.split("-100")
        idlink = "t.me/c/" + idlink[1]
    except:
        idlink = fromchat.split("@")
        idlink = "t.me/" + idlink[1]
        if not (fromchat.startswith("@")):
            await lol.edit("Enter a vailed username or id")
            return
    try:
        tochat = int(tochat)
    except:
        if not (tochat.startswith("@")):
            await lol.edit("Enter a vailed username or id")
            return

    if w == 3:
        try:
            if (msgid.startswith("#")):
                q = msgid.split("#")
                q = int(q.pop())
                msgid = 0
        except:
            try:
                msgid = int(msgid)
                q = 10
            except:
                if not (msg.startswith("#")):
                    await lol.edit("Enter a msg id valor or #(2-10) for no. images per album")
    elif w == 4:
        try:
            msgid = int(msgid)
        except:
            await lol.edit("Enter a msg id valid")
            return
########################################

  #  if not int(fromchat):
    #    if (fromchat.startswith("@")):
   #     idlink = fromchat.split("@")
    #    idlink = "t.me/" + idlink[1]
########################################

    def isbotonera(message):
        if message.entities:
            url = 0
            for MessageEntity in message.entities:
                if MessageEntity.type == "text_link":
                    url+=1
            if url > 3:
                return True

    a = 0
    album=[]
    album2=[]
    mediagid = 0
    lastmsgid = 0 
    boto  = 0
    if msgid == 0:
        try:
            async for message in client.iter_history(fromchat, reverse=True):
                try:
                    if isbotonera(message):
                        boto +=1
                        continue

                    lastmsgid = message.message_id
                        ########################
                    if message.caption is None:
                        captionalbum=""
                    else:
                        captionalbum= message.caption 

                    if message.photo:
                        a+=1
                        if message.media_group_id is None:
                            if album2:
                                await client.send_media_group(tochat, album2)
                                await asyncio.sleep(1)
                                album2.clear()

                            if len(album) < q:
                                if isinstance(message.photo, list):
                                    album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                            else:
                                await client.send_media_group(tochat, album)
                                await asyncio.sleep(1)
                                album.clear()

                                if isinstance(message.photo, list):
                                    album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))                                
                        else:
                            if len(album) > 1:
                                await client.send_media_group(tochat, album)
                                await asyncio.sleep(1)
                                album.clear()
                            if album2 == []:
                                if isinstance(message.photo, list):
                                    album2.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                else:
                                    album2.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                                mediagid = message.media_group_id
                            else:
                                if mediagid == message.media_group_id:
                                    if isinstance(message.photo, list):
                                        album2.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                    else:
                                        album2.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                                else:
                                    await client.send_media_group(tochat, album2)
                                    await asyncio.sleep(1)
                                    mediagid = message.media_group_id
                                    album2.clear()

                                    if isinstance(message.photo, list):
                                        album2.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                    else:
                                        album2.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))                                
                    ########################
                except Exception as e:
                    try:
                        if "[420 FLOOD_WAIT_X]" in str(e):
                            print('Flood: Wait for', int(str(e).split()[5]), 'seconds')
                            time.sleep(int(str(e).split()[5]))
                            await lol.edit(f"Flood wait please. Last post: {lastmsgid}")
                    except:
                        await lol.edit(e)
                    pass
                except RPCError as i:
                    await lol.edit(i)
                    pass      

            if len(album) > 1:
                await client.send_media_group(tochat, album)

            if album2:
                await client.send_media_group(tochat, album2)
            await lol.edit(f"Successfully shifted {a} messages from {fromchat} to {tochat}. Last post: {idlink}/{lastmsgid}. {boto} keypad omitted.")
        except RPCError as i:
            await lol.edit(i)
            return
    else:
        try:
            async for message in client.iter_history(fromchat, offset_id=msgid, reverse=True):
                try:
                    if isbotonera(message):
                        boto +=1
                        continue

                    lastmsgid = message.message_id
                        ########################
                    if message.caption is None:
                        captionalbum=""
                    else:
                        captionalbum= message.caption 

                    if message.photo:
                        a+=1
                        if message.media_group_id is None:
                            if album2:
                                await client.send_media_group(tochat, album2)
                                await asyncio.sleep(1)
                                album2.clear()

                            if len(album) < q:
                                if isinstance(message.photo, list):
                                    album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                            else:
                                await client.send_media_group(tochat, album)
                                await asyncio.sleep(1)
                                album.clear()

                                if isinstance(message.photo, list):
                                    album.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                else:
                                    album.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))                                
                        else:
                            if len(album) > 1:
                                await client.send_media_group(tochat, album)
                                await asyncio.sleep(1)
                                album.clear()
                            if album2 == []:
                                if isinstance(message.photo, list):
                                    album2.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                else:
                                    album2.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                                mediagid = message.media_group_id
                            else:
                                if mediagid == message.media_group_id:
                                    if isinstance(message.photo, list):
                                        album2.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                    else:
                                        album2.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                                else:
                                    await client.send_media_group(tochat, album2)
                                    await asyncio.sleep(1)
                                    mediagid = message.media_group_id
                                    album2.clear()

                                    if isinstance(message.photo, list):
                                        album2.append(InputMediaPhoto(message.photo[-1].file_id, caption=captionalbum))
                                    else:
                                        album2.append(InputMediaPhoto(message.photo.file_id, caption=captionalbum))
                        #####################################################3
                except Exception as e:
                    try:
                        if "[420 FLOOD_WAIT_X]" in str(e):
                            print('Flood: Wait for', int(str(e).split()[5]), 'seconds')
                            time.sleep(int(str(e).split()[5]))
                            await lol.edit(f"Flood wait please. Last post: {lastmsgid}")
                    except:
                        await lol.edit(e)
                    pass
                except RPCError as i:
                    await lol.edit(i)
                    pass

            if len(album) > 1:
                await client.send_media_group(tochat, album)

            if album2:
                await client.send_media_group(tochat, album2)
            await lol.edit(f"Successfully shifted {a} messages from {fromchat} to {tochat}. Last post: {idlink}/{lastmsgid}. {boto} keypad omitted.")
        except RPCError as i:
            await lol.edit(i)
            return
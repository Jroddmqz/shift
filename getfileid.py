import os
from os import remove
from os import path
import asyncio
from pyrogram import filters
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from pyrogram.errors import RPCError
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio

@friday_on_cmd(
    ["getfileid"],
    cmd_help={
        "help": "Get file_id if message is photo, video, sticker or gif  \n .infomedia https://t.me/Friday_Official/446 ",
        "example": "{ch}infomedia https://t.me/Friday_Official/446 ",
        "example": "{ch}infomedia https://t.me/c/1429362247/446 ",
    },
)

async def getfileid(client, message):
    lol = await edit_or_reply(message, "Processing please wait")
    await asyncio.sleep(2)
    x = get_text(message)
    y = x 

    if lol.reply_to_message:
        fromchat = lol.reply_to_message.chat.id
        msgid = lol.reply_to_message.message_id
        if lol.reply_to_message.forward_from_chat:
            y = "https://t.me/c/" + str(lol.reply_to_message.forward_from_chat.id).split("-100")[1] + "/" + str(lol.reply_to_message.forward_from_message_id)
        else:
            y = lol.reply_to_message.message_id
    else:
        if (x.startswith("https://t.me/c/")):
            x = x.split("https://t.me/c/")[1]
        elif (x.startswith("https://t.me/")):
            x = x.split("https://t.me/")[1]
        else:
            await lol.edit("Enter a vailed telegram link")
    
        print("X= ", x)
    
        try:
            fromchat, msgid = x.split("/")
        except:
            await lol.edit("Check command syntax.")
            return
    
        try:
            fromchat = int("-100" + fromchat)
        except:
            try:
                fromchat = str("@" + fromchat)
            except:
                await lol.edit("Check command syntax..")
                return
    
        try:
            msgid = int(msgid)
        except:
            await lol.edit("Check command syntax...")
            return


    message = await client.get_messages(fromchat, msgid)
    if message.photo:
        print(message.photo.file_id)
        t_xt = f"Photo ID : `{message.photo.file_id}`"
    elif message.animation:
        print(message.animation.file_id)
        t_xt = f"Animation ID : `{message.animation.file_id}`"
    elif message.video:
        print(message.video.file_id)
        t_xt = f"Video ID : `{message.video.file_id}`"
    elif message.sticker:
        print(message.sticker.file_id)
        t_xt = f"Sticker ID : `{message.sticker.file_id}`"
    else:
        print("Isn't media")
        t_xt = f"Isn't media : `{message.message_id}`"



    await lol.edit(t_xt)



@friday_on_cmd(
    ["rmfileid"],
    cmd_help={
        "help": "based on file_id remove any photo, video or gif from a channel  \n .rmfileid fromchat | file_id string ",
        "example": "{ch}rmfileid @Friday | CAACAgEAAx0EVyqAowADAmDT1DPEEgS6yfthpEJ7xz8Q_EEXAAI4AQACFU9RRzdYwfdBpAWgHgQ ",
    },
)
async def rmfileid(client, message):
    lol = await edit_or_reply(message, "Processing please wait")
    x = get_text(message)
    x=x.replace(" ","")

    try:
        fromchat, fileid = x.split("|")
    except:
        await lol.edit("Check command syntax")

    try:
        fromchat =int(fromchat)
    except:
        if not (fromchat.startswith("@")):
            await lol.edit("Enter a vailed username or id")
            return
    try:
        fileid = str(fileid)
    except:
        await lol.edit("Enter a vailed string")
        return
    a = 0
    try:
        async for message in client.iter_history(fromchat, reverse=True):
          try:
            ################################
            if message.photo:
                if message.photo.file_id == fileid:
                    await client.delete_messages(fromchat, message.message_id)
                    a+=1
            elif message.video:
                if message.video.file_id == fileid:
                    await client.delete_messages(fromchat, message.message_id)
                    a+=1
            elif message.animation:
                if message.animation.file_id == fileid:
                    await client.delete_messages(fromchat, message.message_id)
                    a+=1
            elif message.sticker:
                if message.sticker.file_id == fileid:
                    await client.delete_messages(fromchat, message.message_id)
                    a+=1
            else:
                pass

            ################################
          except Exception as e:
            await lol.edit(e)
            pass
          except RPCError as i:
            await lol.edit(i)
            pass   
          await asyncio.sleep(1)
        await lol.edit(f"Messages deleted successfully: {a} from chat: {fromchat}")
    except RPCError as i:
        await lol.edit(i)
        return


@friday_on_cmd(
    ["getstructure"],
    cmd_help={
        "help": "Get the message structure\n .getstructure https://t.me/Friday_Official/446 ",
        "example": "{ch}getstructure https://t.me/Friday_Official/446 ",
        "example": "{ch}getstructure https://t.me/c/1429362247/446 ",
    },
)

async def getstructure(client, message):
    lol = await edit_or_reply(message, "Processing please wait")
    await asyncio.sleep(2)
    x = get_text(message)
    y = x
    tochat = lol.chat.id
    
    if lol.reply_to_message:
        fromchat = lol.reply_to_message.chat.id
        msgid = lol.reply_to_message.message_id
        if lol.reply_to_message.forward_from_chat:
            y = "https://t.me/c/" + str(lol.reply_to_message.forward_from_chat.id).split("-100")[1] + "/" + str(lol.reply_to_message.forward_from_message_id)
        else:
            y = lol.reply_to_message.message_id
    if not lol.reply_to_message:
    
        if (x.startswith("https://t.me/c/")):
            x = x.split("https://t.me/c/")[1]
        elif (x.startswith("https://t.me/")):
            x = x.split("https://t.me/")[1]
        else:
            await lol.edit("Enter a vailed telegram link")
    
        try:
            fromchat, msgid = x.split("/")
        except:
            await lol.edit("Check command syntax.")
            return
    
        try:
            fromchat = int("-100" + fromchat)
        except:
            try:
                fromchat = str("@" + fromchat)
            except:
                await lol.edit("Check command syntax..")
                return
    
        try:
            msgid = int(msgid)
        except:
            await lol.edit("Check command syntax...")
            return
    
    caption = f"Structure of msg id: `{y}`"
    message = await client.get_messages(fromchat, msgid)

    file = open("/home/ubuntu/FridayUserbot/structure.txt", "w")
    file.write(str(message))
    file.close()
    try:
        await client.send_document(tochat, "/home/ubuntu/FridayUserbot/structure.txt", caption=caption)
        await lol.delete()
    except:
        await lol.edit("error") 
   
    if path.exists("/home/ubuntu/FridayUserbot/structure.txt"):
        remove('/home/ubuntu/FridayUserbot/structure.txt')



        


@friday_on_cmd(
    ["prueba"],
    cmd_help={
        "help": "Backup all from one chat/channel to other chat/channel \n .prueba fromchat | to chat | msgid (Optional to resume) \nNote: | is essential",
        "example": "{ch}prueba @fridaysupportofficial | @fridaychat | 1600\n For private groups/channels add -100",
    },
)

async def prueba(client, message):
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
#        if message.entities:
#            inlk = message.entities
#            linlk = [i.url for i in inlk if "t.me" in i.url]
#
#            if len(linlk) >4:
#                print("#", message.message_id ,"botonera texto:", len(linlk))
#                return True
        if message.entities:
            url = 0
            for MessageEntity in message.entities:
                if MessageEntity.type == "text_link":
                    url+=1
            if url > 3:
                return True

        if message.caption_entities:
            url = 0
            for MessageEntity in message.caption_entities:
                if MessageEntity.type == "text_link":
                    url+=1
            if url >3:
                return True  

#        if message.caption_entities:
#            link = message.caption_entities
#            linkk = [i.url for i in link if "t.me" if i.url]
#            if len (linkk) >4:
#                print("#", message.message_id, "botonera texto cap_ent", len(linkk))
#                return True
                
        if message.reply_markup:
         #   for message["reply_markup"]["inline_keyboard"] in message["reply_markup"]
         #       print(message["reply_markup"]["inline_keyboard"])
        #    ur = 0
            inlk = message.reply_markup.inline_keyboard
            linlk = [i[0].url for i in inlk if "t.me" in i[0].url]
        #    print(inlk)
     #       linlk = [i[0].url for i in inlk] 
     #       for x in linlk:
     #           if linlk.startswith("https://t.me/"): ur+=1
      #      print(linlk)

            if len(linlk) > 4:
                print("#", message.message_id ,"botonera botones:", len(linlk))
                return True
        #    for InlineKeyboardMarkup in message.reply_markup:
        #        if InlineKeyboardMarkup.inline_keyboard:
        #            url = 0
        #            for InlineKeyboardButton in InlineKeyboardMarkup.inline_keyboard:
    #   #                if InlineKeyboardButton.url.startswith("https://t.me/"):
        #                if InlineKeyboardButton.url:
        #                    url+=1
        #            if url > 3:
        #                return True


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

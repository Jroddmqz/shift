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
    try:
        if (x.startswith("https://t.me/c/")):
            x = x.split("https://t.me/c/").pop()
    except:
        try:
            if (x.startswith("https://t.me/")):
                x = x.split("https://t.me/").pop()
        except:
            await lol.edit("Enter a vailed link")
            return

    try:
        fromchat, msgid = x.split("/")
    except:
        await lol.edit("Check command syntax")
        return

    try:
        fromchat = int("-100" + fromchat)
    except:
        try:
            fromchat = str("@" + fromchat)
        except:
            await lol.edit("Check command syntax")
            return

    try:
        msgid = int(msgid)
    except:
        await lol.edit("Check command syntax")
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
        async for message in client.iter_history(fromchat, reverse=reverse):
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
        

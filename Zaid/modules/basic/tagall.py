from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import Message

from Zaid.modules.help import add_command_help

spam_chats = set()  # Use a set for faster lookups


def get_arg(message: Message) -> str:
    """Get the argument from the message"""
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


async def get_chat_members(client: Client, chat_id: int) -> list:
    """Get a list of chat members"""
    members = []
    async for member in client.get_chat_members(chat_id):
        members.append(member)
    return members


async def send_tagged_message(client: Client, chat_id: int, text: str) -> None:
    """Send a message with tagged users"""
    await client.send_message(chat_id, text)


async def mentionall(client: Client, message: Message) -> None:
    """Tag all members in a chat"""
    chat_id = message.chat.id
    reply_to_message = message.reply_to_message
    args = get_arg(message)

    if not reply_to_message and not args:
        await message.edit("**Send me a message or reply to a message!**")
        return

    await message.delete()
    spam_chats.add(chat_id)

    members = await get_chat_members(client, chat_id)
    usrnum = 0
    usrtxt = ""

    for member in members:
        usrnum += 1
        usrtxt += f"[{member.user.first_name}](tg://user?id={member.user.id}), "
        if usrnum == 5:
            if args:
                txt = f"{args}\n\n{usrtxt}"
                await send_tagged_message(client, chat_id, txt)
            elif reply_to_message:
                await reply_to_message.reply(usrtxt)
            await sleep(2)
            usrnum = 0
            usrtxt = ""

    try:
        spam_chats.remove(chat_id)
    except KeyError:
        pass


async def cancel_spam(client: Client, message: Message) -> None:
    """Cancel the tagall process"""
    if message.chat.id not in spam_chats:
        await message.edit("**It seems there is no tagall here.**")
        return

    try:
        spam_chats.remove(message.chat.id)
    except KeyError:
        pass
    await message.edit("**Cancelled.**")


add_command_help(
    "tagall",
    [
        [
            "tagall [text/reply ke chat]",
            "Tag all the members one by one",
        ],
        [
            "cancel",
            f"to stop.tagall",
        ],
    ],
)

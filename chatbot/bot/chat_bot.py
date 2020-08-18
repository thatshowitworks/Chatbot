from time import time
from pyrogram import Filters

from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
from coffeehouse.exception import CoffeeHouseError as CFError

from chatbot import app, LOGGER, CF_API_KEY, NAME
import chatbot.bot.database.chatbot_db as db
from chatbot.bot.database.chatbot_db import is_rem

CoffeeHouseAPI = API(CF_API_KEY)
api_client = LydiaAI(CoffeeHouseAPI)


HELP_TEXT = """• Reply `.adduser` to someone to enable the chatbot for that person!
• Reply `.rmuser` to someone to stop the chatbot for them!
Have fun!"""

@app.on_message(Filters.command("start"))
def start(client, message):
    app.send_message(message.chat.id, "I'm alive! :3")


@app.on_message(Filters.command("help"))
def help(client, message):
    message.reply(HELP_TEXT)
   
def add(user_id):
    is_user = 1
    if not is_user == 2:
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        db.set_ses(user_id, ses_id, expires)
        message.reply("AI enabled for user successfully!")
        LOGGER.info(f"AI enabled for user - {user_id}")
    else:
        LOGGER.info("AI is already enabled for this user!")
    
def check_message(client, msg):
    reply_msg = msg.reply_to_message
    if NAME.lower() in msg.text.lower():
        return True
    if reply_msg and reply_msg.from_user is not None:
        if reply_msg.from_user.is_self:
            return True
    return False
    
        
@app.on_message(Filters.text)
def chatbot(client, message):
    msg = message
    if not check_message(client, msg):
        return
    user_id = msg.from_user.id
    add(user_id)
    #if not user_id in db.USERS:
        #return
    sesh, exp = db.get_ses(user_id)
    query = msg.text
    if int(exp) < time():
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        db.set_ses(user_id, ses_id, expires)
        sesh, exp = ses_id, expires
        
    try:
        msg.reply_chat_action("typing")
        response = api_client.think_thought(sesh, query)
        msg.reply_text(response)
    except CFError as e:
        app.send_message(chat_id=msg.chat.id, text=f"An error occurred:\n`{e}`", parse_mode="md")

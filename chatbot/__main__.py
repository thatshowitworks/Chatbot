import sys
from chatbot import app, LOGGER

from chatbot.bot import chat_bot

if len(sys.argv) not in (1, 3, 4):
    quit(1)
else:
    app.start()
    LOGGER.info("Simple chatbot written using the pyrogram library.\nUses Intellivoid's Coffeehouse API.\n")
    LOGGER.info("Your bot is now online. Check .help for help!")
    app.idle()

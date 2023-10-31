# !/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from err_hand import error_handler
from recept import dict_to_str_start, dict_to_str, set_ingred_str_org, \
    ingred_str_org, ingredstr_to_list_dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, PicklePersistence, DictPersistence,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

INPUTING, CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(4)

'''
ingred_dict={}
ingred_list=[]
ingred_kbd=[]
markup=ReplyKeyboardMarkup([])
'''
ingredients_string = ""


# entry_points
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    user_data = context.user_data
    user_data.clear()
    print(f'{context.user_data=}')

    await update.message.reply_text(
        "Готов принять строку ингредиентов",
        reply_markup=ReplyKeyboardRemove()
    )
    return INPUTING


# INPUTING
async def input_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ingred_text = update.message.text
    context.user_data["ingred_text"] = ingred_text

    # global ingred_dict, ingred_list, ingred_kbd
    ingred_dict, ingred_list, ingred_kbd = ingredstr_to_list_dict(ingred_text)
    context.user_data["ingred_dict"] = ingred_dict
    context.user_data["ingred_list"] = ingred_list
    context.user_data["ingred_kbd"] = ingred_kbd

    ingred_str = "|".join(ingred_list)
    global ingredients_string
    ingredients_string = f"^({ingred_str})$"
    context.user_data["ingredients_string"] = ingredients_string

    reply_keyboard = ingred_kbd
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    context.user_data["markup"] = markup

    print(f"{ingred_text=}")
    await update.message.reply_text(
        f"{dict_to_str_start(ingred_dict)}",
        reply_markup=markup,
    )

    print("os os os =", os.listdir("/tmp"))
    return CHOOSING


# CHOOSING
async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    markup = context.user_data["markup"]
    ingred_dict = context.user_data["ingred_dict"]

    await update.message.reply_html(f"Ингредиент <i>{text} - {ingred_dict[text][0]}</i>.\nИзменить количество ?",
                                    reply_markup=markup, )
    print(f'{context.user_data=}')
    return TYPING_REPLY


# TYPING_REPLY
async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data

    text = update.message.text
    category = user_data["choice"]
    ingred_dict = context.user_data["ingred_dict"]
    markup = context.user_data["markup"]

    new = float(text)
    old = float(ingred_dict[category][0])
    if old:
        coef = float(new / old)
    else:
        coef = 1
    user_data[category] = text
    del user_data["choice"]

    # print("-----", new, old)

    await update.message.reply_text(
        f"{dict_to_str(ingred_dict, coef)}",
        reply_markup=markup,
    )

    print(f'{context.user_data=}')
    return CHOOSING


# fallbacks
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    print(f'{context.user_data=}')
    return ConversationHandler.END


"""Run the bot."""
# Create the Application and pass it your bot's token.
persistence = PicklePersistence(filepath='persfile.txt', update_interval=30)

# persistence = DictPersistence()
application = Application.builder().token("5742009857:AAGIhBQOXEnKPFobwljcFlydSTIPomhd1a4").persistence(
    persistence).build()

# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start)
    ],
    states={
        INPUTING: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                input_information,
            ),
            CommandHandler("start", start)
        ],
        CHOOSING: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")) & filters.Regex(ingredients_string),
                regular_choice
            ),
            CommandHandler("start", start)
        ],
        TYPING_REPLY: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")) & filters.Regex("^(\d+)(\.?)(\d*)$"),
                received_information,
            ),
            CommandHandler("start", start)
        ],

    },
    fallbacks=[
        MessageHandler(
            filters.Regex("^Done$"),
            done
        )
    ],
    name="my_conversation",
    persistent=True,
)

application.add_handler(conv_handler)
application.add_error_handler(error_handler)

if __name__ == "__main__":
    # iiiRun the bot until the user presses Ctrl-C
    application.run_polling()

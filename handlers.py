from typing import cast

from telegram import Update, Chat, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from flats import get_new_flat
from parser import search_params
import templates


WBS, QM, ROOMS_MIN, ROOMS_MAX, SEARCH = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = cast(Chat, update.effective_chat).id
    wbs_keyboard = [["Yes", "No"]]
    reply_markup = ReplyKeyboardMarkup(
        wbs_keyboard, resize_keyboard=True, one_time_keyboard=True
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=templates.greeting,
        reply_markup=reply_markup,
    )
    return WBS


async def adjust_min_qm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    wbs = cast(Message, update.message).text
    if wbs == "Yes":
        search_params["wbs"] = "erforderlich"

    await update.message.reply_text(
        text=templates.from_qm_question, reply_markup=ReplyKeyboardRemove()
    )
    return QM


async def adjust_max_qm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    min_qm = cast(Message, update.message).text
    if min_qm is not None:
        search_params["min_qm"] = float(min_qm)
    await update.message.reply_text(text=templates.to_qm_question)

    return ROOMS_MIN


async def adjust_min_rooms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    max_qm = cast(Message, update.message).text
    if max_qm is not None:
        search_params["max_qm"] = float(max_qm)
    await update.message.reply_text(text=templates.from_rooms_question)

    return ROOMS_MAX


async def adjust_max_rooms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    min_rooms = cast(Message, update.message).text
    if min_rooms is not None:
        search_params["min_rooms"] = float(min_rooms)
    await update.message.reply_text(text=templates.to_rooms_question)

    return SEARCH


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    max_rooms = cast(Message, update.message).text
    if max_rooms is not None:
        search_params["max_rooms"] = float(max_rooms)

    await update.message.reply_text(text=templates.end_conversation)
    context.job_queue.run_repeating(
        check_updates,
        interval=60,
        first=0,
        job_kwargs={"max_instances": 3},
        chat_id=update.message.chat_id,
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("See you next time!")


async def check_updates(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.chat_id
    new_flats = get_new_flat()
    if new_flats:
        for flat in new_flats:
            text_message = templates.flat_message(flat)
            await context.bot.send_message(chat_id=chat_id, text=text_message)

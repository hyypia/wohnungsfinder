import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import TELEGRAM_TOKEN
from flats import get_new_flat
from parser import search_params
from templates import (
    greeting,
    from_qm_question,
    to_qm_question,
    from_rooms_question,
    to_rooms_question,
    end_conversation,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="bot.log",
    filemode="w",
)


WBS, QM, ROOMS, CANCEL = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    wbs_keyboard = [["Yes", "No"]]
    reply_markup = ReplyKeyboardMarkup(
        wbs_keyboard, resize_keyboard=True, one_time_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=greeting, reply_markup=reply_markup
    )
    return WBS


async def adjust_min_qm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    wbs = update.message.text
    # write wbs to params
    if wbs == "Yes":
        search_params["wbs"] = "erforderlich"
    else:
        search_params["wbs"] = ""

    await update.message.reply_text(
        text=from_qm_question, reply_markup=ReplyKeyboardRemove()
    )
    return QM


async def adjust_max_qm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    min_qm = update.message.text
    search_params["min_qm"] = float(min_qm)

    await update.message.reply_text(text=to_qm_question)
    return ROOMS


async def adjust_min_rooms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    max_qm = update.message.text
    search_params["max_qm"] = float(max_qm)

    await update.message.reply_text(text=from_rooms_question)
    return CANCEL


async def adjust_max_rooms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    min_rooms = update.message.text
    search_params["min_rooms"] = float(min_rooms)

    search_keyboard = [["Search"]]
    reply_markup = ReplyKeyboardMarkup(
        search_keyboard, resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text(text=to_rooms_question, reply_markup=reply_markup)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Fix end conversation
    max_rooms = update.message.text
    search_params["max_rooms"] = float(max_rooms)

    await update.message.reply_text(
        text=end_conversation, reply_markup=ReplyKeyboardRemove()
    )
    context.job_queue.run_repeating(
        check_updates, interval=30, first=0, chat_id=update.message.chat_id
    )
    return ConversationHandler.END


async def check_updates(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.chat_id
    new_flats = get_new_flat()
    if new_flats:
        for flat in new_flats:
            text_message = (
                f"{new_flats[flat]['address']}\n"
                f"Zimmeranzahl: {new_flats[flat]['rooms']}\n"
                f"Wohnfläche: {new_flats[flat]['qm']}\n"
                f"{new_flats[flat]['link']}"
            )
        await context.bot.send_message(chat_id=chat_id, text=text_message)
    else:
        text_message = "Nothing new found"

        await context.bot.send_message(chat_id=chat_id, text=text_message)


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handlers = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WBS: [MessageHandler(filters.Regex("^(Yes|No)$"), adjust_min_qm)],
            QM: [MessageHandler(filters.TEXT, adjust_max_qm)],
            ROOMS: [MessageHandler(filters.TEXT, adjust_min_rooms)],
            CANCEL: [MessageHandler(filters.TEXT, adjust_max_rooms)],
        },
        fallbacks=[CommandHandler("Search", cancel)],
    )

    application.add_handler(conv_handlers)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

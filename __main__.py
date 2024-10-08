import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

from config import TELEGRAM_TOKEN
from flats import get_new_flat


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="bot.log",
    filemode="w",
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'll fetch new flats!"
    )
    context.job_queue.run_repeating(
        check_updates, interval=30, first=0, chat_id=update.message.chat_id
    )


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


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler("start", start)

    application.add_handler(start_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

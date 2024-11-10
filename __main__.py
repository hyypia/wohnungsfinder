import logging
import traceback

from telegram import Update
from telegram.ext import (
    ContextTypes,
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import TELEGRAM_TOKEN, DEVELOPER_CHAT_ID
import handlers


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="bot.log",
    filemode="w",
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send message to developer"""

    logger.error("Exeption while handling an update:", exc_info=context.error)

    # Get python message about an exception and join stings from list format
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    await context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=tb_string)


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handlers = ConversationHandler(
        entry_points=[CommandHandler("start", handlers.start)],
        states={
            handlers.WBS: [
                MessageHandler(filters.Regex("^(Yes|No)$"), handlers.adjust_min_qm)
            ],
            handlers.QM: [MessageHandler(filters.TEXT, handlers.adjust_max_qm)],
            handlers.ROOMS_MIN: [
                MessageHandler(filters.TEXT, handlers.adjust_min_rooms)
            ],
            handlers.ROOMS_MAX: [
                MessageHandler(filters.TEXT, handlers.adjust_max_rooms)
            ],
            handlers.SEARCH: [MessageHandler(filters.TEXT, handlers.search)],
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )

    application.add_handler(conv_handlers)
    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

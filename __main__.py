import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import TELEGRAM_TOKEN
import handlers


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="bot.log",
    filemode="w",
)
logger = logging.getLogger(__name__)


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
        fallbacks=[CommandHandler("cancel", handlers.cancel)]
    )

    application.add_handler(conv_handlers)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

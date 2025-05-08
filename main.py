import logging
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, filters,
)
from config import BOT_TOKEN
from handlers.start import start
from constants import *

from handlers.category_manage import (
    add_category, process_add_category,
    edit_category, select_category,
    enter_new_category, delete_category,
    process_delete_category, view_categories
)
from handlers.cancel import cancel

from handlers.add_item import (
    add_item, choose_category,
    get_name, get_quantity
)
from handlers.edit_quantity import (
    edit_quantity, edit_choose_category,
    edit_get_name, edit_get_quantity
)
from handlers.view_items import view_items_entry, list_items


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_category", add_category),
                      CommandHandler("delete_category", delete_category),
                      CommandHandler("edit_category", edit_category)],
        states={
            ADD_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                          process_add_category)],
            DELETE_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                             process_delete_category)],
            SELECT_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                             select_category)],
            ENTER_NEW_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                enter_new_category)]
        },
        fallbacks=[]
    )
    view_categories_handler = CommandHandler("view_categories", view_categories)

    app.add_handler(view_categories_handler)

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler("add", add_item),
                      CommandHandler("edit_quantity", edit_quantity),
                      CommandHandler("view_items", view_items_entry)],
        states={
            CHOOSE_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_category)],
            GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GET_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_quantity)],
            EDIT_QUANTITY_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_choose_category)],
            EDIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_get_name)],
            EDIT_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_get_quantity)],
            LIST_ITEMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_items)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(conv_handler1)


    print("Бот запущен...")
    app.run_polling()
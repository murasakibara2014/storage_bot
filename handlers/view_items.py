from telegram import Update
from telegram.ext import ContextTypes
from services.sheet_api import get_all_items_grouped_by_category
from constants import LIST_ITEMS

async def view_items_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📦 Получаю список товаров...")
    return await list_items(update, context)

async def list_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    grouped_items = get_all_items_grouped_by_category()

    if not grouped_items:
        await update.message.reply_text("❌ Не удалось получить список товаров.")
        return LIST_ITEMS

    message = "📦 Товары по категориям:\n\n"
    for category, items in grouped_items.items():
        message += f"🔹 {category}:\n"
        for item in items:
            message += f"  • {item}\n"
        message += "\n"

    await update.message.reply_text(message)
    return LIST_ITEMS
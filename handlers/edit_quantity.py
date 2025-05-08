from constants import EDIT_QUANTITY_CATEGORY, EDIT_NAME, EDIT_QUANTITY
from telegram.ext import (ContextTypes, ConversationHandler)
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from services.categories import fetch_categories
from services.sheet_api import update_quantity

CATEGORIES = fetch_categories()

async def edit_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вы хотите обновить количество товара.\n"
        "Пожалуйста, выберите категорию:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(cat)] for cat in CATEGORIES],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return EDIT_QUANTITY_CATEGORY

async def edit_choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text
    if category not in CATEGORIES:
        await update.message.reply_text("Пожалуйста, выберите категорию из списка.")
        return EDIT_QUANTITY_CATEGORY

    context.user_data["category"] = category
    await update.message.reply_text("Введите название товара:")
    return EDIT_NAME

async def edit_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data["name"] = name
    await update.message.reply_text("Введите новое количество:")
    return EDIT_QUANTITY

async def edit_get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quantity = update.message.text
    try:
        quantity = int(quantity)
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите целое число.")
        return EDIT_QUANTITY

    category = context.user_data["category"]
    name = context.user_data["name"]

    success = update_quantity(category, name, quantity)

    if success:
        await update.message.reply_text("✅ Количество успешно обновлено!")
    else:
        await update.message.reply_text("❌ Ошибка при обновлении. Убедитесь, что товар существует.")

    return ConversationHandler.END
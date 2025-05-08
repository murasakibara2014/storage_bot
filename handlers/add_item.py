from telegram.ext import ConversationHandler
from services.sheet_api import save_to_sheet
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from constants import CHOOSE_CATEGORY, GET_NAME, GET_QUANTITY
from services.categories import fetch_categories

CATEGORIES = fetch_categories()

async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(update_category_buttons(), one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите категорию:", reply_markup=reply_markup)
    return CHOOSE_CATEGORY

def update_category_buttons():
    return [[KeyboardButton(cat)] for cat in CATEGORIES]

async def choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text
    context.user_data["category"] = category
    if category not in CATEGORIES:
        await update.message.reply_text("Пожалуйста, выберите категорию из предложенных.")
        return CHOOSE_CATEGORY

    await update.message.reply_text("Введите название товара:")
    return GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data["name"] = name
    await update.message.reply_text("Введите количество:")
    return GET_QUANTITY

async def get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quantity = update.message.text

    try:
        quantity = int(quantity)
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите целое число.")
        return GET_QUANTITY

    category = context.user_data["category"]
    name = context.user_data["name"]

    success = save_to_sheet(category, name, quantity)

    if success:
        await update.message.reply_text("✅ Товар успешно добавлен в склад!")
    else:
        await update.message.reply_text("❌ Ошибка при добавлении товара.")

    return ConversationHandler.END

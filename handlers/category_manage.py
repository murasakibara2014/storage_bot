from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from services.categories import fetch_categories
from constants import SELECT_CATEGORY, ENTER_NEW_CATEGORY, DELETE_CATEGORY, EDIT_CATEGORY, ADD_CATEGORY

CATEGORIES = fetch_categories()

async def add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите категорию, которую хотите добавить:")
    return ADD_CATEGORY

async def process_add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category_to_add = update.message.text.strip()

    if category_to_add in CATEGORIES:
        await update.message.reply_text(f"Категория '{category_to_add}' уже существует.")
    else:
        CATEGORIES.append(category_to_add)
        await update.message.reply_text(f"Категория '{category_to_add}' успешно добавлена.")

    return ConversationHandler.END

async def edit_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(cat)] for cat in CATEGORIES],
                                       one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите категорию, которую хотите отредактировать:",
                                    reply_markup=reply_markup)
    return SELECT_CATEGORY

async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category_to_edit = update.message.text.strip()

    if category_to_edit not in CATEGORIES:
        await update.message.reply_text(f"Категория '{category_to_edit}' не найдена.")
        return EDIT_CATEGORY

    context.user_data["category_to_edit"] = category_to_edit
    await update.message.reply_text("Введите новое название категории:")
    return ENTER_NEW_CATEGORY

async def enter_new_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_category_name = update.message.text.strip()

    old_category_name = context.user_data["category_to_edit"]

    if new_category_name in CATEGORIES:
        await update.message.reply_text(f"Категория '{new_category_name}' уже существует.")
        return ENTER_NEW_CATEGORY

    CATEGORIES[CATEGORIES.index(old_category_name)] = new_category_name
    await update.message.reply_text(
        f"Категория '{old_category_name}' успешно изменена на '{new_category_name}'.")

    return ConversationHandler.END

async def delete_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите категорию, которую хотите удалить:")
    return DELETE_CATEGORY

async def process_delete_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category_to_remove = update.message.text.strip()

    if category_to_remove in CATEGORIES:
        CATEGORIES.remove(category_to_remove)
        await update.message.reply_text(f"Категория '{category_to_remove}' успешно удалена.")
    else:
        await update.message.reply_text(f"Категория '{category_to_remove}' не найдена.")

    return ConversationHandler.END

async def view_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CATEGORIES:
        await update.message.reply_text("Текущие категории: " + ", ".join(CATEGORIES))
    else:
        await update.message.reply_text("Категории пусты.")
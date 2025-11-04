from typing import Final

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from answers import get_prediction, get_yes_no


TOKEN_ENV_VAR: Final[str] = "7983929551:AAGgj0Jh4YcPfrKktl8jp9pvJxOYRuqZnug"


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        "Привет! Я бот - Ответы Судьбы.\n"
        "Я могу дать вам ответ да/нет или предсказание\n\n"
        "   - Для получения ответа да/нет напишите 'Ваш вопрос'?\n"
        "   - Для получения предсказания напишите 'Дай мне предсказание'\n"
    )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(get_yes_no())


async def handle_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(get_prediction())


def text_is_answer(text: str) -> bool:
    normalized = text.strip().lower()
    if "?" in normalized:
        return True
    question_words = (
        "кто ", "что ", "где ", "когда ", "зачем ", "почему ", "как ", "ли ",
        "можно ли ", "стоит ли ", "нужно ли ", "будет ли ", "правда ли ",
    )
    return normalized.startswith(question_words)


def text_is_prediction(text: str) -> bool:
    normalized = text.strip().lower()
    if normalized.startswith("/предсказание"):
        return True
    triggers = (
        "дай мне предсказание",
        "дай предсказание",
        "предсказание",
        "предскажи",
        "хочу предсказание",
    )
    return any(trigger in normalized for trigger in triggers)


async def handle_text_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.text is None:
        return
    text = update.message.text
    if text_is_prediction(text):
        await handle_prediction(update, context)
        return
    if text_is_answer(text):
        await handle_answer(update, context)
        return
    await update.message.reply_text(
        "Не понял команду. Напиши 'ответ' или 'предсказание', либо /start."
    )


def main() -> None:
    token = TOKEN_ENV_VAR
    if not token:
        raise RuntimeError(
            "Токен бота не задан. Проверьте TOKEN_ENV_VAR в коде."
        )

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", handle_start))

    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_router)
    )

    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex(r"^/(ответ|предсказание)\b"), handle_text_router)
    )

    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass



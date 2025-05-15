import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Квестові точки
QUEST_POINTS = [
    # (тут вставити той же список з попереднього коду)
]

user_states = {}

def normalize_answer(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r"[^\wа-яіїєґ]+", "", text)
    return text.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {"step": 0, "awaiting_hint": False}
    await update.message.reply_text(
        "Вітаю у квесті 'Код Ейнштейна'! Напиши відповідь на перше завдання.\n\n" +
        QUEST_POINTS[0]["text"]
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state = user_states.get(user_id)

    if not user_state:
        await update.message.reply_text("Напиши /start, щоб розпочати квест.")
        return

    text = update.message.text.lower().strip()

    if text == "підказка":
        if user_state["awaiting_hint"]:
            current_step = user_state["step"]
            hint = QUEST_POINTS[current_step]["hint"]
            await update.message.reply_text(f"Підказка: {hint}")
            user_state["awaiting_hint"] = False
        else:
            await update.message.reply_text("Підказка наразі недоступна. Спробуй спершу відповісти на завдання.")
        return

    current_step = user_state["step"]
    correct_answer = normalize_answer(QUEST_POINTS[current_step]["answer"])
    user_answer = normalize_answer(text)

    if user_answer == correct_answer:
        user_state["step"] += 1
        user_state["awaiting_hint"] = False
        if user_state["step"] < len(QUEST_POINTS):
            next_task = QUEST_POINTS[user_state["step"]]["text"]
            await update.message.reply_text(f"Правильно!\n\nНаступне завдання:\n\n{next_task}")
        else:
            await update.message.reply_text("Вітаю! Ти пройшов усі завдання квесту!")
            user_states.pop(user_id)
    else:
        user_state["awaiting_hint"] = True
        await update.message.reply_text("Невірна відповідь. Спробуй ще або напиши 'підказка' для підказки.")

if __name__ == "__main__":
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено...")
    app.run_polling()


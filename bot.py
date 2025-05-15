from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

import re

# Завдання квесту
QUEST = [
    {
        "task": ("У темряві світло ховається за трьома кроками назад.\n"
                 "Розшифруй послання, що стоїть на порозі нових знань:\n"
                 "'Khoor, Zruog!'\n\n"
                 "Порада: подумай про того, хто шукав світло у лінзах і променях."),
        "answer": "hello world",
        "hint": ("«Інтелект — це не знання, а уява.» – А. Ейнштейн\n"
                 "«Світло відкриває те, що приховано у темряві.»\n\n"
                 "Наступний крок: Знайди місце, де фізика ставала мистецтвом світла. "
                 "Колись тут шліфували лінзи, сьогодні — це будівля зі скляним обличчям."),
    },
    {
        "task": ("Вулиця, де колись жив геній, ховає його адресу.\n"
                 "Знайди її, розгадавши загадку:\n"
                 "Дві німецькі назви, що несуть імена\n"
                 "Мюллер та Штрассе — поєднай, щоб вийшло місце.\n"
                 "Цифра додається — це будинок, де він жив."),
        "answer": "мюллерштрассе 54",
        "hint": ("Адреса, де дитинство і дорослість перетнулись, "
                 "де думки генія виросли серед вуличного шуму."),
    },
    {
        "task": ("Яка назва гімназії, де сходилися думки генія?\n"
                 "Підказка: В її назві поєднано королівську спадщину та класичну освіту."),
        "answer": "людвігмаксиміліанська гімназія",
        "hint": ("«Освіта — це те, що залишається після того, як забуваєш все вивчене.»\n"
                 "Цей заклад стоїть в центрі і пам’ятає перші кроки Ейнштейна."),
    },
    {
        "task": ("Розв'яжи формулу, щоб дізнатись рік початку навчання генія:\n"
                 "(47×40)+(100÷25)\n"
                 "Відповідь — це рік, коли почалось навчання."),
        "answer": "1888",
        "hint": ("Початок шляхів великого вченого у стінах гімназії, "
                 "що й досі стоїть у центрі міста."),
    },
    {
        "task": ("Уяви оцінки з латини та грецької, які в Ейнштейна були найгіршими.\n"
                 "Які це були? Відповідь у форматі: '5, 5' (цифрами, через кому)."),
        "answer": "5, 5",
        "hint": ("Не всі науки підкорялись генію, "
                 "але це допомогло йому розвивати інші таланти."),
    },
    {
        "task": ("Назви кав’ярню, де люди та машини змагаються за смак кави."),
        "answer": "men versus machine",
        "hint": ("«Технології — лише інструмент, людина творить справжнє.»\n"
                 "Де це місце — там борються люди з машинами."),
    },
    {
        "task": ("Фінал — Віктуалієнмаркт.\n\n"
                 "«Все, що вивчав Ейнштейн, перетворилось на формулу. Але істинна формула — у русі життя. "
                 "На ринку, де все змінюється, шукай продавця, що торгує продуктом вічності.»\n"
                 "Який продукт символізує вічність?"),
        "answer": "мед",
        "hint": ("Вітаємо! Ти розкрив таємницю Ейнштейна — життя рухається, як мед, що ніколи не псується."),
    },
]

# Функція нормалізації відповіді (прибирає пробіли, великі букви, знаки пунктуації)
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\wа-яґєії0-9]', '', text)  # Латиниця, кирилиця, цифри, без знаків
    return text.strip()

# Збереження прогресу користувачів у пам'яті (у продакшені варто використовувати базу)
user_progress = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_progress[user_id] = {"step": 0, "asked_hint": False}
    await update.message.reply_text(
        "Ласкаво просимо в квест ‘Код Ейнштейна’! Напиши 'Почати', щоб розпочати."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    if user_id not in user_progress:
        user_progress[user_id] = {"step": 0, "asked_hint": False}

    step = user_progress[user_id]["step"]

    if text == "почати" and step == 0:
        # Показати перше завдання
        await update.message.reply_text(QUEST[0]["task"])
        user_progress[user_id]["step"] = 1
        user_progress[user_id]["asked_hint"] = False
        return

    # Якщо користувач просить підказку
    if text == "підказка":
        if step == 0:
            await update.message.reply_text("Спочатку напиши 'Почати', щоб розпочати квест.")
            return
        elif step > len(QUEST):
            await update.message.reply_text("Квест вже завершено.")
            return
        else:
            if not user_progress[user_id]["asked_hint"]:
                await update.message.reply_text(QUEST[step-1]["hint"])
                user_progress[user_id]["asked_hint"] = True
            else:
                await update.message.reply_text("Підказка вже була надана.")
            return

    # Якщо квест завершено
    if step == 0:
        await update.message.reply_text("Напиши 'Почати', щоб розпочати квест.")
        return

    if step > len(QUEST):
        await update.message.reply_text("Квест завершено! Дякуємо за участь.")
        return

    # Перевірка відповіді
    correct_answer = normalize(QUEST[step-1]["answer"])
    user_answer = normalize(text)

    if user_answer == correct_answer:
        # Відповідь правильна
        if step == len(QUEST):
            await update.message.reply_text(
                "Правильно! Ви успішно завершили квест. Вітаємо і дякуємо за участь!"
            )
            user_progress[user_id]["step"] = step + 1
        else:
            await update.message.reply_text(
                "Правильно! Наступне завдання:\n\n" + QUEST[step]["task"]
            )
            user_progress[user_id]["step"] = step + 1
            user_progress[user_id]["asked_hint"] = False
    else:
        # Неправильна відповідь
        await update.message.reply_text(
            "Невірно. Спробуй ще раз або напиши 'Підказка', якщо потрібна допомога."
        )


if __name__ == '__main__':
    import os

    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("Помилка: не встановлено BOT_TOKEN в змінних середовища.")
        exit(1)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот запущено...")
    app.run_polling()

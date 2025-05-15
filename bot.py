import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

QUEST = [
    {
        "task": "Точка 1 — Оптичний інститут.\n\n"
                "Завдання: Розшифруй цей текст за допомогою шифру Цезаря:\n"
                "'Khoor, Zruog!'\n\n"
                "Підказка: Сдвиг на 3 літери назад.",
        "answer": "hello, world",
        "hint": "Цитата: 'Інтелект — це не знання, а уява.' – Альберт Ейнштейн\n"
                "Наступна зупинка — гімназія, де вчився Ейнштейн."
    },
    {
        "task": "Точка 2 — Гімназія Ейнштейна.\n\n"
                "Завдання: В які роки Ейнштейн навчався у цій гімназії?\n"
                "Підказка: Період між 1888 і 1894.",
        "answer": "1888-1894",
        "hint": "Цитата: 'Освіта — це те, що залишається після того, як забуваєш все вивчене.'\n"
                "Наступна зупинка — кав’ярня Süß & Salzig."
    },
    {
        "task": "Точка 3 — Кав’ярня Süß & Salzig.\n\n"
                "Завдання: Знайди булочку з корицею — вона допоможе отримати наступну підказку.\n"
                "Напиши слово, що описує цей смак.",
        "answer": "кориця",
        "hint": "Цитата: 'Солодкість життя в дрібницях.'\n"
                "Наступна зупинка — кав’ярня Men Versus Machine."
    },
    {
        "task": "Точка 4 — Кав’ярня Men Versus Machine.\n\n"
                "Завдання: Що вказує назва цієї кав’ярні?\n"
                "Підказка: Борьба між людиною та технологією.",
        "answer": "боротьба",
        "hint": "Цитата: 'Технології — лише інструмент, людина творить справжнє.'\n"
                "Наступна зупинка — Віктуалієнмаркт."
    },
    {
        "task": "Фінал — Віктуалієнмаркт.\n\n"
                "Підказка: 'Все, що вивчав Ейнштейн, перетворилось на формулу. Але істинна формула — у русі життя. "
                "На ринку, де все змінюється, шукай продавця, що торгує чимось, що не старіє.'\n"
                "Завдання: Який продукт на ринку символізує вічність і не старіє?",
        "answer": "мед",
        "hint": "Вітаємо! Ти розкрив таємницю Ейнштейна — життя рухається, як мед, що ніколи не псується."
    }
]

user_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_state[message.chat.id] = 0
    bot.send_message(message.chat.id, "Ласкаво просимо в квест ‘Код Ейнштейна’! Напиши 'Почати', щоб почати.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    step = user_state.get(chat_id, 0)

    if step >= len(QUEST):
        bot.send_message(chat_id, "Квест завершено! Дякуємо за участь.")
        return

    current_task = QUEST[step]

    if step == 0 and message.text.lower() != "почати":
        bot.send_message(chat_id, "Напиши 'Почати', щоб розпочати квест.")
        return

    if step == 0 and message.text.lower() == "почати":
        bot.send_message(chat_id, current_task["task"])
        user_state[chat_id] = 1
        return

    if step > 0:
        if message.text.lower() == current_task["answer"]:
            bot.send_message(chat_id, current_task["hint"])
            user_state[chat_id] += 1

            if user_state[chat_id] < len(QUEST):
                next_task = QUEST[user_state[chat_id]]
                bot.send_message(chat_id, next_task["task"])
        else:
            bot.send_message(chat_id, "Спробуй ще раз або подумай над підказкою.")

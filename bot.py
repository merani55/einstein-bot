import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
print(f"Token is: {TOKEN}")

bot = telebot.TeleBot(TOKEN)

QUEST = [
    # ... (твій список завдань як є)
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

bot.polling()

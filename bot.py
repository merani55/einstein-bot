import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

QUEST = [
    {
        "task": ("У темряві світло ховається за трьома кроками назад.\n"
                 "Розшифруй послання, що стоїть на порозі нових знань:\n"
                 "'Khoor, Zruog!'\n\n"
                 "Порада: подумай про того, хто шукав світло у лінзах і променях."),
        "answer": "hello world",
        "hint": ("«Інтелект — це не знання, а уява.» – А. Ейнштейн\n"
                 "«Світло відкриває те, що приховано у темряві.»\n"
                 "Наступний крок: Знайди місце, де фізика ставала мистецтвом світла. "
                 "Колись тут шліфували лінзи, сьогодні — це будівля зі скляним обличчям.")
    },
    {
        "task": ("Вулиця, де час і простір переплітаються, та номер, що тримає пам’ять про генія.\n"
                 "Щоб рухатися далі, знайди адресу, де думки Ейнштейна набирали силу."),
        "answer": "мюллерштрассе 54",
        "hint": ("Якщо шукаєш початок великої історії, подумай про місце, "
                 "де стіни знають все про світло і тінь.")
    },
    {
        "task": ("Які роки закарбувалися у пам’яті одного генія у стінах, де сходилися перші його думки?"),
        "answer": "1888-1894",
        "hint": ("Це період, коли формувалося майбутнє.\n"
                 "Школа, де Ейнштейн пізнавав основи, стоїть і досі у центрі міста.\n"
                 "В її назві поєднано королівську спадщину та класичну освіту.")
    },
    {
        "task": ("Смак, що відкриває нові світи — знайди слово, яке описує аромат булочки з корицею, "
                 "що відкриває шлях далі."),
        "answer": "suuapinga",
        "hint": ("Солодкість життя ховається у дрібницях.\n"
                 "Інколи шлях лежить через аромат і смак, що об’єднує людей.")
    },
    {
        "task": ("Що вказує назва цієї кав’ярні? Подумай про боротьбу, що несе зміни у світ."),
        "answer": "боротьба",
        "hint": ("Технології — лише інструмент, людина творить справжнє.\n"
                 "Де людина зустрічає машину, там народжується нова ера.")
    },
    {
        "task": ("Все, що вивчав Ейнштейн, перетворилось на формулу. Але істинна формула — у русі життя.\n"
                 "На ринку, де все змінюється, шукай продукт, що символізує вічність і не старіє."),
        "answer": "мед",
        "hint": ("Життя рухається, як мед — що не псується і не старіє.\n"
                 "Цей символ постійності серед змін допоможе зрозуміти суть.")
    },
]

user_state = {}  # chat_id: {step: int, hint_requested: bool}

@bot.message_handler(commands=['start'])
def start(message):
    user_state[message.chat.id] = {"step": 0, "hint_requested": False}
    bot.send_message(message.chat.id,
                     "Ласкаво просимо в квест ‘Код Ейнштейна’! Напиши 'Почати', щоб почати.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip().lower()

    if chat_id not in user_state:
        user_state[chat_id] = {"step": 0, "hint_requested": False}

    step = user_state[chat_id]["step"]
    hint_requested = user_state[chat_id]["hint_requested"]

    # Початковий крок: чекати 'почати'
    if step == 0:
        if text == "почати":
            bot.send_message(chat_id, QUEST[0]["task"])
            user_state[chat_id]["step"] = 1
            user_state[chat_id]["hint_requested"] = False
        else:
            bot.send_message(chat_id, "Напиши 'Почати', щоб розпочати квест.")
        return

    # Кінець квесту
    if step > len(QUEST):
        bot.send_message(chat_id, "Квест завершено! Дякуємо за участь.")
        return

    # Якщо користувач попросив підказку
    if text == "підказка":
        if step <= len(QUEST) and step > 0:
            bot.send_message(chat_id, QUEST[step - 1]["hint"])
            user_state[chat_id]["hint_requested"] = True
        else:
            bot.send_message(chat_id, "Поки немає підказки для цього етапу.")
        return

    # Перевірка відповіді
    if step <= len(QUEST) and step > 0:
        expected_answer = QUEST[step - 1]["answer"].lower()

        # Нормалізація відповіді: прибрати пробіли, знаки пунктуації, привести до нижнього регістру
        def normalize(text):
            import re
            return re.sub(r"[^a-zа-я0-9]+", "", text.lower())

        if normalize(text) == normalize(expected_answer):
            bot.send_message(chat_id, "Правильно! 🎉")
            user_state[chat_id]["step"] += 1
            user_state[chat_id]["hint_requested"] = False
            if user_state[chat_id]["step"] <= len(QUEST):
                bot.send_message(chat_id, QUEST[user_state[chat_id]["step"] - 1]["task"])
            else:
                bot.send_message(chat_id, "Вітаємо! Ви завершили квест ‘Код Ейнштейна’. Дякуємо за участь!")
        else:
            if not hint_requested:
                bot.send_message(chat_id, "Спробуй ще раз або напиши 'Підказка', якщо хочеш допомогу.")
            else:
                bot.send_message(chat_id, "Все ще не вийшло. Подумай уважніше або звернись до підказки.")

if __name__ == "__main__":
    print("Бот запущено")
    bot.polling(none_stop=True)


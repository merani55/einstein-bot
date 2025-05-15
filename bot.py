import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

QUEST = [
    {
        "task": (
            "У темряві світло ховається за трьома кроками назад.\n"
            "Розшифруй послання, що стоїть на порозі нових знань:\n"
            "'Khoor, Zruog!'\n"
            "Порада: подумай про того, хто шукав світло у лінзах і променях."
        ),
        "answer": "hello world",
        "hint": (
            "«Інтелект — це не знання, а уява.» – А. Ейнштейн\n"
            "«Світло відкриває те, що приховано у темряві.»\n"
            "Наступний крок: Знайди місце, де фізика ставала мистецтвом світла. "
            "Колись тут шліфували лінзи, сьогодні — це будівля зі скляним обличчям."
        )
    },
    {
        "task": (
            "Де колись жив геній, що дивився на світ і вбачав у ньому формули?\n"
            "Шукайте вулицю, що носить ім'я з п’яти складів, і будинок з номером усього одинарним."
        ),
        "answer": "müllerstraße 54",
        "hint": (
            "Пам’ятка: Вулиця носить ім’я, що складно вимовити, але легко впізнати.\n"
            "Номер будинку — найменший з можливих."
        )
    },
    {
        "task": (
            "У центрі міста стоїть школа, де юний геній формував свої думки.\n"
            "Її ім’я поєднує королівську спадщину та класичну освіту.\n"
            "Вгадай назву цієї гімназії."
        ),
        "answer": "luitpold-gymnasium",
        "hint": (
            "Тут навчався той, хто змінив уявлення про час і простір.\n"
            "Назва містить ім’я короля Людвіга.\n"
            "Це одна з найстаріших гімназій міста, що зберегла свою історію."
        )
    },
    {
        "task": (
            "Які роки закарбувалися у пам’яті генія в стінах цієї гімназії?\n"
            "Період, коли формувалося його майбутнє, між 1888 і 1894."
        ),
        "answer": "1888-1894",
        "hint": (
            "Цей період охоплює майже шість років.\n"
            "Відповідь — у форматі `1888-1894`.\n"
            "Саме тут юний Ейнштейн здобував основи, що згодом змінили світ."
        )
    },
    {
        "task": (
            "Щоб знайти кав'ярню, де час зупиняється у парі чашок, згадай слово,\n"
            "що звучить незвично — су-уа-пін-га.\n"
            "Відгадай її назву."
        ),
        "answer": "suuapinga",
        "hint": (
            "Це місце кавоманів з унікальним звучанням назви.\n"
            "Тут кожна чашка — це подорож у світ смаків."
        )
    },
    {
        "task": (
            "Які роки навчання найбільш значущі для генія?\n"
            "Після відкриття його таланту у гімназії, життя набирає обертів."
        ),
        "answer": "1888-1894",
        "hint": (
            "Період формування особистості та ідей.\n"
            "Відповідь у форматі `1888-1894`."
        )
    },
    {
        "task": (
            "Що означає назва кав’ярні 'Men Versus Machine'?\n"
            "Вона відображає давній конфлікт."
        ),
        "answer": "боротьба",
        "hint": (
            "Це суперечка між людиною і технологією.\n"
            "Тема, що розгортається на багатьох фронтах."
        )
    },
    {
        "task": (
            "Ринок змінюється, але тут є продукт, що символізує вічність.\n"
            "Що це за продукт?"
        ),
        "answer": "мед",
        "hint": (
            "Цей продукт не псується з роками,\n"
            "як знання, які залишаються назавжди."
        )
    }
]

user_state = {}
awaiting_hint = set()

def normalize(text):
    return ''.join(c.lower() for c in text if c.isalnum())

@bot.message_handler(commands=['start'])
def start(message):
    user_state[message.chat.id] = 0
    if message.chat.id in awaiting_hint:
        awaiting_hint.remove(message.chat.id)
    bot.send_message(message.chat.id, "Ласкаво просимо в квест ‘Код Ейнштейна’! Напиши 'Почати', щоб розпочати.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    step = user_state.get(chat_id, 0)
    text = message.text.strip().lower()

    if step == 0:
        if text == "почати":
            bot.send_message(chat_id, QUEST[0]["task"])
            user_state[chat_id] = 1
        else:
            bot.send_message(chat_id, "Напиши 'Почати', щоб розпочати квест.")
        return

    if step > len(QUEST):
        bot.send_message(chat_id, "Квест завершено! Дякуємо за участь.")
        return

    # Якщо користувач просить підказку
    if text == "підказка":
        if step - 1 < len(QUEST):
            bot.send_message(chat_id, QUEST[step - 1]["hint"])
            awaiting_hint.add(chat_id)
        else:
            bot.send_message(chat_id, "Підказок більше немає.")
        return

    # Перевірка відповіді
    normalized_answer = normalize(QUEST[step - 1]["answer"])
    normalized_text = normalize(text)

    if normalized_text == normalized_answer:
        if chat_id in awaiting_hint:
            awaiting_hint.remove(chat_id)
        if step < len(QUEST):
            bot.send_message(chat_id, "Правильно! Ось наступне завдання:")
            bot.send_message(chat_id, QUEST[step]["task"])
            user_state[chat_id] += 1
        else:
            bot.send_message(chat_id, "Вітаємо! Ви пройшли квест ‘Код Ейнштейна’!")
            user_state[chat_id] = len(QUEST) + 1
    else:
        bot.send_message(chat_id, "Спробуй ще раз або напиши 'Підказка', якщо потрібна допомога.")

if __name__ == "__main__":
    print("Бот запущено...")
    bot.infinity_polling()

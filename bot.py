import telebot
import os
import re

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
                 "Які це були? Відповідь у форматі: 'латина, грецька' (у нижньому регістрі)."),
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

user_state = {}
user_hints_requested = {}

def normalize(text):
    text = text.lower()
    text = text.strip()
    text = re.sub(r'[^\w\sа-яіїєґ]', '', text)  # Прибрати всі небуквено-цифрові символи, крім кирилиці
    text = text.replace("ё", "е")  # Для російської, на всяк випадок
    text = text.replace("ї", "і")  # Замінити для уніфікації
    text = text.replace("й", "і")
    return text

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_state[chat_id] = 0
    user_hints_requested[chat_id] = False
    bot.send_message(chat_id, "Ласкаво просимо в квест ‘Код Ейнштейна’! Напиши 'Почати', щоб почати.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    step = user_state.get(chat_id, 0)
    hint_requested = user_hints_requested.get(chat_id, False)
    
    if step >= len(QUEST):
        bot.send_message(chat_id, "Квест завершено! Дякуємо за участь.")
        return
    
    if step == 0:
        if message.text.lower() == "почати":
            bot.send_message(chat_id, QUEST[step]["task"])
            user_state[chat_id] = 1
            user_hints_requested[chat_id] = False
        else:
            bot.send_message(chat_id, "Напиши 'Почати', щоб розпочати квест.")
        return
    
    current_task = QUEST[step - 1]  # тому що після старту step=1 для 0-го завдання
    
    text = normalize(message.text)
    
    # Перевірка запиту підказки
    if text in ["підказка", "підсказка", "hint"]:
        if not user_hints_requested.get(chat_id, False):
            bot.send_message(chat_id, current_task["hint"])
            user_hints_requested[chat_id] = True
        else:
            bot.send_message(chat_id, "Підказка вже надана. Спробуй відповісти.")
        return
    
    # Перевірка відповіді
    correct_answer = normalize(current_task["answer"])
    
    if text == correct_answer:
        user_state[chat_id] += 1
        user_hints_requested[chat_id] = False
        
        if user_state[chat_id] >= len(QUEST):
            bot.send_message(chat_id, "Вітаємо! Ти пройшов увесь квест ‘Код Ейнштейна’!")
        else:
            next_task = QUEST[user_state[chat_id]]
            bot.send_message(chat_id, "Правильно! Ось наступне завдання:\n\n" + next_task["task"])
    else:
        bot.send_message(chat_id, "Неправильна відповідь. Спробуй ще раз або напиши 'Підказка' для допомоги.")

if __name__ == "__main__":
    print("Бот запущено...")
    bot.polling(none_stop=True)

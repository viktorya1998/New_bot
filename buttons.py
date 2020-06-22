import pandas as pd
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

BUTTON1_ABOUT = "Об университете ❓"
BUTTON2_STUDENT = "Поступающим 👩‍🎓"


# Клавиатура 1 - Главная
def keyboard1():
    keyboard = [
        [
            KeyboardButton(BUTTON1_ABOUT),
            KeyboardButton(BUTTON2_STUDENT),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


BUTTON_HOSTEL = "Общежитие 🏡"
BUTTON_HOUSING = "Корпуса 🏢"

BUTTON_PRICE = "Стоимость 💰"
BUTTON_DOCUMENTS = "Документы 📋"

BUTTON_SPEC = "Направления подготовки 📝"
BUTTON_BALL = "Баллы 📊"

BUTTON_RESULTS = "Итоги приема ✅"
BUTTON_FACULTY = "Факультеты 📚"

BUTTON_SCHOLARSHIP = "Стипендия 💶"
BUTTON_LEISURE = "Досуг 🎉"

BUTTON_COMMISSION = "Приемная комиссия 🙍‍♂"
BUTTON0_BACK = "Назад 🔙"


# Клавиатура 2 - Поступающим
def keyboard2():
    keyboard = [
        [
            KeyboardButton(BUTTON_HOSTEL),
            KeyboardButton(BUTTON_HOUSING),
        ],
        [
            KeyboardButton(BUTTON_PRICE),
            KeyboardButton(BUTTON_DOCUMENTS),
        ],
        [
            KeyboardButton(BUTTON_SPEC),
            KeyboardButton(BUTTON_BALL),
        ],
        [
            KeyboardButton(BUTTON_FACULTY),
            KeyboardButton(BUTTON_RESULTS),
        ],
        [
            KeyboardButton(BUTTON_SCHOLARSHIP),
            KeyboardButton(BUTTON_LEISURE),
        ],
        [
            KeyboardButton(BUTTON_COMMISSION),
            KeyboardButton(BUTTON0_BACK),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


BUTTON_HOSTEL1 = "В каком общежитии я буду жить"
BUTTON_HOSTEL2 = "Кто живет в общежитии"
BUTTON_HOSTEL3 = "Контактная информация об общежитиях"


# общежития
def keyboard3():
    keyboard = [
        [
            KeyboardButton(BUTTON_HOSTEL1),
        ],
        [
            KeyboardButton(BUTTON_HOSTEL2),
        ],
        [
            KeyboardButton(BUTTON_HOSTEL3),
        ],
        [
            KeyboardButton(BUTTON0_BACK),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


BUTTON_HOUSING1 = "В каком корпусе я буду учиться"
BUTTON_HOUSING2 = "Кто учиться в корпусе"
BUTTON_HOUSING3 = "Контактная информация об корпусах"


# корпуса
def keyboard4():
    keyboard = [
        [
            KeyboardButton(BUTTON_HOUSING1),
        ],
        [
            KeyboardButton(BUTTON_HOUSING2),
        ],
        [
            KeyboardButton(BUTTON_HOUSING3),
        ],
        [
            KeyboardButton(BUTTON0_BACK),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


BUTTON_SPEC1 = "Куда поступить с предметами"
BUTTON_SPEC2 = "Предметы для поступления"
BUTTON_SPEC3 = "Количество мест"


# Вопросы по аправлениям подготовки
def keyboard5():
    keyboard = [
        [
            KeyboardButton(BUTTON_SPEC1),
        ],
        [
            KeyboardButton(BUTTON_SPEC2),
        ],
        [
            KeyboardButton(BUTTON_SPEC3),
        ],
        [
            KeyboardButton(BUTTON0_BACK),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


# Факультеты
def keyboard6():
    df = pd.read_excel('Faculties.xlsx', sheet_name='Лист1')
    keyboard = []
    for i in df[1]:
        keyboard.append([KeyboardButton(i)])
    keyboard.append([KeyboardButton(BUTTON0_BACK)])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


# Специальности
def keyboard7():
    df = pd.read_excel('Profession.xlsx', sheet_name='Лист1')
    keyboard = []
    for i in df[1]:
        keyboard.append([KeyboardButton(i)])
    keyboard.append([KeyboardButton(BUTTON0_BACK)])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

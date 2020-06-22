import re
import SpeechException
import buttons
import config
import db
import joblib
import numpy as np
import pandas as pd
import pymorphy2
import requests

from sklearn.preprocessing import LabelEncoder
from telegram import Bot, Update, InputMediaPhoto
from telegram.ext import CallbackContext, MessageHandler, Updater, Filters, CommandHandler
from telegram.utils.request import Request

subject = ['математика', 'информатика', 'русский', 'химия', 'физика', 'география', 'биология', 'физкультура',
           'рисование', 'литература', 'обществознание', 'журналистика', 'история', 'собеседование', 'иностранный',
           'английский', 'немецкий', 'искусство']

# загружаем обученную модель
swg = joblib.load('Model/model.pkl')
vector = joblib.load('Model/model_vec.pkl')
encoder = LabelEncoder()
encoder.classes_ = joblib.load('Model/model_enc.joblib')

category = ''
b = False


# удаляем смайлики
def sub_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return (emoji_pattern.sub(r'', text)).strip()


# формирование ответа
def get_answer(text, update, context):
    df = pd.read_excel('Users.xlsx', sheet_name='Лист1')
    global category, b

    if text == buttons.BUTTON0_BACK:
        r = np.where(update.message.from_user.id == df['id'])[0][0]
        keyboard = df.loc[r, 'key']
        if keyboard == str(buttons.keyboard2()):
            new_keyboard = buttons.keyboard1()
        else:
            new_keyboard = buttons.keyboard2()

        df.loc[r, 'key'] = new_keyboard
        df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Что вас интересует?",
            reply_markup=new_keyboard,
        )
        return ''
    #
    elif text == buttons.BUTTON2_STUDENT:
        category = ''
        df.loc[np.where(update.message.from_user.id == df['id'])[0][0], 'key'] = str(buttons.keyboard2())
        df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Что вас интересует?",
            reply_markup=buttons.keyboard2(),
        )
        return ''
    #
    elif text == buttons.BUTTON_SPEC:
        category = ''
        df.loc[np.where(update.message.from_user.id == df['id'])[0][0], 'key'] = str(buttons.keyboard5())
        df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Выберите, какую информацию о направлениях подготовки вы хотели бы получить?",
            reply_markup=buttons.keyboard5(),
        )
        return ''
    #
    elif category == 'Общая информация':
        category = ''
        return 'ФГБОУ ВО «Вятский государственный университет» (ВятГУ) – государственное вясшее учебное заведение в ' \
               'городе Кирове. ВятГУ насчитывает 9 институтов, объединяющих 75 кафедр. Ведет обучение по традиционной ' \
               'и дистанционной формам, на которых обучается более 20 000 студентов по более чем 140 направлениям и ' \
               'профилям подготовки. Число научно-педагогических сотрудников составляет около 1000 человек, ' \
               'из них 105 — докторов наук и профессоров, 581 — кандидатов наук и доцентов, работает аспирантура и ' \
               'докторантура, функционирует 1 специализированный совет по защите диссертаций. '
    #
    elif category == 'Приветствие':
        return 'Здраствуйте, ' + update.message.from_user.first_name + '! Я персональный помощник абитуриента ВятГУ. ' \
                                                                       'Чем я могу помочь? '
    #
    elif category == 'Прощание':
        return 'Всего хорошего! Я всегда готов помочь!'
    #
    elif category == 'Общежитие':
        b = True
        if text == buttons.BUTTON_HOSTEL1:
            category = buttons.BUTTON_HOSTEL1
            df.loc[np.where(update.message.from_user.id == df['id'])[0][0], 'key'] = str(buttons.keyboard6())
            df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Куда вы хотите поступить?",
                reply_markup=buttons.keyboard6(),
            )
        elif text == buttons.BUTTON_HOSTEL2:
            category = buttons.BUTTON_HOSTEL2
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Какое общажитие вас интересует?",
            )
        elif text == buttons.BUTTON_HOSTEL3:
            category = buttons.BUTTON_HOSTEL3
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Какое общажитие вас интересует?",
            )
        else:
            text = "Выберите, какую информацию про общежитие вы хотите получить?"
            df.loc[np.where(update.message.from_user.id == df['id'])[0][0], 'key'] = str(buttons.keyboard3())
            df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=text,
                reply_markup=buttons.keyboard3()
            )
        return ''
    #
    elif category == 'Корпуса':
        b = True
        if text == buttons.BUTTON_HOUSING1:
            category = buttons.BUTTON_HOUSING1
            df.loc[np.where(update.message.from_user.id == df['id'])[0][0], 'key'] = str(buttons.keyboard6())
            df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Куда вы хотите поступить?",
                reply_markup=buttons.keyboard6(),
            )
        elif text == buttons.BUTTON_HOUSING2:
            category = buttons.BUTTON_HOUSING2
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Какой корпус вас интересует?",
            )
        elif text == buttons.BUTTON_HOUSING3:
            category = buttons.BUTTON_HOUSING3
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Какой корпус вас интересует?",
            )
        else:
            text = "Выберите, какую информацию про корпуса вы хотите получить?"
            df.loc[np.where(update.message.from_user.id == df['id'])[0][0], 'key'] = str(buttons.keyboard4())
            df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=text,
                reply_markup=buttons.keyboard4()
            )
        return ''

    elif category == 'Стоимость':
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            category = ''
            b = False
            answer = 'Стоимость обучения равна \n'
            for t in res:
                answer += str(t[0]) + '. С учетом скидки ' + str(t[1])
            return answer

        lists = intersection(Morph(text), pd.read_excel('Profession.xlsx', sheet_name='Лист1'))

        if b and not lists:
            return 'А вот это не совсем понятно...'
        elif not lists:
            b = True
            df.loc[np.where(update.message.from_user.id == df['id'])[0][0], 'key'] = str(buttons.keyboard7())
            df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Какое направление подготовки вас интересует?",
                reply_markup=buttons.keyboard7(),
            )
            return ''
        else:
            return get_data(lists)
    #
    elif category == 'Документы':
        category = ''
        return 'Абитуриенты подают в приемную комиссию университета следующие документы:\n' \
               '  📌 Документ об образовании\n' \
               '  📌 Паспорт\n' \
               '  📌 4 фотографии 3х4\n' \
               '  📌 Заявление о поступлении в ВятГУ\n' \
               '  📌 Документы, подтверждающие льготы\n' \
               '  📌 Медицинская справка (специальность "Таможенное дело)"\n' \
               '  📌 При смене фамилии – подтверждающие документы\n' \
               '  📌 Военный билет для граждан, прошедших военную службу'
    #
    elif category == 'Стипендия':
        category = ''
        return 'Лица, обучающиеся в университете, обеспечиваются стипендией в соответствии с действующим ' \
               'законодательством. Виды стипендий для обучающихся по образовательной программе бакалавриат:' \
               '\n  💷  Академическая стипендия - 2820 рублей' \
               '\n       💲 оценки «4» и «5» – 3525 рублей' \
               '\n       💲 оценки  «5» – 4230 рублей' \
               '\n  💷  Социальная стипендия - 4230 рублей' \
               '\n  💷  Повышенная социальная стипендия - 7000 рублей' \
               '\n  💷  Повышенная академическая стипендия - 7200 рублей' \
               '\n\nБолее подробную информацию можно посмотреть на сайте: ' \
               'https://www.vyatsu.ru/studentu-1/stipendial-noe-obespechenie-i-material-naya-podder.html' \
            #
    #
    elif category == 'Баллы':
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            category = ''
            b = False
            answer = 'Проходные баллы:\n'
            i = 0
            for t in res:
                answer += str(l[i]) + ': ' + str(t[0]) + '\n'
                i += 1
            return answer

        lists = intersection(Morph(text), subject)
        if b and not lists:
            return 'А вот это не совсем понятно...'
        elif not lists:
            b = True
            return 'Какие предметы вас интересуют?'
        else:
            return get_data(lists)
    #
    elif category == 'Итоги приема':
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            category = ''
            b = False
            answer = ''
            i = 0
            for t in l:
                answer += 'Итоги приема за ' + str(t) + ' год: ' + str(res[0]) + '\n\nСредние баллы: ' + str(res[1])
                i += 1
            return answer

        lists = intersection(Morph(text), ['2019', '2018', '2017', '2016'])
        if b and not lists:
            return 'А вот это не совсем понятно...'
        elif b:
            return get_data(lists)
        elif not lists:
            b = True
            return 'Итоги приема какого года вас интересует?'
        else:
            return get_data(lists)
    #
    elif category == 'Факультеты':
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            category = ''
            b = False
            answer = 'На данном факультете осуществляется подготовка студентов по следующим специальностям:'
            i = 0
            for t in res:
                answer += '\n   ✅  ' + str(t[0])
                i += 1
            return answer

        lists = intersection(Morph(text), pd.read_excel('Faculties.xlsx', sheet_name='Лист1'))

        if b and not lists:
            return 'А вот это не совсем понятно...'
        elif b:
            return get_data(lists)
        elif not lists:
            b = True
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Какой факультет или институт вас интересует?",
                reply_markup=buttons.keyboard6(),
            )
            return ''
        else:
            return get_data(lists)
    #
    elif category == 'Куда поступить с предметами':
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            if not res:
                return 'В ВятГУ нет направлений подготовки с такими предматами'
            category = ''
            b = False
            answer = 'С данными предметами можно поступить на следующие напрвления подготовки:'
            i = 0
            for t in res:
                answer += '\n   ✅  ' + str(t[0])
                i += 1
            return answer

        lists = intersection(Morph(text), subject)
        if b and not lists:
            return 'А вот это не совсем понятно...'
        elif b:
            return get_data(lists)
        elif not lists:
            b = True
            return 'Какие предметы вас интересуют?'
        else:
            return get_data(lists)
    #
    elif category == 'Досуг':
        category = ''
        answer = 'Студенческая жизнь во время обучения в ВятГУ насыщена множеством ярких и запоминающихся событий. С ' \
                 'первого курса и до окончания университета студентам предоставлены возможности и созданы условия для ' \
                 'самореализации, развития талантов и творчества. '
        media = [
            InputMediaPhoto(open("image/1.jpg", 'rb')),
            InputMediaPhoto(open("image/2.jpg", 'rb')),
            InputMediaPhoto(open("image/3.jpg", 'rb')),
            InputMediaPhoto(open("image/4.jpg", 'rb'), answer)
        ]
        return media
    #
    elif category == 'Приемная комиссия':
        context.bot.send_message(chat_id=update.message.chat_id, text="Приемная комиссия:\n📞(8332) 74-29-29, "
                                                                      "64-89-89\n🌍610000, г.Киров, ул.Московская. д.36, "
                                                                      "ауд.129\n✉prcom@vyatsu.ru\n📅пн-чт: 8:00-17:00, "
                                                                      "пт: 08:00-16:00\nсб, вс: выходной\n\nКурсы и "
                                                                      "тестирование:\n📞(8332) 74-29-35, "
                                                                      "32-11-42\n🌍ул.Московская. д.36, "
                                                                      "ауд.243\n✉ct@vyatsu.ru\n📅пн-чт: 8:00-17:00, "
                                                                      "пт: 08:00-16:00")
        return ''
    #
    elif category == 'Предметы для поступления':
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            category = ''
            b = False
            answer = 'Для поступления необходимы следующие предметы:\n'
            i = 0
            for t in res:
                answer += " ✅ " + str(t[0]) + '\n'
                i += 1
            return answer

        lists = intersection(Morph(text), pd.read_excel('Profession.xlsx', sheet_name='Лист1'))

        if b and not lists:
            return 'А вот это не совсем понятно...'
        elif b:
            return get_data(lists)
        elif not lists:
            b = True
            df.loc[np.where(update.message.from_user.id == df['id'])[0][0], 'key'] = str(buttons.keyboard7())
            df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Какое направление подготовки вас интересует?",
                reply_markup=buttons.keyboard7(),
            )
            return ''
        else:
            return get_data(lists)
    #
    elif category == 'Количество мест':
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            category = ''
            b = False
            i = 0
            answer = ''
            for t in res:
                answer += '\n\nКоличество мест для приёма на обучение по направлению подготовки ' + l[i] + ':'
                answer += '\n ✅ Бюджетные места: ' + str(t[0]) + '\n ✅ Целевая квота: ' + str(t[1]) + \
                          '\n ✅ Особая квота: ' + str(t[2]) + '\n ✅ Места с оплатой:' + str(t[3])
                i += 1
            return answer

        lists = intersection(Morph(text), pd.read_excel('Profession.xlsx', sheet_name='Лист1'))

        if b and not lists:
            return 'А вот это не совсем понятно...'
        elif not lists:
            b = True
            df.loc[np.where(update.message.from_user.id == df['id'])[0][0], 'key'] = str(buttons.keyboard7())
            df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Какое направление подготовки вас интересует?",
                reply_markup=buttons.keyboard7(),
            )
            return ''
        else:
            return get_data(lists)

    # Кто живет/учится в общежитии/корпусе
    elif category in [buttons.BUTTON_HOSTEL2, buttons.BUTTON_HOUSING2]:
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            answer = ''
            for r in res:
                if category == buttons.BUTTON_HOSTEL2:
                    answer += 'В общежитии ' + str(r[0]) + ' проживают студенты следующих факультетов и институтов: '
                else:
                    answer += 'В ' + str(r[0]) + ' корпусе учатся студенты следующих факультетов и институтов: '
                for j in r[1]:
                    answer += '\n   ✅ ' + str(j)
                answer += '\n\n'
            category = ''
            b = False
            return answer

        if category == buttons.BUTTON_HOSTEL2:
            lists = intersection(Morph(text), [str(i) for i in range(1, 9)])
        else:
            r = [str(i) for i in range(1, 24)]
            lists = intersection(Morph(text), r)
        if b and not lists:
            return 'А вот это не совсем понятно...'
        else:
            return get_data(lists)

    # В каком общежитии/корпусе я буду жить/учится
    elif category in [buttons.BUTTON_HOSTEL1, buttons.BUTTON_HOUSING1]:
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            if category == buttons.BUTTON_HOSTEL1:
                answer = 'Вы будите жить в одном из следующих общежитий: '
                for r in res:
                    answer += '\n   ✅  Общежитие ' + str(r[0]) + ' - адрес: ' + str(r[1])
            else:
                answer = 'Ваш основной корпус №' + str(res[0][0]) + ' и находится по адресу: ' + str(res[0][1])
            category = ''
            b = False
            return answer

        lists = intersection(Morph(text), pd.read_excel('Faculties.xlsx', sheet_name='Лист1'))

        if b and not lists:
            return 'А вот это не совсем понятно...'
        else:
            return get_data(lists)

    # Контактная информация об общежитиях/корпусах
    elif category in [buttons.BUTTON_HOSTEL3, buttons.BUTTON_HOUSING3]:
        def get_data(l):
            global category, b
            res = db.connect(category, l)
            category = ''
            b = False
            answer = ''
            if category == buttons.BUTTON_HOSTEL1:
                for r in res:
                    answer += '✅  Общежитие ' + str(r[0][0]) + \
                              '\n - Адрес: ' + str(r[0][1]) + \
                              '\n - Телефон: ' + str(r[0][2]) + '\n\n'
            else:
                for r in res:
                    answer += '✅  Корпус ' + str(r[0][0]) + \
                              '\n - Адрес: ' + str(r[0][1]) + \
                              '\n - Телефон: ' + str(r[0][2]) + '\n\n'
            return answer

        lists = intersection(Morph(text), ['1', '2', '3', '4', '5', '6', '7', '8'])
        if b and not lists:
            return 'А вот это не совсем понятно...'
        else:
            return get_data(lists)


# если пользователь зашел впервые
def do_start(update: Update, context: CallbackContext):
    id = update.message.from_user.id
    keyboard = buttons.keyboard1()

    df = pd.read_excel('Users.xlsx', sheet_name='Лист1')
    mask = np.where(id == df['id'])
    if len(mask[0]) == 0:
        count = len(df['id'])
        df.loc[count, 'id'] = id
        df.loc[count, 'key'] = keyboard
        df.to_excel('Users.xlsx', sheet_name='Лист1', index=False)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Приветствуем абитуриентов ВятГУ в нашем чат-боте! Здесь вы можете найти ответы на часто задаваемые "
             "вопросы. Выберите интересующий вас раздел. Не забывайте о полезном для вас ресурсе: "
             "https://www.vyatsu.ru/abiturientu.html",
        reply_markup=buttons.keyboard1(),
    )


#  добавление вопроса в модель
def add_excel(text, name_file):
    global category
    df = pd.read_excel(name_file, sheet_name='Лист1')
    mask = np.where(text == df)
    if len(mask[0]) == 0:
        try:
            nan_indexes = np.where(pd.isnull(df[category]))
            df.loc[nan_indexes[0][0], category] = text
        except:
            count = len(df[category])
            df.loc[count, category] = text
        finally:
            df.to_excel(name_file, sheet_name='Лист1', index=False)


#  удаление знаков пунктуации
def sub_symbol(text):
    text = re.sub(r'[()"<>.,!?;]', "", text)
    text = text.lower()
    return text


#  исправление ошибок в сообщении
def correct(text):
    r = requests.post("https://speller.yandex.net/services/spellservice.json/checkText", data={'text': text})
    data = r.json()
    changes = {change['word']: change['s'][0] for change in data}
    for word, suggestion in changes.items():
        text = text.replace(word, suggestion)
    return text


# приведения слов к нормальной форме
def Morph(text):
    text = sub_symbol(text)
    text = correct(text)
    text = sub_emoji(text)
    morph = pymorphy2.MorphAnalyzer()
    new_text = ''
    for word in text.split(' '):
        new_text += morph.parse(word)[0].normal_form + " "
    print(new_text[0:-1])
    return new_text[0:-1]


# извлечение параметров
def intersection(text, array):
    if type(array) == list:
        text = text.split(' ')
    else:
        array = array[2]
    rew = [i for i in array if i in text]
    return rew


# получаем категорию
def get_category(text):
    global category
    text = Morph(text)
    df = pd.read_excel('model.xlsx', sheet_name='Лист1')
    mask = np.where(text == df)
    if len(mask[0]) == 0:
        t = vector.transform([text])
        rt = swg.predict_proba(t)
        if rt.max() > 0.3:
            Y = swg.predict(t)
            category = encoder.inverse_transform(Y)[0]
            add_excel(text, 'model.xlsx')
        else:
            category = 'NaN'
    else:
        category = list(df)[mask[1][0]]


def Answer(text, update, context):
    if not b and text != buttons.BUTTON0_BACK:
        get_category(text)

    if category == 'NaN':
        r = 'Попробуй, пожалуйства, выразить свою мысль по-другому.'
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=r,
        )
        return
    else:
        r = get_answer(text, update, context)

    if r != '':
        if isinstance(r, list):
            context.bot.send_media_group(update.message.chat_id, r)
        else:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=r,
            )


#  получено новое сообщение текст
def do_echo(update: Update, context: CallbackContext):
    global category
    text = update.message.text
    print(str(update.message.from_user.first_name) + ": " + str(text))

    Answer(text, update, context)


#  получено новое голосовое сообщение
def do_echo_voice(update: Update, context: CallbackContext):
    file_id = update.message.voice.file_id
    file = context.bot.get_file(file_id)
    file.download('voice.ogg')

    text = SpeechException.get_text(update.message.voice.file_id)
    Answer(text, update, context)


# инициализация
def main():
    request = Request(con_pool_size=8)

    bot = Bot(
        token=config.TG_TOKEN,
        request=request,
        base_url=config.TG_API_URL
    )

    updater = Updater(
        bot=bot,
        use_context=True
    )

    print("..Start..\n")

    start_handler = CommandHandler("start", do_start)
    text_handler = MessageHandler(Filters.text, do_echo)
    mp3_handler = MessageHandler(Filters.voice, do_echo_voice)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(text_handler)
    updater.dispatcher.add_handler(mp3_handler)

    updater.start_polling()  # начать обработку входящих сообщений
    updater.idle()  # не прерывать скрипт до обработки всех сообщений


if __name__ == '__main__':
    main()

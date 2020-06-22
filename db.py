import pandas as pd
import psycopg2


def connect(intents, entity):
    conn = psycopg2.connect(dbname='VyatGU', user='postgres', password='mypassword', host='localhost')
    cursor = conn.cursor()
    st = ''
    if intents == 'Факультеты':
        name = get_data(entity, 'Факультеты')
        if name == '':
            return []
        else:
            st = 'SELECT Название FROM "Направления подготовки" WHERE Факультет = (SELECT id FROM Факультеты WHERE ' \
                 'Название = ' + "'" + str(name[0]) + "') "

    elif intents == 'Предметы для поступления':
        name = get_data(entity, 'Специальности')
        if name == '':
            return []
        else:
            st = 'SELECT Предмет1, Предмет2, Предмет3 FROM "Направления подготовки" WHERE Название = ' + "'" + \
                 str(name[0]) + "'"
            cursor.execute(st)
            records = cursor.fetchall()
            st = 'SELECT Название FROM Предметы WHERE id IN (' + str(records[0][0]) + ', ' + str(
                records[0][1]) + ', ' + str(
                records[0][2]) + ')'

    elif intents == 'Куда поступить с предметами':
        cursor.execute('SELECT id FROM Предметы WHERE Название in (' + get_list(entity) + ')')
        x = cursor.fetchall()

        mas = []
        for k in x:
            st = 'SELECT Название FROM "Направления подготовки" WHERE Предмет1 = ' + str(k[0]) + ' or Предмет2 = ' + \
                 str(k[0]) + ' or Предмет3 = ' + str(k[0])
            cursor.execute(st)
            mas.append(cursor.fetchall())

        if len(mas) == 2:
            res = [ele1 for ele1 in mas[0] for ele2 in mas[1] if ele1 == ele2]
            return res
        elif len(mas) == 3:
            return list(set(mas[0]) & mas[1] & set(mas[2]))
        else:
            return mas[0]

    elif intents == 'Баллы':
        st = "SELECT Балл FROM Предметы WHERE Название in (" + get_list(entity) + ")"

    elif intents == 'Количество мест':
        list = []
        for i in entity:
            list.extend(get_data([i], 'Специальности'))
        if not list:
            return []
        else:
            st = 'SELECT Бюджет, Целевые, Особые, Платные FROM Места WHERE id in (SELECT Места FROM "Направления ' \
                 'подготовки" WHERE Название in (' + get_list(entity) + "))"

    elif intents == 'В каком общежитии я буду жить':
        name = get_data(entity, 'Факультеты')
        if name == '':
            return []
        else:
            st = 'SELECT id, Адрес FROM Общежития WHERE ARRAY[id] && ANY (SELECT Общежитие FROM Факультеты ' \
                 'WHERE Название =' + get_list(name) + ")"

    elif intents == 'Кто живет в общежитии':
        mas = []
        for i in entity:
            st = 'SELECT Название FROM "Факультеты" WHERE Общежитие && ARRAY[' + str(i) + ']'
            cursor.execute(st)
            mas.append([i, cursor.fetchall()])
        return mas

    elif intents == 'Контактная информация об общежитиях':
        mas = []
        for i in entity:
            st = 'SELECT id, Адрес, Телефон FROM Общежития WHERE id = ' + str(i)
            cursor.execute(st)
            mas.append(cursor.fetchall())
        return mas

    elif intents == 'В каком корпусе я буду учиться':
        name = get_data(entity, 'Факультеты')
        if name == '':
            return []
        else:
            st = 'SELECT id, Адрес FROM Корпуса WHERE id in (SELECT Корпус FROM Факультеты ' \
                 'WHERE Название =' + get_list(name) + ")"

    elif intents == 'Кто учиться в корпусе':
        mas = []
        if type(entity) == str:
            entity = [entity]
        for i in entity:
            st = 'SELECT Название FROM "Факультеты" WHERE Корпус in (' + str(i) + ')'
            cursor.execute(st)
            mas.append([i, cursor.fetchall()])
        return mas

    elif intents == 'Контактная информация об корпусах':
        mas = []
        for i in entity:
            st = 'SELECT id, Адрес, Телефон FROM Корпуса WHERE id = ' + str(i)
            cursor.execute(st)
            mas.append(cursor.fetchall())
        return mas

    elif intents == 'Стоимость':
        name = get_data(entity, 'Специальности')
        if name == '':
            return []
        else:
            st = 'SELECT Цена, Скидка FROM Стоимость WHERE id in (SELECT Стоимость FROM "Направления подготовки" ' \
                 'WHERE Название in (' + get_list(name) + "))"

    elif intents == 'Итоги приема':
        df = pd.read_excel('Reception_results.xlsx', sheet_name='Лист1')
        try:
            name = df[entity[0]]
            return name
        except:
            return ''

    cursor.execute(st)
    return cursor.fetchall()


def get_data(entity, file):
    df = pd.read_excel(file + '.xlsx', sheet_name='Лист1')
    try:
        name = list(df[1])[list(df[2]).index(entity[0])]
        return [name]
    except:
        return ''


def get_list(en):
    if len(en) == 1:
        return "'" + en[0] + "'"
    name = ""
    for i in en:
        name += "'" + i + "'"
    return name.replace("''", "', '")

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
import vk
import json
import re

from sklearn.svm import SVC

from config import VK_TOKEN


def add_excel(text, name_column, name_file):
    df = pd.read_excel(name_file, sheet_name='Лист1')
    mask = np.where(text == df)
    if len(mask[0]) == 0:
        try:
            # print(str(text) + '\n' + str(name_column) + ": ")
            i = input(str(text) + '\n' + str(name_column) + ": ")
            if i != '':
                name_column = i

            nan_indexes = np.where(pd.isnull(df[name_column]))
            df.loc[nan_indexes[0][0], name_column] = text
        except:
            count = len(df[name_column])
            df.loc[count, name_column] = text
        finally:
            df.to_excel(name_file, sheet_name='Лист1', index=False)


def train(name_file):
    df = pd.read_excel(name_file + '.xlsx', sheet_name='Лист1')

    question = []
    theme = []
    for i in df:
        for j in df[i]:
            if j == j:
                question.append(j)
                theme.append(i)

    encoder = LabelEncoder()
    vector = TfidfVectorizer()

    train_x = vector.fit_transform(question)
    train_y = encoder.fit_transform(theme)

    svg = SVC()
    svg.fit(train_x, train_y)

    joblib.dump(svg, 'Model/' + name_file + '.pkl')
    print("Модель сохранена в файл " + 'Model/' + name_file + '.pkl')

    joblib.dump(vector.vocabulary_, 'Model/' + name_file + '_vec.pkl')
    print("TfidfVectorizer сохраненн в файл " + 'Model/' + name_file + '_vec.pkl')

    joblib.dump(encoder.classes_, 'Model/' + name_file + '_enc.joblib')
    print("LabelEncoder сохранен в файл " + 'Model/' + name_file + '_enc.joblib')


def get_data():
    text = open('posts_students.txt', 'r', encoding='utf-8').read()
    text = text.lower()
    text = re.sub(r'[()"<>]', "", text)
    split_regex = re.compile(r'[.|!|?|…|]')
    sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(text)])

    return sentences


def add_model(name_file):
    svg = joblib.load('Model/model.pkl')
    vectorizer = CountVectorizer(vocabulary=joblib.load('Model/model_vec.pkl'))
    encoder = LabelEncoder()
    encoder.classes_ = joblib.load('Model/model_enc.joblib')

    date = get_data()

    for text in date:
        t = vectorizer.transform([text])
        category = svg.predict(t)
        answer = encoder.inverse_transform(category)
        add_excel(text, answer, name_file + '.xlsx')


def save_posts_students():
    all_posts = json.load(open('posts.json'))
    posts_students = ''

    svg = joblib.load('Model/posts.pkl')
    vectorizer = CountVectorizer(vocabulary=joblib.load('Model/posts_vec.pkl'))
    encoder = LabelEncoder()
    encoder.classes_ = joblib.load('Model/posts_enc.joblib')

    for i in all_posts:
        text_post = i['text'].replace('\n', ' ')
        text = vectorizer.transform([text_post])
        category = svg.predict(text)
        answer = encoder.inverse_transform(category)

        if answer[0] != 'Админ':
            posts_students += text_post + '\n'

    f = open("posts_students.txt", "w", encoding='utf-8')
    f.write(posts_students)
    f.close()

    print('Посты студентов сохранены в файл posts_students.txt')


def save_all_posts():
    session = vk.Session(access_token=VK_TOKEN)
    vk_api = vk.API(session)

    offset = 0
    all_posts = []

    # получим 1000 постов
    while offset < 1000:
        r = vk_api.wall.get(owner_id=-67048316, count=100, v=5.107, offset=offset)
        posts = r['items']
        all_posts.extend(posts)
        offset += 100

    with open('posts.json', 'w') as file:
        json.dump(all_posts, file)

    print('Посты сохранены в файл posts.json')


def test_model():
    df = pd.read_excel('tests.xlsx', sheet_name='Лист1')

    question = []
    theme = []
    for i in df:
        for j in df[i]:
            if j == j:
                question.append(j)
                theme.append(i)

    svg = joblib.load('Model/model.pkl')
    vectorizer = CountVectorizer(vocabulary=joblib.load('Model/model_vec.pkl'))
    encoder = LabelEncoder()
    encoder.classes_ = joblib.load('Model/model_enc.joblib')

    train_x = vectorizer.transform(question)
    train_y = encoder.transform(theme)

    y_pred = svg.predict(train_x)

    print(metrics.accuracy_score(train_y, y_pred))


# save_all_posts()
# train('posts')
# save_posts_students()

# train('model')
# add_model('model')
# test_model()

import joblib

import pandas as pd
from sklearn import metrics, tree
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

name = ['Баллы', 'Документы', 'Досуг', 'Итоги приема', 'Количество мест', 'Корпуса', 'Куда поступить',
        'Общая информация', 'Общежитие', 'Что сдавать', 'Приветствие', 'Приемная комиссия', 'Прощание',
        'Стипендия', 'Стоимость', 'Факультеты']


def train(name_file, b):
    df = pd.read_excel(name_file + '.xlsx', sheet_name='Лист1')
    question = []
    theme = []
    for i in df:
        for j in df[i]:
            if j == j:
                question.append(j)
                theme.append(i)

    question, theme = shuffle(question, theme)

    encoder = LabelEncoder()
    vector = TfidfVectorizer()

    train_x = vector.fit_transform(question)
    train_y = encoder.fit_transform(theme)

    k = 200
    train_x = vector.fit_transform(question[:len(question) - k])
    train_y = encoder.fit_transform(theme[:len(theme) - k])

    test_x = vector.transform(question[len(question) - k:])
    test_y = encoder.transform(theme[len(theme) - k:])

    # к - ближайших соседей
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(train_x, train_y)
    Y = knn.predict(test_x)
    if b:
        clf_report = classification_report(test_y, Y, target_names=name, output_dict=True)
        sns.heatmap(pd.DataFrame(clf_report).iloc[:-1, :].T, annot=True, cmap= 'cividis')
        plt.show(sns)

    print('к - ближайших соседей: ' + str(metrics.accuracy_score(test_y, Y)))

    # метод опорных векторов
    svc = SVC(probability=True)
    svc.fit(train_x, train_y)
    Y = svc.predict(test_x)

    if b:
        clf_report = classification_report(test_y, Y, target_names=name, output_dict=True)
        sns.heatmap(pd.DataFrame(clf_report).iloc[:-1, :].T, annot=True, cmap= 'cividis')
        plt.show(sns)

    print('метод опорных векторов: ' + str(metrics.accuracy_score(test_y, Y)))

    # наивный байес
    NB = BernoulliNB()
    NB.fit(train_x, train_y)
    Y = NB.predict(test_x)

    if b:
        clf_report = classification_report(test_y, Y, target_names=name, output_dict=True)
        sns.heatmap(pd.DataFrame(clf_report).iloc[:-1, :].T, annot=True, cmap= 'cividis')
        plt.show(sns)

    print('наивный байес: ' + str(metrics.accuracy_score(test_y, Y)))

    # дерево решений
    clf = DecisionTreeClassifier()
    clf.fit(train_x, train_y)
    tree.plot_tree(clf)
    Y = clf.predict(test_x)

    if b:
        clf_report = classification_report(test_y, Y, target_names=name, output_dict=True)
        sns.heatmap(pd.DataFrame(clf_report).iloc[:-1, :].T, annot=True, cmap= 'cividis')
        plt.show(sns)

    print('дерево решений: ' + str(metrics.accuracy_score(test_y, Y)))

    joblib.dump(svc, 'Model/' + name_file + '.pkl')
    print("\nМодель сохранена в файл " + 'Model/' + name_file + '.pkl')

    joblib.dump(vector, 'Model/' + name_file + '_vec.pkl')
    print("TfidfVectorizer сохраненн в файл " + 'Model/' + name_file + '_vec.pkl')

    joblib.dump(encoder.classes_, 'Model/' + name_file + '_enc.joblib')
    print("LabelEncoder сохранен в файл " + 'Model/' + name_file + '_enc.joblib')


train('model', False)

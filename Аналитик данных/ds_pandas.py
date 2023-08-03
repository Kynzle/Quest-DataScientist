import pandas as pd
import matplotlib.pyplot as plt
import matplotlib # для задания отступа графика от левого края формы

# 1 ИЗВЛЕЧЕНИЕ ДАННЫХ
# Чтение файла
df = pd.read_csv('events.csv')

# Первоначальный просмотр данных файла
print(df.head())
print('\n')

# 2. ПОДГОТОВКА ДАННЫХ
# 2.1 Проверка на пустые значения в столбцах
print ('\n---- Информация о созданом "df"  ------------------')
print(df.info())
'''Вывод. Пустых значений нет. 
Столбцы visit_date,URL_visited, user_reg_date представлены в виде, неудобном для анализа. 
Например, для анализа активности пользователей в разные периоды времени необходимо формировать новые столбцы. 
Для полноценного анализа данных о пользователях, которые перестали учиться, на платформе не хватает информации 
о том, на какие курсы они были записаны и на какой период времени был рассчитан срок их обучения. '''

# 2.2 Преобразование текстовых столбцов c заменой отсутствующих позиций
# 2.2.1 Формирование нового столбца 'day' 
def get_day(data):
    return data[0:2]
df['day'] = df['visit_date'].apply(get_day)
print ('\n---- Новый столбец "day"  ------------------')
print(df['day'].head(5))

# 2.2.2 Формирование нового столбца 'month' 
def get_month(data):
    return data[3:5]
df['month'] = df['visit_date'].apply(get_month)
print ('\n---- Новый столбец "month"  ------------------')
print(df['month'].head(5))

# 2.2.3 Формирование нового столбца 'format' 
# Столбец формат содержит подстроку из столбца 'URL_visited', который находится между 4 и 5 слэшем ('/')
# Пустые значения и пустые строки заменяем на  'without format'
# Решение о включении в выдачу полей со значением 'without format' зависит от условия задачи
# В нашем случае условий нет. Решаем не включать

def format(url):
    data = url.split('/')
    if len(data) < 5:
        str_val = 'without format'
    else:
        if data[4] =='':
            str_val = 'without format'
        else:
            str_val = data[4]
    return str_val
df['format'] = df['URL_visited'].apply(format)
print ('\n---- Новый столбец "format"  ------------------')
print(df['format'].head(5))

# 2.2.4 Формирование нового столбца 'material' 
# Столбец materialсодержит подстроку из столбца 'URL_visited', который находится между 5 и 6 слэшем ('/')
def material(url):
    data = url.split('/')
    if len(data) < 6:
        str_val = 'without material'
    else:
        if data[5] =='':
            str_val = 'without material'
        else:
            str_val = data[5]
    return str_val
df['material'] = df['URL_visited'].apply(material)
print ('\n---- Новый сталбец "material"  ------------------')
print(df['material'].head(5))

# 2.2.5 Формирование нового столбца 'submaterial' 
# Столбец submaterial содержит подстроку из столбца 'URL_visited', который находится между 7 и 8 слэшем ('/')
def submaterial(url):
    data = url.split('/')
    str_val = 'without material'
    if len(data) == 6:
        str_val = 'the only one lesson'+'  ('+ data[5]+')'    
    if len(data) == 8:
        if data[7] =='':
            str_val = 'the only one lesson'+'  ('+ data[5]+')'
        else:
            str_val = data[7]+'  ('+ data[5]+')'
    return str_val
df['submaterial'] = df['URL_visited'].apply(submaterial)
print ('\n---- Новый сталбец "submaterial"  ------------------')
print(df['submaterial'].head(5))

# 2.3 Проверка  пустых значений в 5 созданных столбцах
print ('\n---- Проверка  пустых значений в 5 созданных столбцах  ------------------')
print(df.info())

# 3 ПРОВЕДЕНИЕ ИССЛЕДОВАНИЙ (НА ВЫБОР)

# 3.1
print ('\n---- Рейтинг месяцев по количеству посещений сайта ------------------')
dt_tmp_1 =df.groupby('month')['user_id'].count().sort_values(ascending=False)
print(dt_tmp_1)

# 3.2
print ('\n---- Количество посещений по дням (февраль) ------------------')
dt_tmp_2 = df[(df['month']=='02')].groupby('day')['user_id'].count() 
print(dt_tmp_2)

# 3.3
print ('\n---- Рейтинг 10 пользователей по количеству посещений в феврале (user ID) ------------------')
dt_tmp_3 = df[(df['month']=='02')].groupby('user_id')['user_id'].count().sort_values(ascending=False)
print (dt_tmp_3.head(10))

# 3.4
print ('\n---- Статистика посещений за один день в феврале ------------------')
dt_tmp_4 = df[(df['month']=='02')].groupby('day')['user_id'].count().agg(['min','mean', 'max'])
print (dt_tmp_4.head(10))

# 3.5
print ('\n---- Рейтинг посещаемости по разделам ------------------')
dt_tmp_5 = df[df['format']!='without format']['format'].value_counts()
print (dt_tmp_5.head(10))

# 3.6
print ('\n---- Рейтинг 10 самых посещаемых курсов (courses)---------------------------------------')
dt_tmp_6 = df[(df['format']=='courses') & (df['material']!='without material')].groupby(['material'])['user_id'].count().sort_values(ascending=False)
print (dt_tmp_6.head(10))

# 3.7
print ('\n---- Рейтинг 10  самых посещаемых уроков ---------------------------------------')
dt_tmp_7 = df[(df['format']=='courses') & (df['submaterial']!='without material')].groupby(['submaterial'])['user_id'].count().sort_values(ascending=False)
print (dt_tmp_7.head(10))

# 3.8
print ('\n---- Рейтинг 10 самых посещаемых видео (номера)---------------------------------------')
dt_tmp_8 = df[df['format']=='video'].groupby(['material'])['user_id'].count().sort_values(ascending=False)
print (dt_tmp_8.head(10))

# 3.9
print ('\n---- Рейтинг 10 самых посещаемых направлений (trajectory)---------------------------------------')
dt_tmp_9 = df[df['format']=='trajectory'].groupby(['material'])['user_id'].count().sort_values(ascending=False)
print (dt_tmp_9.head(10))

# 3.10
print ('\n---- Рейтинг посещений по категориям (category)---------------------------------------')
dt_tmp_10 = df[df['format']=='category'].groupby(['material'])['user_id'].count().sort_values(ascending=False)
print (dt_tmp_10.head(10))

# 4 ВИЗУАЛИЗАЦИЯ (НА ВЫБОР)

dt_tmp_1.plot(kind = 'barh',title='Рейтинг месяцев по количеству посещений в месяц')
plt.show()

dt_tmp_2.plot(kind = 'line',title='Количество посещений по дням (февраль)')
plt.show()

dt_tmp_4.plot(kind = 'barh',title='Статистика посещений за один день в феврале')
plt.show()

matplotlib.rcParams['figure.subplot.left'] = 0.3 # отступ графика от левого края формы
dt_tmp_5.plot(kind = 'barh',title='Рейтинг посещаемости по разделам')
mng = plt.get_current_fig_manager() # максимизация окна графика
mng.window.showMaximized() 
plt.show()

matplotlib.rcParams['figure.subplot.left'] = 0.4 # отступ графика от левого края формы
dt_tmp_6.iloc[0:10].plot(kind = 'barh',title='Рейтинг 10 самых посещаемых курсов ')
mng = plt.get_current_fig_manager() # максимизация окна графика
mng.window.showMaximized()  
plt.show()

matplotlib.rcParams['figure.subplot.left'] = 0.6
dt_tmp_7.iloc[0:10].plot(kind = 'barh',title='Рейтинг 10 самых посещаемых  уроков ')
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
plt.show()

matplotlib.rcParams['figure.subplot.left'] = 0.2
dt_tmp_8.iloc[0:10].plot(kind = 'barh',title='Рейтинг 10 самых посещаемых видео (номера)')
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
plt.show()

dt_tmp_9.iloc[0:10].plot(kind = 'barh',title='Рейтинг 10 самых посещаемых направлений (trajectory)')
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
plt.show()

dt_tmp_10.iloc[0:10].plot(kind = 'barh',title='Рейтинг посещения по категориям (category)')
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
plt.show()
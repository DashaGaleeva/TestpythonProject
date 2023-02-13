import sqlite3

global data, columns
data = []
columns = ('id','name', 'age', 'gender', 'crime', 'execution_method', 'year')

database = sqlite3.connect('victims.db')
cursor = database.cursor()

def read(filename):
#пришлось добавить кодировку принудительно
    with open(filename, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.split(',')
            line = (int(line[0]), line[1], int(line[2]), line[3], line[4], line[5], int(line[6].replace('\n', '')))
            data.append(line)

def write(filename):
    with open(filename, 'w') as file:
        for line in data:
            line = ','.join([str(i) for i in line]) + '\n'
            file.write(line)

def build_database():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
        victims
        (
            id INT,
            name TEXT,
            age INT,
            gender TEXT,
            crime TEXT,
            execution_method TEXT,
            year INT
        );
    ''')
    database.commit()

def add_to_database(data):
    for line in data:
        if line not in cursor.execute('SELECT * FROM victims'):
            cursor.execute(f'INSERT INTO victims VALUES(?,?,?,?,?,?,?)', line)
            print(f'Жертва {line} внесена в базу данных')
        else:
            print(f'Жертва {line} уже есть в базе данных')
    database.commit()

def remove_from_database(key, value):
    cursor.execute(f'DELETE FROM victims WHERE {key}={value}')
    print(f'Жертва с {key} = {value} удалена из базы данных')
#прочитаем файл с данными
read('victims.txt')
#создадим и заполним базу данных
build_database()
add_to_database(data)
#выведем записи базы данных
for n in list(cursor.execute('SELECT * FROM victims')):
    print(n)

#отберем жертв старше 60 и выведем данные в файл

data = cursor.execute('SELECT * FROM victims WHERE age>60')
write('old.txt')

#удалим из базы жертву с id = 1
remove_from_database('id', 1)

#выведем оставшиеся записи
for n in list(cursor.execute('SELECT * FROM victims')):
    print(n)
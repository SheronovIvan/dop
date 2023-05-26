import pymongo

"""
 код, значение не будет временно инициализировано
"""

f = open('codeTest.txt','r')
res = f.read().replace('\n','').replace('\t','').replace('  ',' ')
res_lst = list(res)
print(res)
p = 0 # Инициализировать указатель позиции

def check_code():
    # Инициализация
    result = []
    str_get = []
    ch = get_char()
    new_ch = get_blank_ch(ch)
    # Идентификационный идентификатор
    if  new_ch.isalpha() or new_ch == '_' or new_ch == '$':
        str_get.append(new_ch)
        new_ch = get_char()
        while new_ch.isalpha() or new_ch.isdigit() or new_ch == '_' or new_ch == '$':
            str_get.append(new_ch)
            new_ch = get_char()
        retract_pointer()
        str_result = ''.join(str_get)
        code = is_reserved_word(str_result)
        if code == 0 :
            value = insert_identifier(str_result)
            result.append('2') # Здесь 2 используется как код типа идентификатора незарезервированного слова
            result.append(value)
            return result
        else:
            result.append('1') # Здесь 1 используется как код категории зарезервированного слова
            result.append(str_result) # В экспериментальном примере значением является само зарезервированное слово
            """
                         result.append ('-') # Зарезервированные слова не имеют собственного значения
            """
            return result
    # Определить целочисленные константы
    elif new_ch.isdigit():
        str_get.append(new_ch)
        new_ch = get_char()
        while new_ch.isdigit():
            str_get.append(new_ch)
            new_ch = get_char()
        retract_pointer()
        str_result = ''.join(str_get)
        value = insert_constant(str_result)
        result.append('3') # Здесь 3 используется как код категории целочисленной константы
        result.append(value)
        return result
    #Identification Operator
    elif new_ch == '=' or new_ch == '+' or new_ch == '-' or new_ch == '*' or new_ch == '/' or new_ch == '>'\
        or new_ch == '<' or new_ch == '!' or new_ch == '%':
        if new_ch == '>' or new_ch == '<' or new_ch == '!':
            str_get.append(new_ch)
            value = ''.join(new_ch)
            new_ch = get_char()
            if new_ch == '=':
                str_get.append(new_ch)
                str_result = ''.join(str_get)
                result.append('4') # Здесь используйте 4 как код типа оператора
                result.append(str_result)
                return result
            else:
                retract_pointer()
                result.append('4')
                result.append(value)
                return result
        elif new_ch == '*':
            str_get.append(new_ch)
            value = ''.join(new_ch)
            new_ch = get_char()
            if new_ch == '*':
                str_get.append(new_ch)
                str_result = ''.join(str_get)
                result.append('4')
                result.append(str_result)
                return result
            else:
                retract_pointer()
                result.append('4')
                result.append(value)
                return result
        else:
            value = ''.join(new_ch)
            result.append('4')
            result.append(value)
            return  result
    # Определить разделитель
    elif new_ch == ',' or new_ch == ';' or new_ch == '{' or new_ch == '}' or new_ch == '(' or new_ch == ')':
        value = ''.join(new_ch)
        result.append('5') # Используйте 5 как код категории разделителя
        result.append(value)
        return result
    else:
        result.append("Error.")
        return result

# Читать следующий символ в new_ch
def get_char():
    global p
    temp_ch = res_lst[p]
    p += 1
    return temp_ch

# Пропускаем пробел, пока ch не прочитает не пробел
def get_blank_ch(temp_ch_1):
    if temp_ch_1 == ' ':
        temp_ch_2 = get_char()
        return temp_ch_2
    return temp_ch_1

# Подключаем символы в ch к str_get
def ch_append():
    # Вызов функции Python напрямую
    return

# Проверяем, есть ли str_get в таблице зарезервированных слов, если она существует, возвращает 1, в противном случае возвращает 0
def is_reserved_word( str_result ):
    check_client = pymongo.MongoClient("mongodb://localhost:27017/")
    check_db = check_client["PrincipleOfCompiler"]
    check_col = check_db["ReservedWord"]
    check_query = {"content" : str_result}
    for get_text in check_col.find(check_query):
        # Определяем, является ли сопоставленный get_text пустым, если он не пуст, строка для сопоставления находится в списке зарезервированных слов
        if any(get_text):
            check_client.close()
            return 1
    """
    check_doc = check_col.find(check_query)
    print(check_doc)
    for res in check_doc:
        print(res)
    """
    check_client.close()
    return 0

# Обратный вызов указателя поиска на позицию символа
def retract_pointer():
    global p
    p -= 1
    return

# Если распознается как идентификатор, вставить идентификатор в str_result в таблицу символов и вернуть указатель таблицы символов
def insert_identifier( str_result ):
    return str_result

# Если распознается как константа, вставить константу в str_result в таблицу констант и вернуть указатель таблицы параметров
def insert_constant( str_result ):
    return str(bin(int(str_result)))

while p in range(len(res_lst)):
    print(check_code())
f.close()

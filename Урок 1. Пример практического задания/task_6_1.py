"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но отерыть нужно ИМЕННО в формате Unicode (utf-8)

например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""

from chardet import detect

with open('test.txt', encoding='utf-8') as file:
    for line in file.read():
        print(line)
#file.close()

# UnicodeDecodeError: 'utf-8' codec can't decode
# byte 0xf0 in position 0: invalid continuation byte


# открываем файл в правильной кодировке
file = open('test.txt', 'rb')
for line in file:
    print(line.decode(encoding='utf-8'))




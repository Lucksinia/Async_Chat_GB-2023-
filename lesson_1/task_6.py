"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

with open(r"lesson_1/test_file.txt", "r", encoding="Latin-1") as test_file:
    for line in test_file.readlines():
        print(f"Строка с кодировкой по умолчанию - {line}", end="")
with open(r"lesson_1/test_file.txt", "r", encoding="utf-8") as test_file:
    for line in test_file:
        print(f"Строка в формате Unicode - {line}", end="")

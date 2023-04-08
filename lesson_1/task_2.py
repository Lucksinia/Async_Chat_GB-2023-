"""
2. Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.
"""

STR_LIST = [b"class", b"function", b"method"]

for el in STR_LIST:
    print(f"{type(el)}:{el}:len = {len(el)}")

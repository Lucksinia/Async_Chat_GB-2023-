"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).
"""

base = ["разработка", "администрирование", "protocol", "standard"]

encoded = []
for el in base:
    el_b = el.encode("utf-8")
    encoded.append(el_b)
print(f"\nencoded: {encoded}")
decoded = []
for el in encoded:
    el_str = el.decode("utf-8")
    decoded.append(el_str)
print(f"\ndecoded:{decoded}")

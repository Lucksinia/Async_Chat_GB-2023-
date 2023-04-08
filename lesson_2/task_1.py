"""
Написать скрипт, осуществляющий выборку определенных данных из
файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.
1. Создать функцию get_data(), для циклического считывания данных. С помошью Regex вытащить значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка. Создать ещё один список для хранения названий столбцов
и второй для хранения их значений.
2. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать
получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий
CSV-файл; Проверить работу программы через вызов функции write_to_csv().
"""

from pathlib import Path
import csv
import re


def get_data():
    path = Path().cwd() / "lesson_2" / "input_data"  # Путь к требуемым файлам
    prod_list = []  # «Изготовитель системы»
    name_list = []  # «Название ОС»
    code_list = []  # «Код продукта»
    type_list = []  # «Тип системы»

    pathdir = list(path.iterdir())
    for filename in pathdir:
        if filename.suffix == ".txt":
            with open(filename, "r", encoding="utf-8") as f:
                file_content = f.read()

                if "Изготовитель системы" in file_content:
                    search_point = re.search(
                        "Изготовитель системы:(.*)\n", file_content
                    )
                    prod_list.append(search_point.group(1).replace(" ", ""))

                if "Название ОС" in file_content:
                    search_point = re.search("Название ОС:(.*)\n", file_content)
                    name_list.append(search_point.group(1).replace(" ", ""))

                if "Код продукта" in file_content:
                    search_point = re.search("Код продукта:(.*)\n", file_content)
                    code_list.append(search_point.group(1).replace(" ", ""))

                if "Тип системы" in file_content:
                    search_point = re.search("Тип системы:(.*)\n", file_content)
                    type_list.append(search_point.group(1).replace(" ", ""))

    main_data = [
        list(i) for i in zip([1, 2, 3], prod_list, name_list, code_list, type_list)
    ]
    return main_data  # [[1, 'LENOVO', 'MicrosoftWindows7Профессиональная', '00971-OEM-1982661-00231', 'x64-basedPC'],..


def write_to_csv(csv_file: Path):
    cols = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]
    rows = get_data()
    with open(csv_file / "output.csv", "w", encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerow(cols)
        for i in rows:
            write.writerow(i)


write_to_csv(Path().cwd() / "lesson_2" / "output_data")

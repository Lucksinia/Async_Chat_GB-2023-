"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
скрипт, автоматизирующий его заполнение данными. Для этого: Создать функцию write_order_to_json(),
в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer),
дата (date). Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных
указать величину отступа в 4 пробельных символа; Проверить работу программы через вызов функции
write_order_to_json() с передачей в нее значений каждого параметра.
"""

import json
import shutil
from pathlib import Path


def write_order_to_json(
    item: str,
    quantity: int,
    price: float,
    buyer: str,
    date: str,
) -> None:
    order = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date,
    }
    copy_path = Path().cwd() / "lesson_2" / "input_data" / "orders.json"
    output_path = Path().cwd() / "lesson_2" / "output_data" / "orders.json"
    if not output_path.exists():
        shutil.copy(copy_path, output_path)
    with open(output_path, "r", encoding="utf-8") as jsonr:
        data = json.load(jsonr)
    with open(output_path, "w", encoding="utf-8") as jsonw:
        orders = data["orders"]
        orders.append(order)
        json.dump(data, jsonw, indent=4, ensure_ascii=False)


write_order_to_json("Beijing Corn", 9, 0.1, "Steven's Dad", "In my Time")
write_order_to_json("Failure", 1, 69.99, "Steven's Dad", "xx.xx.1996")

"""
Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging): клиент отправляет
запрос серверу; сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде
отдельных скриптов, содержащих соответствующие функции. Функции клиента: сформировать presence-сообщение; отправить
сообщение серверу; получить ответ сервера; разобрать сообщение сервера; параметры командной строки скрипта
client.py <addr> [<port>]: addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777. Функции сервера:
принимает сообщение клиента; формирует ответ клиенту; отправляет ответ клиенту; имеет параметры командной строки:
-p <port> — TCP-порт для работы (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по
умолчанию слушает все доступные адреса).

!КЛИЕНТ ЗАПУСКАЕТСЯ ВТОРЫМ
"""
import argparse
from socket import *
from datetime import datetime
import json


def presence(account_name, status):
    data = {
        "action": "presence",
        "time": datetime.timestamp(datetime.now()),
        "type": "status",
        "user": {"account_name": account_name, "status": status},
    }
    return data


def get_addr_port():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", action="store", dest="addr", type=str, default="localhost"
    )
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777)
    parser.add_argument(
        "-user", action="store", dest="user", type=str, default="Daniil"
    )
    parser.add_argument(
        "-status", action="store", dest="status", type=str, default="Constantly Ill"
    )
    return parser.parse_args()


def run():
    print("client starting...")
    args = get_addr_port()
    addr, port, user, status = args.addr, args.port, args.user, args.status
    print(f"parameters = {addr}, {port}, {user}, {status}")
    s = socket(AF_INET, SOCK_STREAM)  # creating TCP
    s.connect((addr, port))  # Соединяемся с сервером
    presence_msg = presence(user, status)  # создаем presencemsg
    s.send(json.dumps(presence_msg, indent=4).encode("utf-8"))
    try:
        data = s.recv(1000000)
        d = json.loads(data.decode("utf-8"))
        print("Сообщение от сервера: ", d["response"], d["alert"])
    except:
        print("Сообщений нет")

    s.close()


if __name__ == "__main__":
    run()

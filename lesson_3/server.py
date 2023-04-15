"""
Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging): клиент отправляет
запрос серверу; сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде
отдельных скриптов, содержащих соответствующие функции. Функции клиента: сформировать presence-сообщение; отправить
сообщение серверу; получить ответ сервера; разобрать сообщение сервера; параметры командной строки скрипта
client.py <addr> [<port>]: addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777. Функции сервера:
принимает сообщение клиента; формирует ответ клиенту; отправляет ответ клиенту; имеет параметры командной строки:
-p <port> — TCP-порт для работы (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по
умолчанию слушает все доступные адреса).
"""
import argparse
import json
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime


def get_params():
    """get parameters of port and IP-adress

    :return: returns parametrs as a namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777)
    parser.add_argument("-a", action="store", dest="addr", type=str, default="")
    return parser.parse_args()


def run():
    """server starting and parsing logic in a mainloop"""
    print("server start...")
    args = get_params()
    addr = args.addr
    port = args.port
    print(f"server params = addr: {addr}, port {port}")
    s = socket(AF_INET, SOCK_STREAM)  # TCP
    s.bind((addr, port))
    s.listen(5)  # five clients max

    while True:
        # mainloop
        client, addr = s.accept()
        data = client.recv(1000000)
        d = json.loads(data.decode("utf-8"))
        if d["action"] == "presence":
            print("Получено presence-сообщение от клиента")
            print(d)
            msg_to_client = {
                "response": 200,
                "time": datetime.timestamp(datetime.now()),  # from 1970-01-01
                "alert": "Code 200",
            }
            msg = json.dumps(msg_to_client, indent=4).encode("utf-8")
            client.send(msg)
            print(
                "Сообщение: ",
                msg.decode("utf-8"),
                ", было отправлено клиенту: ",
                addr,
                port,
            )

        client.close()


if __name__ == "__main__":
    run()

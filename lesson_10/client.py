import argparse
import time
import json
import logging
from socket import *
from datetime import datetime
from dis import get_instructions
from log.logging_decorator import log
from threading import Thread

client_log = logging.getLogger("client")

"""
Lesson 10. 
1. Реализовать метакласс ClientVerifier, выполняющий базовую проверку класса «Клиент» (для некоторых
проверок уместно использовать модуль dis): отсутствие вызовов accept и listen для сокетов; использование сокетов
для работы по TCP; отсутствие создания сокетов на уровне классов, то есть отсутствие конструкций такого вида: class
Client: s = socket() ...
"""


@log
def presence(account_name, status):
    data = {
        "action": "presence",
        "time": datetime.timestamp(datetime.now()),
        "type": "status",
        "user": {"account_name": account_name, "status": status},
    }
    return data


@log
def message_to_server(message, account_name):
    data = {
        "action": "message",
        "time": datetime.timestamp(datetime.now()),
        "text": message,
        "user": {"account_name": account_name},
    }
    return data


@log
def data_from_server(sock):
    received_data = sock.recv(10000000)
    decoded_data = received_data.decode("utf-8")
    result_data = json.loads(decoded_data)
    if type(result_data) == dict:
        return result_data
    return {}


@log
def send_data(data, sock):
    result_data = json.dumps(data).encode("utf-8")
    sock.send(result_data)


@log
def get_addr_port():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", action="store", dest="addr", type=str, default="localhost"
    )
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777)
    parser.add_argument(
        "--user", action="store", dest="user", type=str, default="Daniil"
    )
    parser.add_argument(
        "--status", action="store", dest="status", type=str, default="Constantly Ill"
    )
    # is a flag factually
    # parser.add_argument("--send", action="store", dest="send", type=int, default=0)
    client_log.debug("Function get_addr_port starting...")
    return parser.parse_args()


@log
def create_socket_client(addr, port):
    # Connection rewritten as try\exept statment
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect((addr, port))
        client_log.debug(f"Create socket client. Connect to server: {addr}, {port}")
        return s
    except ConnectionRefusedError as e:
        client_log.error("Can't connect to server. Maybe wrong port?")
        exit(1)


@log
def read_answer(dict_from_server):
    try:
        response_code = dict_from_server.get("response", 0)
    except Exception as err:
        client_log.error(f"Error {err})")
    else:
        if response_code:
            if response_code == 200:
                result_msg = dict_from_server.get("alert", "OK.")
                client_log.info("Response status OK")
                try:
                    result_msg = dict_from_server.get("text", 0)
                except Exception as err:
                    client_log.error(f"Error {err})")
                else:
                    if result_msg:
                        return f"{result_msg[0]} by {result_msg[1]}"
            else:
                result_msg = dict_from_server.get("error", "unknown error")
                client_log.info(f"Status: {response_code}: {result_msg}")
            return f"{response_code}: {result_msg}"
        client_log.error(f"Data : {dict_from_server}")
    return ""


def chat_read(sock):
    while True:
        try:
            data = data_from_server(sock)
            answer = read_answer(data)
            print(answer)
            client_log.info(f"Message received: {answer} ")
        except Exception as err:
            client_log.error(f"Some errors: {err}")
            exit(1)


def chat_write(user, s):
    while True:
        message = input(f">>>{user}\n")
        try:
            send_data(message_to_server(message, user), s)
        except Exception as err:
            client_log.error(f"Some errors: {err}")


def run():
    client_log.info("client.py start...")
    args = get_addr_port()
    addr, port, user, status = args.addr, args.port, args.user, args.status
    client_log.info(f"parameters = {addr}, {port}, {user}, {status}")
    s = create_socket_client(addr, port)
    presence_msg = presence(user, status)
    client_log.info("Presence message sending start...")
    s.send(json.dumps(presence_msg, indent=4).encode("utf-8"))
    client_log.info("Presence message sending...DONE")
    # Slightly less mess of a msg parser
    try:
        data = data_from_server(s)
        answer = read_answer(data)
        print(f"Message(answer) from server received: ", answer)

    except:
        client_log.error("No messages from server.")
        exit(1)

    w = Thread(target=chat_write, args=(user, s))
    w.daemon = True
    w.start()

    r = Thread(target=chat_read, args=(s,))
    r.daemon = True
    r.start()

    while True:
        time.sleep(1)
        if not w.is_alive() or not r.is_alive():
            break


if __name__ == "__main__":
    run()

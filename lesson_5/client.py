import argparse
from socket import *
from datetime import datetime
import json
import logging
from log import client_log_config

client_log = logging.getLogger("client")
print(client_log)


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
    client_log.debug("Function get_addr_port starting...")
    return parser.parse_args()


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


def read_answer(dict_from_server):
    # Reading msg from server with logging
    client_log.info("Reading answer from server(func read_answer)")
    return dict_from_server["response"], dict_from_server["alert"]


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
    try:
        data = s.recv(1000000)
        d = json.loads(data.decode("utf-8"))
        answer = read_answer(d)
        client_log.info("Message(answer) from server received. ")
        print("Сообщение от сервера: ", answer)
        s.close()
    except:
        client_log.error("No messages from server.")
        s.close()
    s.close()


if __name__ == "__main__":
    run()

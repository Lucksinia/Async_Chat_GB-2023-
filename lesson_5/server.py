import argparse
import json
import logging
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
from log import server_log_config
from log.logging_decorator import log

server_log = logging.getLogger("server")
print(server_log)


@log
def get_params():
    """get parameters of port and IP-adress

    :return: returns parametrs as a namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777)
    parser.add_argument("-a", action="store", dest="addr", type=str, default="")
    return parser.parse_args()


@log
def create_socket_server(addr, port):
    print(f"server params = addr: {addr}, port: {port}")
    server_log.info(f"Create socket server. Server params -- addr: {addr}, port {port}")
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    return s


@log
def msg_to_client(d, client):
    if d["action"] == "presence":
        msg = {
            "response": 200,
            "time": datetime.timestamp(datetime.now()),
            "alert": "200 OK",
        }
        msg = json.dumps(msg, indent=4).encode("utf-8")
        client.send(msg)
        server_log.info('Msg send to client. "response": 200')


def run():
    """server starting and parsing logic in a mainloop"""
    server_log.info("server.py start...")
    args = get_params()
    addr = args.addr
    port = args.port
    s = create_socket_server(addr, port)

    while True:
        client, addr = s.accept()
        try:
            data = client.recv(1000000)
            d = json.loads(data.decode("utf-8"))
            server_log.info("Resived presence-msg from client")
            msg_to_client(d, client)
            client.close()
        except Exception as err:
            server_log.error("Error:", err)
            server_log.error("Wrong data from client")
            client.close()
        client.close()


if __name__ == "__main__":
    run()

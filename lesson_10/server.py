import argparse
import json
import logging
import select
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
from dis import get_instructions
from log.logging_decorator import log

server_log = logging.getLogger("server")


class ServerPort:
    def __set__(self, instance, value):
        if not 1024 < value < 65535:
            raise ValueError(f"Wrong port: {value}")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class ServerVerifier(type):
    def __init__(cls, classname, bases, dict):
        for func in dict:
            try:
                instructions = get_instructions(dict[func])
            except TypeError:
                pass
            else:
                for op in instructions:
                    if op.opname == "LOAD_GLOBAL":
                        if op.argval in ("accept", "listen"):
                            raise TypeError(f"{op.argval} cant use in class Server")

        super().__init__(classname, bases, dict)


class Server(metaclass=ServerVerifier):
    port = ServerPort()

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port

    @staticmethod
    def create_socket_server(addr, port):
        print(f"server params = addr: {addr}, port: {port}")
        server_log.info(
            f"Create socket server. Server params -- addr: {addr}, port {port}"
        )
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((addr, port))
        s.listen(5)
        s.settimeout(1)
        return s

    @log
    def read_requests(self, r_clients, all_clients):
        responses = {}  # dict{socket:query}
        for sock in r_clients:
            try:
                data = sock.recv(1024).decode("utf-8")
                responses[sock] = data
            except:
                server_log.info(
                    f"Client {sock.fileno()} {sock.getpeername()} disconnected"
                )
                all_clients.remove(sock)
        return responses

    @log
    def presence_reaction(self, d):
        msg = {
            "response": 200,
            "time": datetime.timestamp(datetime.now()),
            "alert": "OK",
        }
        msg = json.dumps(msg, indent=4).encode("utf-8")
        return msg

    @log
    def write_responses(self, requests, w_clients, all_clients, chat):
        for client in w_clients:
            if client in requests:
                resp = requests[client].encode("utf-8")
                recipients = all_clients.copy()
                recipients.remove(client)
                if resp != b"":
                    d = json.loads(resp.decode("utf-8"))
                    try:
                        if d["action"] == "presence":
                            client.send(self.presence_reaction(d))
                        if d["text"]:
                            chat.append([d["text"], d["user"]["account_name"]])
                            for clnt in recipients:
                                data = {
                                    "response": 200,
                                    "action": "message",
                                    "time": datetime.timestamp(datetime.now()),
                                    "text": chat[0],
                                }
                                try:
                                    self.send_data(data, clnt)

                                except:
                                    print(
                                        "Клиент {} {} отключился".format(
                                            client.fileno(), client.getpeername()
                                        )
                                    )
                                    client.close()
                            del chat[0]
                    except:
                        pass

    @log
    def send_data(self, data, sock):
        result_data = json.dumps(data).encode("utf-8")
        sock.send(result_data)

    @log
    def run(self):
        """server starting and parsing logic in a mainloop"""
        server_log.info("server.py start...")
        chat = []
        clients = []
        s = self.create_socket_server(self.addr, self.port)

        while True:
            try:
                conn, addr = s.accept()  # Check timeout
            except OSError as e:
                pass  # timeout
            else:
                print("Connection from %s" % str(addr))
                clients.append(conn)
            finally:
                # test for events
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(clients, clients, [], wait)
                except:
                    pass  # client disconnected
                requests = self.read_requests(r, clients)
                if requests:
                    self.write_responses(requests, w, clients, chat)
                if chat:
                    for client in clients:
                        data = {
                            "response": 200,
                            "action": "message",
                            "time": datetime.timestamp(datetime.now()),
                            "text": chat[0],
                        }
                        self.send_data(data, client)
                    del chat[0]


@log
def get_params():
    """get parameters of port and IP-adress

    :return: returns parametrs as a namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777)
    parser.add_argument("-a", action="store", dest="addr", type=str, default="")
    args = parser.parse_args()
    addr = args.addr
    port = args.port
    return addr, port


if __name__ == "__main__":
    server = Server(*get_params())
    server.run()

import argparse
import json
import logging
import select
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
from log.logging_decorator import log

server_log = logging.getLogger("server")


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
    s.settimeout(1)
    return s


@log
def read_requests(r_clients, all_clients):
    responses = {}  # dict{socket:query}
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except:
            server_log.info(f'Client {sock.fileno()} {sock.getpeername()} disconnected')
            all_clients.remove(sock)
    return responses


@log
def presence_reaction(d):
    msg = {
        "response": 200,
        "time": datetime.timestamp(datetime.now()),
        "alert": "OK"
    }
    msg = json.dumps(msg, indent=4).encode('utf-8')
    return msg
        

@log
def write_responses(requests, w_clients, all_clients, chat):
    for client in w_clients:
        if client in requests:
            resp = requests[client].encode('utf-8')
            recipients = all_clients.copy()
            recipients.remove(client)
            if resp != b'':
                d = json.loads(resp.decode('utf-8'))
                try:
                    if d['action'] == 'presence':
                        client.send(presence_reaction(d))
                    if d['text']:
                        chat.append([d['text'], d['user']['account_name']])
                        for clnt in recipients:
                            data = {
                                "response": 200,
                                "action": "message",
                                "time": datetime.timestamp(datetime.now()),
                                "text": chat[0],
                            }
                            try:
                                send_data(data, clnt)

                            except:
                                print('Клиент {} {} отключился'.format(client.fileno(), client.getpeername()))
                                client.close()
                        del chat[0]
                except:
                    pass


@log
def send_data(data, sock):
    result_data = json.dumps(data).encode('utf-8')
    sock.send(result_data)


def run():
    """server starting and parsing logic in a mainloop"""
    server_log.info("server.py start...")
    args = get_params()
    addr = args.addr
    port = args.port
    chat = []
    clients = []
    s = create_socket_server(addr, port)

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
            requests = read_requests(r, clients)
            if requests:
                write_responses(requests, w, clients, chat)
            if chat:
                for client in clients:
                    data = {
                        "response": 200,
                        "action": "message",
                        "time": datetime.timestamp(datetime.now()),
                        "text": chat[0],
                    }
                    send_data(data, client)
                del chat[0]


if __name__ == "__main__":
    run()

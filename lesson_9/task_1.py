"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых
узлов. Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или
ip-адресом. В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего
сообщения («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью
функции ip_address().
"""
from string import punctuation
from subprocess import check_output, STDOUT
from socket import gethostbyname
from ipaddress import ip_address
from platform import system


def host_ping(list_addr):
    """hosting ping addresses
    :param list_addr:
    :return: dict {'Reachable': [], 'Unreachable': []}
    """
    param = "-n 1" if system().lower() == "windows" else "-c"
    result = {"Reachable": [], "Unreachable": []}
    for addr in list_addr:
        try:
            s = addr.translate(str.maketrans("", "", punctuation))
            if s.isdigit():  # then ip-addres
                address = ip_address(addr)
            else:
                address = ip_address(gethostbyname(addr))
            args = "ping " + param + " " + str(address)
            con_out = check_output(args, shell=True, stderr=STDOUT).decode("cp866")
            if con_out:
                # print(f'Узел доступен: {addr}')
                result["Reachable"].append(addr)
        except Exception:
            # print(f'Узел недоступен: {addr}')
            result["Unreachable"].append(addr)
            pass
    return result


if __name__ == "__main__":
    host_ping(["8.8.8.8", "127.0.0.1", "111.22.33.44.55", "youtube.com"])

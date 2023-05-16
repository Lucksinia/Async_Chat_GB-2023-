"""
Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только
последний октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.

Октет — 8-битный номер, 4 из которых составляют 32-битный IP-адрес. Они имеют диапазон 00000000-11111111,
соответствующий десятичным значениям 0–255.
"""
from task_1 import host_ping


def host_range_ping(ip_addr, rng):
    octets = ip_addr.split(".")
    last = int(octets[-1])
    result = [ip_addr]
    for numbers in range(rng):
        result_oct = last + (numbers + 1)
        octets[-1] = result_oct
        s = ".".join(str(x) for x in octets)
        result.append(s)
    return host_ping(result)


if __name__ == "__main__":
    host_range_ping("127.0.0.251", 5)

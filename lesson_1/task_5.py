"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.
"""
import subprocess
import platform

sites = ["yandex.ru", "www.youtube.com"]
for site in range(len(sites)):
    ping = subprocess.Popen(
        ["ping", "-n", "4", sites[site]],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for line in ping.stdout:
        match platform.system():
            case "Windows":
                print(line.decode("cp866"))
            case "Linux":
                print(line.decode("utf-8"))

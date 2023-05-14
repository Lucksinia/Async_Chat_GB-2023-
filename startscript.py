from subprocess import Popen, CREATE_NEW_CONSOLE
# !Does not work in VScode
client_list = []
while True:
    user = input("start test clients(s) / Close test clients (x) / Quit(q): ")
    if user == "q":
        break
    elif user == "s":
        client_list.append(
            Popen(
                "python lesson_5\client.py --user NotMe", creationflags=CREATE_NEW_CONSOLE
            )
        )
        client_list.append(
            Popen("python lesson_5\client.py --user Daniil", creationflags=CREATE_NEW_CONSOLE)
        )
        print(f"Started {len(client_list)}")
    elif user == "x":
        for p in client_list:
            p.kill()
        client_list.clear()

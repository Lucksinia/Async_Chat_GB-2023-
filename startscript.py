from subprocess import Popen, CREATE_NEW_CONSOLE
# !Does not work in VScode
client_list = []
while True:
    user = input(
        "start clients(s) / Close clients (x) / Start N clients(add) / Quit(q): "
    )
    match user:
        case "q":
            break
        case "s":
            client_list.append(
                Popen(
                    "python lesson_5\client.py --user NotMe",
                    creationflags=CREATE_NEW_CONSOLE,
                )
            )
            client_list.append(
                Popen(
                    "python lesson_5\client.py --user Daniil",
                    creationflags=CREATE_NEW_CONSOLE,
                )
            )
            print(f"Started {len(client_list)}")
        case "add":
            chaters_number = input("Input number of clients: ")
            if chaters_number.isdigit():
                print("starting")
                for i in range(int(chaters_number)):
                    client_list.append(
                        Popen(
                            f"python lesson_5\client.py --user Client{i + 1} --status {i+1}",
                            creationflags=CREATE_NEW_CONSOLE,
                        )
                    )
            else:
                print("try again")
        case "x":
            for p in client_list:
                p.kill()
            client_list.clear()

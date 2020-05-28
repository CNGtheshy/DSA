import UserInfo


class LogManager:
    def __init__(self):
        self.current_user_index = -1
        pass

    def signUp(self, users, email, password=""):
        self.current_user_index = users.addUser(email, password)
        return self.current_user_index

    def logIn(self, users, email, password):
        status = users.checkUser(email, password)
        self.current_user_index = status if status >= 0 else -1
        return status


if __name__ == "__main__":
    users = UserInfo.Users()
    log = LogManager()
    current_user = "Guest"
    while True:
        option = input("{0}:~$ ".format(current_user))
        if option == "quit" or option == "exit":
            print('Thanks for using. Bye-bye~')
            break
        elif "sign" in option:
            flag = False
            args = option[4:].split()
            if len(args) and (args[0] == '-u' or args[0] == '--username'):
                if args[2] == '-p' or args[2] == '--password':
                    log.signUp(users, args[1], args[3])
                else:
                    log.signUp(users, args[1])
                flag = True
            else:
                print("[ERROR]: INPUT ERROR -- please input username at least!")
            if flag:
                current_user = args[1]
        else:
            print('[ERROR]: INPUT ERROR -- Invalid input!')
    pass
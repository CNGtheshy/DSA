import LogManager
import UserInfo


class LogForm(LogManager.LogManager):
    def __init__(self):
        super().__init__()
        self.log = LogManager.LogManager()
        self.current_user = "Guest"

    def analyse(self, users, command):
        if "sign" in command:
            args = command[4:].split()

            # valid checking
            if len(args) & 1:
                print("[ERROR]: INPUT ERROR -- you entered invalid options!")
                return -1
            for i in range(len(args)):
                if '-' in args[i] and ('p' not in args[i] and 'u' not in args[i]):
                    print("[ERROR]: INPUT ERROR -- you entered invalid options!")
                    return -1

            if len(args) and (args[0] == '-u' or args[0] == '--username'):
                if args[2] == '-p' or args[2] == '--password':
                    self.signUp(users, args[1], args[3])
                else:
                    self.signUp(users, args[1])
            else:
                print("[ERROR]: INPUT ERROR -- please input username at least!")
                return -2
            if self.current_user_index != -1:
                self.current_user = args[1]
                print('Congratulations! Sign up successfully.')
                return len(users.user_list)-1
            else:
                # account exists
                return -3
        else:
            if "logout" in command:
                self.current_user = "Guest"
                return -3
            args = command[4:].split()
            # valid checking
            if len(args) != 4:
                print("[ERROR]: INPUT ERROR -- you must enter both account and password!")
                return
            for i in range(len(args)):
                if '-' in args[i] and ('p' not in args[i] and 'u' not in args[i]):
                    print("[ERROR]: INPUT ERROR -- you entered invalid options!")
                    return

            status = users.checkUser(args[1], args[3])
            if status >= 0:
                self.current_user = args[1]
                print("< {0} >: Welcome! ".format(args[1]))
            elif status == -1:
                print("[ERROR]: LOG ERROR -- Account doesn't exists, Sign up firstly please!")
            else:
                print("[ERROR]: LOG ERROR -- please enter right password!")
            return status


if __name__ == '__main__':
    users = UserInfo.Users()
    test = LogForm()
    while True:
        option = input("{0}:~$ ".format(test.current_user))
        if option == "quit" or option == "exit":
            print('Thanks for using. Bye~')
            break
        else:
            test.analyse(users, option)
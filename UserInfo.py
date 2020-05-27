import hashlib
import getpass
import pickle


class User:
    def __init__(self, email, password=""):
        self._email = email
        self._password = hashlib.sha1(password.encode("utf8")).hexdigest()
        self._public_key = []
        self._private_key = []

    def isSelf(self, email, password):
        """
        :param email:
        :param password:
        :return:-1 (email wrong); -2 (password wrong)
        """
        if email != self._email:
            return -1
        if hashlib.sha1(password.encode('utf8')).hexdigest() != self._password:
            return -2
        return 0

    def show(self):
        print('<', self._email, '> : ')
        print('+--------'+'+'+'-'*60+'+'+'-'*60+'+')
        print('|', "index".center(6), '|', "public_key".center(58), '|', "private_key".center(58), '|')
        print('+--------'+'+' + '-' * 60 + '+' + '-' * 60 + '+')
        for i in range(len(self._private_key)):
            print('|', ("{0}".format(i)).center(6), '|', self._public_key[i].center(58), '|', self._private_key[i].center(58), '|')
            print('+--------'+'+' + '-' * 60 + '+' + '-' * 60 + '+')
        if len(self._private_key) == 0:
            print('|', "0".center(6), '|', "None".center(58), '|', "None".center(58), '|')
            print('+--------'+'+' + '-' * 60 + '+' + '-' * 60 + '+')

    def getKeys(self):
        return self._public_key, self._private_key

    def addKey(self, public_key, private_key):
        self._public_key.append(public_key)
        self._private_key.append(private_key)

    def delKey(self, index):
        count_pass = 3
        tmp_pass = getpass.getpass("Please enter your password to confirm del-option again: ")
        while count_pass:
            if hashlib.sha1(tmp_pass.encode('utf8')).hexdigest() == self._password:
                break
            count_pass -= 1
            if count_pass == 0:
                break
            tmp_pass = getpass.getpass("Password error, please Try again: ")
        if count_pass == 0:
            print('Authenticate failed: WRONG PASSWORD!')
            return
        key_num = len(self._public_key)
        if index < 0 or index >= key_num:
            print('[ERROR]: OUT OF INDEX -- there is no matched key in your account and check your Keys again please!')
            return
        self._public_key.pop(index)
        self._private_key.pop(index)
        print('Delete Key successfully!')


class Users:
    def __init__(self):
        self.user_list = []
        try:
            conf_file = open('./conf.ini', 'rb')
            self.user_list = pickle.load(conf_file)
            conf_file.close()
        except:
            conf_file = open('./conf.ini', 'wb')
            conf_file.close()

    def updateFile(self):
        conf_file = open('./conf.ini', 'wb')
        pickle.dump(self.user_list, conf_file)
        conf_file.close()

    def addUser(self, email, password=""):
        tmp_user = User(email, password)
        self.user_list.append(tmp_user)
        print("New user < {0} > Sign Up successfully!".format(email))

    def checkUser(self, email, password):
        for i in range(len(self.user_list)):
            user = self.user_list[i]
            if user.isSelf(email, password) == -1:
                continue
            if user.isSelf(email, password) == -2:
                print('[ERROR]: WRONG PASSWORD -- your password is wrong!')
                return False
            else:
                print("< {0} >: Welcome!".format(email))
                return True
        print('[ERROR]: NO USER -- there is no such user and sign up one please!')


if __name__ == '__main__':
    test = Users()
    test.checkUser('74651665@qq.com', '123456')
    test.updateFile()
    pass
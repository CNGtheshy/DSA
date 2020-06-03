_OPTION_ARG_LESS = -1
_OPTION_ARG_MORE = -2
_OPTION_VALID = -3


class Option:
    def __init__(self, name, args_min_num=1, args_max_num=1, help_text=""):
        self.name = name
        self.args_min_num = args_min_num
        self.args_max_num = args_max_num
        self.args = []
        self.help_text = help_text

    def checkLenValid(self, length):
        if length > self.args_max_num:
            print("[ERROR]: INPUT ERROR -- option -{0} supports up to {1} arguments(s).".format(self.name, self.args_max_num))
            return _OPTION_ARG_MORE
        if length < self.args_min_num:
            print("[ERROR]: INPUT ERROR -- option -{0} needs at least {1} arguments(s).".format(self.name,
                                                                                                self.args_min_num))
            return _OPTION_ARG_LESS
        return _OPTION_VALID


class Command:
    class AttrError(PermissionError):
        pass

    def __init__(self, name="", help_text=""):
        self.name = name
        self.help_text = help_text
        pass

    def __getitem__(self, item):
        if item == 'name' or item == 'help_text':
            return getattr(self, item)
        if hasattr(self, item):
            return getattr(self, item).args
        raise self.AttrError("There is no such attribute named {0}".format(item))

    def addOption(self, option, args_min_num=1, arg_max_num=1, help_text=""):
        setattr(self, option, Option(option, args_min_num, arg_max_num, help_text=help_text))

    def setHelp(self, help_text):
        self.help_text = help_text

    def getAllArgs(self):
        op_arg = {}
        for i in self.__dict__:
            if i == 'name' or i == 'help_text':
                continue
            op_arg[i] = self[i]
        return op_arg

    def showHelp(self):
        print(self.name+'\t\t'+self.help_text)
        print('\t-h\tGet the help text and this option will cover any other options')
        for i in self.__dict__:
            if i == 'name' or i == 'help_text':
                continue
            print('\t-{0}\t{1}'.format(i, self.__dict__[i].help_text))

    def analyseOption(self, option_list):
        if '-h' in option_list:
            self.showHelp()
            return None
        self.clear()
        option = ''
        args = []
        for i in option_list:
            if i[0] == '-' and hasattr(self, i[1:]):
                if args:
                    if getattr(self, option).checkLenValid(len(args)) == _OPTION_VALID:
                        getattr(self, option).args = args
                        args.clear()
                    else:
                        return None
                elif args is [] and option is not '':
                    if getattr(self, i[1:]).checkLenValid(len(args)) == _OPTION_ARG_LESS:
                        return None
                    getattr(self, option).args.append(True)
                option = i[1:]
            elif i[0] == '-' and hasattr(self, i[1:]) is False:
                print("[ERROR]: INPUT ERROR -- Invalid option")
            else:
                args.append(i)
        if getattr(self, option).checkLenValid(len(args)) == _OPTION_VALID:
            if args:
                getattr(self, option).args = args
            else:
                getattr(self, option).args.append(True)
        else:
            return None
        return self

    def clear(self):
        for i in self.__dict__:
            if i == 'name' or i == 'help_text':
                continue
            self.__dict__[i].args.clear()


class Commands:
    class AttrError(PermissionError):
        pass

    def __init__(self):
        pass

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        raise self.AttrError("There is no such attribute named {0}".format(item))

    def addCommand(self, command, option, args_min_num=1, arg_max_num=1, help_text=""):
        if not hasattr(self, command):
            setattr(self, command, Command(command))
        getattr(self, command).addOption(option, args_min_num, arg_max_num, help_text)

    def setCommandHelp(self, command, help_text):
        if not hasattr(self, command):
            setattr(self, command, Command(command))
        getattr(self, command).setHelp(help_text)

    def analyseCommand(self, command):
        options = command.split()
        command_name = options[0]
        if not hasattr(self, command_name):
            print("[ERROR]: INPUT ERROR -- No such command")
            return None
        options = ["x"]+options[1:]+["x"]
        for i in range(len(options)):
            if ',' in options[i]:
                tmp_op = options[i].split(',')
                options = options[:i] + tmp_op + options[i + 1:]
        options = options[1:-1]
        if len(getattr(self, command_name).__dict__) > 2 and options == []:
            print("[ERROR]: INPUT ERROR -- {0} need at least one option".format(command_name))
            return None
        elif not options:
            return getattr(self, command_name)
        return getattr(self, command_name).analyseOption(options)


if __name__ == "__main__":
    commands = Commands()
    commands.addCommand('log', 'u', help_text='need an argument which means your account')
    commands.addCommand('log', 't', args_min_num=0, help_text='set the time or show the time when you choose this option')
    commands.setCommandHelp('ls', "list the users info")
    tmp = commands.analyseCommand("log -t")
    print(tmp.getAllArgs())
    commands.analyseCommand("log -u")
    commands.analyseCommand("log -u cxol,ok")
    commands.analyseCommand("log")
    commands.analyseCommand("log -h")
    commands.analyseCommand("ls")
    commands.analyseCommand('ls -h')
    pass
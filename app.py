from model import menu as models_menu
import abc


class App(metaclass=abc.ABCMeta):
    __slots__ = ["manager"]

    def __init__(self):
        self.manager: models_menu.MenuManager = None

    def __call__(self, cmd: int):
        if cmd and cmd in self.manager:
            print(self.manager(cmd))
        return None

    def stat_menu(self):
        print(self.manager)
        return None

    def run(self):
        self.create_menu()
        cmd = 0
        while True:
            self.stat_menu()
            try:
                cmd = int(input("choose number"))
            except ValueError:
                print("command non numeric")
                continue
            if cmd in self.manager:
                self.__call__(cmd)
            elif cmd < 0:
                quit(0)
            else:
                print("command out of range!")

    @abc.abstractmethod
    def create_menu(self):
        pass


class SomeApp(App):
    defaults = zip("a,b,c,d,e".split(","), (lambda a: f"{a.title} work" for _ in range(5)))

    def __init__(self):
        super(SomeApp, self).__init__()

    def __call__(self, *args, **kwargs):
        if not args:
            self.run()
        elif len(args) and args[0] in self.manager:
            print(self.manager(args[0]))
        else:
            return 1
        return 0

    def create_menu(self):
        self.manager = models_menu.MenuManager(self.__class__.__name__+models_menu.MenuManager.__name__)
        return [
            _ for _ in map(
                (lambda a: self.manager+a),
                (models_menu.Menu(*pair) for pair in self.__class__.defaults)
            )
        ]


if __name__ == '__main__':
    a = SomeApp()
    a()

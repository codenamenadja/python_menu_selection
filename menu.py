from functools import reduce, partial
from abc import ABCMeta, abstractmethod

class MenuBase(metaclass=ABCMeta):
    def __init__(self, t):
        self.title = t

    def __str__(self):
        return self.title


class Menu(MenuBase):
    __slots__ = ["title", "_action"]

    def __init__(self, t, a=None):
        super(Menu, self).__init__(t)
        self._action = partial(a, self)

    def __str__(self):
        return self.title

    def __call__(self):
        return self._action()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.title == other.title
        return False


class MenuManager(MenuBase):
    __slots__ = ['title', 'menus']

    def __init__(self, t):
        self.title = t
        self.menus: list[Menu] = []

    def __add__(self, other: Menu):
        self.menus.append(other)
        return self

    def __str__(self):
        return str.join(
            "", [f"{i}:{v.title}\t" for i, v in enumerate(self.menus)]
        )

    def __contains__(self, item):
        if self.menus and (len(self.menus) >= item) and (item >= 0):
            return True
        return False

    def __call__(self, i):
        if i not in self:
            return None
        return self.menus[i]()

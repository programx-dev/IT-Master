from PyQt6 import QtCore

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MetaclassCommon(type(QtCore.QObject), Singleton):
    pass

class GlobalSenderEvents(QtCore.QObject, metaclass = MetaclassCommon):
    def __init__(self):
        super().__init__()
        self.__events = {}

    def addEventListener(self, name, func):
        if name not in self.__events:
            self.__events[name] = [func]
        else:
            self.__events[name].append(func)

    def dispatchEvent(self, name, *args, **kvargs):
        functions = self.__events.get(name, [])
        for func in functions:
            # QtCore.QTimer.singleShot(0, lambda: func(*args, **kvargs))
            func(*args, **kvargs)

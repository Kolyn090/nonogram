class Matrix_Subject:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def update_observer_axis(self, xy, newlen):
        if xy == 'row':
            for observer in self._observers:
                observer.update_row(newlen)
        elif xy == 'col':
            for observer in self._observers:
                observer.update_column(newlen)

    def update_observer_size(self, width, height):
        for observer in self._observers:
            observer.update_size(width=width, height=height)

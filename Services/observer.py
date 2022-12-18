from Domain.Events.event import Event


class Observer:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, event: Event, *args, **kwargs):
        print(event)
        for observer in self._observers:
            observer.model_is_changed(event)

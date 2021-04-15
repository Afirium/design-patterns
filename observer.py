from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Subject(ABC):
    """The Subject interface declares a set of methods for managing subscribers"""
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class CoinFlipper(Subject):
    """The Coin flipper owns some important state and notifies observers when the state changes"""
    _state: int = None
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        print("Coin flipper: attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        """Trigger an update in each subscriber"""

        print("Coin flipper: notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def flip(self) -> None:
        print("\nCoin flipper: fliiiip")
        self._state = randrange(0, 2)

        print(f"Coin flipper: my state has just changed to: {self._state}")
        self.notify()


class Observer(ABC):
    """The Observer interface declares the update method, used by subjects"""
    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass


class HeadsObserver(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state == 1:
            print("Heads observer: heads!")


class TailsObserver(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state == 0:
            print("Tails observer: tails!")


if __name__ == "__main__":
    # Inspiration
    # https://www.random.org/coins/
    subject = CoinFlipper()

    # Add first observer
    observer_a = HeadsObserver()
    subject.attach(observer_a)

    # Add second observer
    observer_b = TailsObserver()
    subject.attach(observer_b)

    subject.flip()
    subject.flip()

    subject.detach(observer_a)

    subject.flip()

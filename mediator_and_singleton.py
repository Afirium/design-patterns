from __future__ import annotations
from abc import abstractmethod
from typing import List


class Chat:
    """Mediator"""
    def __init__(self):
        self.users_list: List[User] = []
        self.bot: Bot = None

    def send_message(self, message: str, user: User):
        if user in self.users_list:
            self.check_bot_commands(message)
            message = self.run_bots(user, message)

            for chat_user in self.users_list:
                if chat_user != user:
                    chat_user.receive(message)

    def add_user(self, user: User):
        if user not in self.users_list:
            self.users_list.append(user)

    def remove_user(self, user: User):
        if user in self.users_list:
            self.users_list.remove(user)

    def run_bots(self, user: User, message: str) -> str:
        if self.bot:
            censor_message = self.bot.check_message(message)

            if censor_message:
                message = censor_message
                self.remove_user(user)

        return message

    def check_bot_commands(self, message: str):
        if 'addBot' in message:
            self.bot = Bot(stopword='cat')
        elif 'removeBot' in message:
            self.bot = None

class User:
    def __init__(self, mediator, user_name):
        self.mediator = mediator
        self.user_name = user_name

    @abstractmethod
    def send(self, msg: str):
        pass

    @abstractmethod
    def receive(self, msg: str):
        pass


class ChatUser(User):
    def __init__(self, mediator: Chat, user_name: str):
        super().__init__(mediator, user_name)
        mediator.add_user(self)

    def send(self, msg: str):
        print(f'{self.user_name} -> send -> {msg}' )
        self.mediator.send_message(msg, self)

    def receive(self, msg: str):
        print(f'{self.user_name} <- receive <- {msg}')


class Singleton(object):
    """Use to create a singleton"""
    def __new__(cls, *args, **kwds):
        """
        >>> s = Singleton()
        >>> p = Singleton()
        >>> id(s) == id(p)
        True
        """
        self = "__self__"
        if not hasattr(cls, self):
            instance = object.__new__(cls)
            instance.init(*args, **kwds)
            setattr(cls, self, instance)
        return getattr(cls, self)

    def init(self, *args, **kwds):
        pass


class Bot(Singleton):
    def init(self, stopword: str, *args, **kwds):
        self.stopword = stopword

    def check_message(self, message: str):
        if self.stopword in message:
            print(f'\tStopword "{self.stopword}" removed')

            return message.replace(self.stopword, '#$@&%*')

if __name__ == '__main__':
    # Create chat room
    chat = Chat()

    # Add users
    user_alfa = ChatUser(chat, 'alfa')
    user_beta = ChatUser(chat, 'beta')
    user_gamma = ChatUser(chat, 'gamma')

    # Send messages
    user_alfa.send('Hello!')

    # Add bot
    user_beta.send('addBot')


    # Send message with stopword
    user_beta.send('I love my cat!')

    user_gamma.send('Wow!')

    # Remove bot and try again
    user_alfa.send('removeBot please!')

    user_gamma.send('I love my cat!')

    # Removed from chat
    user_beta.send('I love my cat!')

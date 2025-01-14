import json

from model import User, Channel, Message


class Server :
    def __init__(self, users : 'list[User]', channels : 'list[Channel]', messages : 'list[Message]') :
        self.users = users
        self.channels = channels
        self.messages = messages

    @staticmethod
    def list_to_str(L : 'list[str]') -> 'str' :
        res = ''
        for word in L :
            res = res + word + ', '
        res = res[ :-2] + '.'
        return res

    @classmethod
    def from_dict(cls, server_dict : 'dict') -> 'Server' :
        users = []
        channels = []
        messages = []
        for user in server_dict['users'] :
            users.append(User(user['id'], user['name']))
        for channel in server_dict['channels'] :
            channels.append(Channel(channel['id'], channel['name'], channel['member_ids']))
        for message in server_dict['messages'] :
            messages.append(Message(message['id'], message['reception_date'], message['sender_id'], message['channel'], message['content']))
        server = cls(users, channels, messages)
        return server

    @classmethod
    def load(cls, server_filename) -> 'Server' :
        with open(server_filename, 'r') as f :
            server = json.load(f)
        return cls.from_dict(server)
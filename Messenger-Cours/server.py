import json
import colorama

from model import User, Channel, Message


class Server :
    def __init__(self, users : 'list[User]', channels : 'list[Channel]', messages : 'list[Message]') :
        self.users = users
        self.channels = channels
        self.messages = messages

    @staticmethod
    def list_to_str(L : 'list[str]', color_words : 'str' = '', color_commas : 'str' = colorama.Style.RESET_ALL) -> 'str' :
        res = ''
        for word in L :
            res = res + color_words + word + color_commas + ', '
        res = res[ :-2] + color_commas + '.' + colorama.Style.RESET_ALL
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

    # Fonctions utiles

    def id_to_user(self, id : 'int') -> 'User' :
        pass

    def id_to_channel(self, id : 'int') -> 'Channel' :
        pass

    def name_to_user(self, name : 'str') -> 'User' :
        pass

    def name_to_channel(self, name : 'str') -> 'Channel' :
        pass

#Fonctionnalités de la classe

    def get_users(self) -> 'list[User]' :
        pass

    def get_channels(self) -> 'list[Channel]' :
        pass
    
    def get_messages(self) -> 'list[Message]' :
        pass

    def post_user(self, name : 'str') -> 'list' :
        pass
    
    def post_channel(self, channel_name : 'str') -> 'list' :
        pass

    def post_user_in_channel(self, channel_id : 'int', user_id : 'int') : #LocalServer : renvoie un 'bool' ; RemoteServer : renvoie un 'bool' ou une 
        pass

    def post_message(self, channel_id : 'int', sender_id : 'int', message : 'str') :
        pass
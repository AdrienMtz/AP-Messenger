from server import Server
from client import Client
from model import User
from model import Channel
from model import Message
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--server', '-s', help = 'enter json path', default = 'C:/Users/Adrien/UE12/AP/Messenger-Cours/Server-Messenger.json')
parser.add_argument('--url', help = 'enter server url', default = 'http://127.0.0.1:5000')
args = parser.parse_args()

class RemoteServer :
    def __init__(self, url : str):
        self.url = url
    
    def __repr__(self) :
        return f'RemoteServer({self.url})'

    def get_users(self) :
        users = requests.get(self.url + '/users')
        
        return users

    def get_channels(self) :
        channels = requests.get(self.url + '/channels')
        
        return channels
    
    def get_messages(self) :
        messages = requests.get(self.url + '/channels/$id/messages')

        return messages


    def id_to_user(self, id : 'int') -> 'User' :
        L = []
        for user in self.get_users() :
            if user.id == id :
                L.append(user)
        if len(L) == 0 :
            print('No such user id.')
        elif len(L) > 2 :
            print(f'Error : 2 names for id {id}')
        else :
            return L[0]

    def id_to_channel(self, id : 'int') -> 'Channel' :
        L = []
        for channel in self.get_channels() :
            if channel.id == id :
                L.append(channel)
        if len(L) == 0 :
            print('No such channel id.')
        elif len(L) > 2 :
            print(f'Error : 2 names for id {id}')
        else :
            return L[0]

    def name_to_user(self, name : 'str') -> 'User' :
        L = []
        for user in self.get_users() :
            if user.name == name :
                L.append(user)
        if len(L) == 0 :
            print('No such username.')
        elif len(L) > 2 :
            print(f'Error : 2 ids for name {name}')
        else :
            return L[0]

    def name_to_channel(self, name : 'str') -> 'Channel' :
        L = []
        for channel in self.get_channels() :
            if channel.name == name :
                L.append(channel)
        if len(L) == 0 :
            print('No such channel name.')
        elif len(L) > 2 :
            print(f'Error : 2 ids for name {name}')
        else :
            return L[0]

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
    def load(cls) -> 'Server' :
        with open(cls.SERVER_FILENAME, 'r') as f :
            server = json.load(f)
        return cls.from_dict(server)
    
    def save(self) :
        with open(Server.SERVER_FILENAME, 'w') as f :
            json.dump(self.to_dict(), f)
    
    def to_dict(self) -> 'dict' :
        server = {'users' : [], 'channels' : [], 'messages' : []}
        for user in self.get_users() :
            server['users'].append(user.to_dict())
        for channel in self.get_channels() :
            server['channels'].append(channel.to_dict())
        for message in self.get_messages() :
            server['messages'].append(message.to_dict())
        return server

server = Server.load()
client = Client(server)
client.main_menu()

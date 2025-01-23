import json
import colorama
from datetime import datetime

from model import User
from model import Channel
from model import Message
from server import Server


class LocalServer(Server) :
    def __init__(self, server_filename : 'str') :
        self.server_filename = server_filename
        server = Server.load(server_filename)
        self.users = server.users
        self.channels = server.channels
        self.messages = server.messages
    
    def __repr__(self) -> 'str' :
        return f'LocalServer(Users : {[(user.id, user.name) for user in self.users]}, Channels : {[(channel.id, channel.name) for channel in self.channels]}, Messages : {[(message.content, message.id) for message in self.messages]}'

# Fonctions annexes

    def id_to_user(self, id : 'int') -> 'User' :
        L = []
        for user in self.users :
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
        for channel in self.channels :
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
        for user in self.users :
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
        for channel in self.channels :
            if channel.name == name :
                L.append(channel)
        if len(L) == 0 :
            print('No such channel name.')
        elif len(L) > 2 :
            print(f'Error : 2 ids for name {name}')
        else :
            return L[0]
    
    def save(self) :
        with open(self.server_filename, 'w') as f :
            json.dump(self.to_dict(), f)
    
    def to_dict(self) -> 'dict' :
        server = {'users' : [], 'channels' : [], 'messages' : []}
        for user in self.users :
            server['users'].append(user.to_dict())
        for channel in self.channels :
            server['channels'].append(channel.to_dict())
        for message in self.messages :
            server['messages'].append(message.to_dict())
        return server

    def get_users(self) -> 'list[User]' :
        return self.users
    
    def get_channels(self) -> 'list[Channel]' :
        return self.channels
    
    def get_messages(self) -> 'list[Message]' :
        return self.messages

    def post_user(self, name : 'str') -> 'list' :
        user_id = max(user.id for user in self.users) + 1
        user = User(user_id, name)
        self.users.append(user)
        self.save()
        return [True, user_id]

    def post_channel(self, channel_name : 'str') -> list :
        member_ids = []
        choice = '0'
        size = 0
        names = []
        vide = True
        while choice != 'n' or vide:
            choice = input('\nDo you want to add a new user to this channel ? (y/n) \n')
            if choice == 'y' :
                user_id = int(input('\nUser Id : \n'))
                if user_id not in [user.id for user in self.users] :
                    return [False]
                member_ids.append(user_id)
                names.append(self.id_to_user(user_id).name)
                size += 1
            elif choice == 'n' :
                if size > 0:
                    vide = False
                    break
                else :
                    print(f'\n{colorama.Fore.LIGHTRED_EX}Please add a user to this channel.{colorama.Style.RESET_ALL}')
            else :
                print(f'{colorama.Fore.LIGHTRED_EX}Unknown option : {choice} \n{colorama.Style.RESET_ALL}')
        channel = Channel(max(channel.id for channel in self.channels) + 1, channel_name, member_ids)
        self.channels.append(channel)
        self.save()
        print(f'\n{colorama.Fore.LIGHTGREEN_EX}New channel created -> {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Fore.LIGHTGREEN_EX} : {Server.list_to_str(names, color_words = colorama.Fore.LIGHTCYAN_EX, color_commas = colorama.Fore.LIGHTGREEN_EX)} \n')  
        return [True]

    def post_user_in_channel(self, channel_id : 'int', user_id : 'int') -> 'bool' :
        channel = self.id_to_channel(channel_id)
        channel.member_ids.append(user_id)
        self.save()
        return True

    def post_message(self, channel_id : 'int', user_id : 'int', message : 'str') -> 'bool' :
        self.messages.append(Message(max(message.id for message in self.messages) + 1, str(datetime.now()).split('.')[0], user_id, channel_id, message))
        self.save()
        return True
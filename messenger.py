from datetime import datetime
import json


# Définition des classes

class User :
    def __init__(self, id : int, name : str) :
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f'User({self.id}, {self.name})'

    def to_dict(self) :
        return {'id' : self.id, 'name' : self.name}

class Channel :
    def __init__(self, id : int, name : str, member_ids : 'list[int]') :
        self.id = id
        self.name = name
        self.member_ids = member_ids
    
    def __repr__(self):
        return f'Channel({self.id}, {self.name}, {self.member_ids})'

    def to_dict(self) :
        return {'id' : self.id, 'name' : self.name, 'member_ids' : self.member_ids}

class Message  :
    def __init__(self, id : int, reception_date : str, sender_id : int, channel : int, content : str) :
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content
    
    def __repr__(self):
        return f'Message({self.id}, {self.reception_date}, {self.sender_id}, {self.channel}, {self.content})'

    def to_dict(self) :
        return {'id' : self.id, 'reception_date' : self.reception_date, 'sender_id' : self.sender_id, 'channel' : self.channel, 'content' : self.content}

class Server :
    def __init__(self, users : 'list[User]', channels : 'list[Channel]', messages : 'list[Message]') :
        self.users = users
        self.channels = channels
        self.messages = messages
    
    def __repr__(self) :
        return f'Server(Users : {[(user.id, user.name) for user in self.users]}, Channels : {[(channel.id, channel.name) for channel in self.channels]}, Messages : {[(message.content, message.id) for message in self.messages]}'

    @classmethod
    def from_dict(cls, server_dict : 'dict'):
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
    def load(cls, file = 'C:/Users/Adrien/UE12/AP/Server-Messenger.json') :
        with open(file, 'r') as f :
            server = json.load(f)
        return cls.from_dict(server)
    
    def save(self):
        with open('C:/Users/Adrien/UE12/AP/Server-Messenger.json', 'w') as f :
            json.dump(self.to_dict(), f)
    
    def to_dict(self) :
        server = {'users' : [], 'channels' : [], 'messages' : []}
        for user in self.users :
            server['users'].append(user.to_dict())
        for channel in self.channels :
            server['channels'].append(channel.to_dict())
        for message in self.messages :
            server['messages'].append(message.to_dict())
        return server

class Client :
    def __init__(self, server):
        self.server = server

    def main_menu(self):
        print('\n')
        print('a. See users')
        print('b. See channels')
        print('c. Leave')
        print('\n')
        choice = input('Select an option : ')
        if choice == 'a':
            self.see_users()
        elif choice == 'b':
            self.see_channels()
        elif choice == 'c':
            print('\nBye !\n')
        else :
            print(f'Unknown option : {choice}')

    def see_users(self):
        server = self.server
        print('\n')
        for user in server.users:
            print(f'{user.id}. {user.name}\n')
        print('a. Create user')
        print('b. Back to main menu')
        print('\n')
        choice = input('Select an option : ')
        if choice == 'a' :
            self.create_user()
        elif choice == 'b' :
            self.main_menu()
        else :
            print(f'Unknown option : {choice}')
            self.main_menu()

    def see_channels(self):
        server = self.server
        print('\n')
        for channel in server.channels:
            names = ''
            for member in channel.member_ids:
                username = id_to_user(member).name
                names = names + username + ', '
            names = names[:-2] + '.'
            print(f'{channel.id}. {channel.name} : {names}\n')
        print('a. See messages')
        print('b. Create new channel')
        print('c. Add user to channel')
        print('d. Remove user from channel')
        print('e. Back to main menu')
        print('\n')
        choice = input('Select an option : ')
        if choice == 'a' :
            channel_id = input('Channel id : ')
            self.see_messages(int(channel_id))
        elif choice == 'b':
            self.create_channel()
        elif choice == 'c' :
            self.add_user()
        elif choice == 'd':
            self.remove_user()
        elif choice == 'e':
            self.main_menu()
        else :
            print(f'Unknown option : {choice}')
            self.main_menu()

    def create_user():
        server = Server.load()
        name = input('Name : ')
        user = User(max(user.id for user in server.users) + 1, name)
        server.users.append(user)
        print(f'New user created : {user.id}. {name}\n')
        server.save()
        print('a. See users')
        print('b. Back to main menu')
        print('\n')
        choice = input('Select an option : ')
        if choice == 'a' :
            see_users()
        elif choice == 'b' :
            main_menu()
        else :
            print(f'Unknown option : {choice}')
            main_menu()

    def see_messages(channel_id : 'int'):
        server = Server.load()
        messages = [message for message in server.messages if message.channel == channel_id]
        print(f'Channel {channel_id} : {id_to_channel(channel_id).name}\n')
        for message in messages :
            user = id_to_user(message.sender_id).name
            print(f'({message.reception_date}) - {user} : {message.content}')
        print('\n')
        print('a. See channels')
        print('b. Write a message')
        print('c. Back to main menu')
        print('\n')
        choice  = input('Select an option  : ')
        if choice == 'a' :
            see_users()
        elif choice == 'b' :
            write_message(channel_id)
        elif choice == 'c' :
            main_menu()
        else :
            print(f'Unknown option : {choice}')
            main_menu()

    def create_channel():
        server = Server.load()
        channel_name = input('Channel name : ')
        member_ids = []
        choice = '0'
        while choice != 'n' :
            choice = input('Do you want ot add a new user to this channel ? (y/n) \n')
            if choice == 'y':
                user_id = int(input('User Id : \n'))
                member_ids.append(user_id)
            elif choice != 'n':
                print(f'Unknown option : {choice}')
                main_menu()
        channel = Channel(max(channel.id for channel in server.channels) + 1, channel_name, member_ids)
        server.channels.append(channel)
        print('New channel created')
        server.save()
        see_channels()

    def add_user():
        server = Server.load()
        channel_id = int(input('To which channel ? \n'))
        channel = id_to_channel(channel_id)
        user_id = int(input('User Id ? \n'))
        if user_id in channel.member_ids :
            print(f'User {user_id} is already in channel {channel_id}')
        else :
            channel.member_ids.append(user_id)
            print(f'User {user_id} has been added to channel {channel_id}')
        server.save()
        see_channels()

    def remove_user():
        server = Server.load()
        channel_id = int(input('From which channel ? \n'))
        channel = id_to_channel(channel_id)
        user_id = int(input('User Id ? \n'))
        if user_id not in channel.member_ids :
            print(f'User {user_id} is not in channel {channel_id}')
        else :
            channel.member_ids.pop(premier_indice(channel.member_ids, user_id))
            print(f'User {user_id} has been removed from channel {channel_id}')
        server.save()
        see_channels()

    def write_message(channel_id : 'int') :
        server = Server.load()
        print(f'Message to channel {channel_id} : {id_to_channel(channel_id).name} \n')
        name = input('Who writes ? \n')
        user_id = name_to_user(name).id
        for channel in server.channels :
            if channel.id == channel_id :
                ch = channel
        if user_id not in channel.member_ids :
            print(f'User {name} is not in channel {channel.id} : {channel.name}.')
            choice = input('Do you want to add a new user to this channel ? (y/n)\n')
            if choice == 'y' :
                add_user()
            elif choice == 'n' :
                see_messages(channel_id)
            else :
                print(f'Unknown option : {choice}')
                main_menu()
        else :
            message = input('Message : ')
            server.messages.append(Message(max(message.id for message in server.messages) + 1, str(datetime.now()).split('.')[0], name_to_user(name).id, channel_id, message))
            server.save()
            see_messages(channel_id)

# Fonctions annexes

def id_to_user(id : 'int'):
    server = Server.load()
    L = []
    for user in server.users:
        if user.id == id :
           L.append(user)
    if len(L) == 0 :
        print('No such id')
    elif len(L) > 2 :
        print(f'Error : 2 names for id {id}')
    else :
        return L[0]

def id_to_channel(id : 'int'):
    server = Server.load()
    L = []
    for channel in server.channels:
        if channel.id == id :
           L.append(channel)
    if len(L) == 0 :
        print('No such id')
    elif len(L) > 2 :
        print(f'Error : 2 names for id {id}')
    else :
        return L[0]

def name_to_user(name : 'str') :
    server = Server.load()
    L = []
    for user in server.users:
        if user.name == name :
            L.append(user)
    if len(L) == 0 :
        print('No such name')
    elif len(L) > 2 :
        print(f'Error : 2 ids for name {name}')
    else :
        return L[0]

def name_to_channel(name : 'str') :
    server = Server.load()
    L = []
    for channel in server.channels:
        if channel.name == name :
            L.append(channel)
    if len(L) == 0 :
        print('No such name')
    elif len(L) > 2 :
        print(f'Error : 2 ids for name {name}')
    else :
        return L[0]

def premier_indice(L : 'list', e) :
    for i in range(len(L)) :
        if L[i] == e :
            return i


# Fonctionnalités de Messenger

#current_user = {}

# def login():
#     user_id = input('Please enter user id : \n')
#     L = []
#     for user in server['users'] :
#         if user['id'] == user_id :
#             L.append(user)
#     if len(L) == 0 :
#         print('No such user')
#         choice = ('Do you want to create a new user ? (y/n)')
#         if choice == 'y' :
#             create_user()
#         elif choice == 'n' :
#             login()
#         else : 
#             print(f'Unknown option : {choice}')
#             print('a. Retry to login')
#             print('b. Leave \n')
#             choice = input('Select an option : \n')
#             if choice == 'a' :
#                 login()
#             elif choice == 'b' :
#                 print('\nBye !\n')
#             else :
#                 print(f'Unknown option : {choice}')
#     else :
#         password = input('Please enter password : \n')
#         user = L[0]
#         if password == user['password'] :
#             print(f'\nWelcome {user["name"]} !')
#             current_user = user
#         else :
#             print('Incorrect password \n')
#             print('a. Retry to login')
#             print('b. Leave \n')
#             choice = input('Select an option : \n')
#             if choice == 'a' :
#                 login()
#             elif choice == 'b' :
#                 print('\nBye !\n')
#             else :
#                 print(f'Unknown option : {choice}')




print('=== Messenger ===')
main_menu()


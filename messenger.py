from datetime import datetime
import json


# Définition des classes

class User :
    def __init__(self, id : int, name : str) :
        self.id = id
        self.name = name
    
    def __repr__(self) -> 'str':
        return f'User({self.id}, {self.name})'

    def to_dict(self) -> 'dict' :
        return {'id' : self.id, 'name' : self.name}

class Channel :
    def __init__(self, id : int, name : str, member_ids : 'list[int]') :
        self.id = id
        self.name = name
        self.member_ids = member_ids
    
    def __repr__(self) -> 'str':
        return f'Channel({self.id}, {self.name}, {self.member_ids})'

    def to_dict(self) -> 'dict' :
        return {'id' : self.id, 'name' : self.name, 'member_ids' : self.member_ids}

class Message  :
    def __init__(self, id : int, reception_date : str, sender_id : int, channel : int, content : str) :
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content
    
    def __repr__(self) -> 'str' :
        return f'Message({self.id}, {self.reception_date}, {self.sender_id}, {self.channel}, {self.content})'

    def to_dict(self) -> 'dict' :
        return {'id' : self.id, 'reception_date' : self.reception_date, 'sender_id' : self.sender_id, 'channel' : self.channel, 'content' : self.content}

class Server :
    def __init__(self, users : 'list[User]', channels : 'list[Channel]', messages : 'list[Message]') :
        self.users = users
        self.channels = channels
        self.messages = messages
    
    def __repr__(self) -> 'str':
        return f'Server(Users : {[(user.id, user.name) for user in self.users]}, Channels : {[(channel.id, channel.name) for channel in self.channels]}, Messages : {[(message.content, message.id) for message in self.messages]}'

# Fonctions annexes

    def id_to_user(self, id : 'int') -> 'User' :
        L = []
        for user in self.users:
            if user.id == id :
                L.append(user)
        if len(L) == 0 :
            print('No such id')
        elif len(L) > 2 :
            print(f'Error : 2 names for id {id}')
        else :
            return L[0]

    def id_to_channel(self, id : 'int') -> 'Channel':
        L = []
        for channel in self.channels:
            if channel.id == id :
                L.append(channel)
        if len(L) == 0 :
            print('No such id')
        elif len(L) > 2 :
            print(f'Error : 2 names for id {id}')
        else :
            return L[0]


    def name_to_user(self, name : 'str') -> 'User' :
        L = []
        for user in self.users:
            if user.name == name :
                L.append(user)
        if len(L) == 0 :
            print('No such name')
        elif len(L) > 2 :
            print(f'Error : 2 ids for name {name}')
        else :
            return L[0]

    def name_to_channel(self, name : 'str') -> 'Channel' :
        L = []
        for channel in self.channels:
            if channel.name == name :
                L.append(channel)
        if len(L) == 0 :
            print('No such name')
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
    def load(cls, file = 'C:/Users/Adrien/UE12/AP/Server-Messenger.json') -> 'Server' :
        with open(file, 'r') as f :
            server = json.load(f)
        return cls.from_dict(server)
    
    def save(self):
        with open('C:/Users/Adrien/UE12/AP/Server-Messenger.json', 'w') as f :
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

class Client :
    def __init__(self, server : 'Server'):
        self.server = server

    def __repr__(self) -> 'str' :
        return f'Client({self.server})'

    @staticmethod
    def premier_indice(L : 'list', e) :
        for i in range(len(L)) :
            if L[i] == e :
                return i

    @staticmethod
    def list_to_str(L : 'list[str]') -> 'str' :
        res = ''
        for word in L :
            res = res + word + ', '
        res = res[:-2] + '.'
        return res

# Fonctionnalités de Messenger

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
            self.server.save()
        else :
            print(f'Unknown option : {choice}')
            self.main_menu()

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
                username = server.id_to_user(member).name
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
            if channel_id not in [channel.id for channel in server.channels] :
                print('No such channel.')
                self.see_channels()
            else :
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

    def create_user(self):
        server = self.server
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
            self.see_users()
        elif choice == 'b' :
            self.main_menu()
        else :
            print(f'Unknown option : {choice}')
            self.main_menu()

    def see_messages(self, channel_id : 'int'):
        server = self.server
        messages = [message for message in server.messages if message.channel == channel_id]
        print(f'Channel {channel_id} : {server.id_to_channel(channel_id).name} \n')
        print(f'Members : {self.list_to_str([server.id_to_user(member_id).name for member_id in server.id_to_channel(channel_id).member_ids])}')
        for message in messages :
            user = server.id_to_user(message.sender_id).name
            print(f'({message.reception_date}) - {user} : {message.content}')
        print('\n')
        print('a. See channels')
        print('b. Write a message')
        print('c. Back to main menu')
        print('\n')
        choice  = input('Select an option  : ')
        if choice == 'a' :
            self.see_users()
        elif choice == 'b' :
            self.write_message(channel_id)
        elif choice == 'c' :
            self.main_menu()
        else :
            print(f'Unknown option : {choice}')
            self.main_menu()

    def create_channel(self):
        server = self.server
        channel_name = input('Channel name : ')
        member_ids = []
        choice = '0'
        while choice != 'n' :
            choice = input('Do you want ot add a new user to this channel ? (y/n) \n')
            if choice == 'y':
                user_id = int(input('User Id : \n'))
                if user_id not in [user.id for user in server.users] :
                    print('No such user.')
                    answer = input('Create new user ? (y/n) \n')
                    if answer == 'y' :
                        self.create_user()
                    elif answer == 'n' :
                        self.create_channel()
                    else :
                        print(f'Unknown option : {answer}')
                        self.main_menu()
                member_ids.append(user_id)
            elif choice != 'n':
                print(f'Unknown option : {choice}')
                self.main_menu()
        channel = Channel(max(channel.id for channel in server.channels) + 1, channel_name, member_ids)
        server.channels.append(channel)
        print('New channel created')
        server.save()
        self.see_channels()

    def add_user(self, user_id = None):
        server = self.server
        channel_id = int(input('To which channel ? \n'))
        if channel_id not in [channel.id for channel in server.channels] :
                    print('No such channel.')
                    answer = input('Create new channel ? (y/n) \n')
                    if answer == 'y' :
                        self.create_channel()
                    elif answer == 'n' :
                        self.add_user()
                    else :
                        print(f'Unknown option : {answer}')
        channel = server.id_to_channel(channel_id)
        if user_id == None :
            user_id = int(input('User Id ? \n'))
        if user_id in channel.member_ids :
            print(f'User {user_id} is already in channel {channel_id}')
        else :
            channel.member_ids.append(user_id)
            print(f'User {user_id} has been added to channel {channel_id}')
        server.save()
        self.see_channels()

    def remove_user(self):
        server = self.server
        channel_id = int(input('From which channel ? \n'))
        channel = server.id_to_channel(channel_id)
        user_id = int(input('User Id ? \n'))
        if user_id not in channel.member_ids :
            print(f'User {user_id} is not in channel {channel_id}')
        else :
            channel.member_ids.pop(self.premier_indice(channel.member_ids, user_id))
            print(f'User {user_id} has been removed from channel {channel_id}')
        server.save()
        self.see_channels()

    def write_message(self, channel_id : 'int') :
        server = self.server
        print(f'Message to channel {channel_id} : {server.id_to_channel(channel_id).name} \n')
        name = input('Who writes ? (enter username) \n')
        if name not in [user.name for user in server.users] :
            print('No such user. \n')
            choice = input('Create new user ? (y/n)')
            if choice == 'y' :
                self.create_user()
            elif choice == 'n' :
                self.see_messages(channel_id)
            else :
                print(f'Unknown option : {choice}')
                self.see_messages(channel_id)
        else :
            user_id = server.name_to_user(name).id
        channel = server.id_to_channel(channel_id)
        if user_id not in channel.member_ids :
            print(f'User {name} is not in channel {channel.id} : {channel.name}.')
            choice = input('Do you want to add this user to this channel ? (y/n)\n')
            if choice == 'y' :
                self.add_user(user_id)
            elif choice == 'n' :
                self.see_messages(channel_id)
            else :
                print(f'Unknown option : {choice}')
                self.main_menu()
        else :
            message = input('Message : ')
            server.messages.append(Message(max(message.id for message in server.messages) + 1, str(datetime.now()).split('.')[0], server.name_to_user(name).id, channel_id, message))
            server.save()
            self.see_messages(channel_id)


print('=== Messenger ===')
server = Server.load()
client = Client(server)
client.main_menu()


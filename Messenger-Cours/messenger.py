from datetime import datetime
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--server', '-s', help='enter json path', default = 'C:/Users/Adrien/UE12/AP/Messenger-Cours/Server-Messenger.json')
args=parser.parse_args()
print(f'server json : {args.server}')

# Définition des classes

class User :
    def __init__(self, id : int, name : str) :
        self.id = id
        self.name = name
    
    def __repr__(self) -> 'str' :
        return f'User({self.id}, {self.name})'

    def __eq__(self, user : 'User') -> 'bool' :
        return self.id == user.id

    def to_dict(self) -> 'dict' :
        return {'id' : self.id, 'name' : self.name}

class Channel :
    def __init__(self, id : int, name : str, member_ids : 'list[int]') :
        self.id = id
        self.name = name
        self.member_ids = member_ids
    
    def __repr__(self) -> 'str' :
        return f'Channel({self.id}, {self.name}, {self.member_ids})'

    def __eq__(self, channel : 'Channel') -> 'bool' :
        return self.id == channel.id
        

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

    def __eq__(self, message : 'Message') -> 'bool' :
        return self.id == message.id

    def to_dict(self) -> 'dict' :
        return {'id' : self.id, 'reception_date' : self.reception_date, 'sender_id' : self.sender_id, 'channel' : self.channel, 'content' : self.content}

class Server :
    SERVER_FILENAME = args.server

    def __init__(self, users : 'list[User]', channels : 'list[Channel]', messages : 'list[Message]') :
        self.users = users
        self.channels = channels
        self.messages = messages
    
    def __repr__(self) -> 'str' :
        return f'Server(Users : {[(user.id, user.name) for user in self.users]}, Channels : {[(channel.id, channel.name) for channel in self.channels]}, Messages : {[(message.content, message.id) for message in self.messages]}'

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
        for user in self.users :
            server['users'].append(user.to_dict())
        for channel in self.channels :
            server['channels'].append(channel.to_dict())
        for message in self.messages :
            server['messages'].append(message.to_dict())
        return server

class Client :
    def __init__(self, server : 'Server') :
        self.server = server

    def __repr__(self) -> 'str' :
        return f'Client({self.server})'

# Fonctions annexes

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
        res = res[ :-2] + '.'
        return res

    @staticmethod
    def clear_screen() :
        os.system('clear')
        print('=== Messenger === \n')

# Fonctionnalités de Messenger

    def main_menu(self) :
        self.clear_screen()
        print('a. See users')
        print('b. See channels')
        print('c. Leave')
        print('\n')
        choice = input('Select an option : ')
        if choice == 'a' :
            self.see_users()
        elif choice == 'b' :
            self.see_channels()
        elif choice == 'c' :
            self.clear_screen()
            print('Bye !\n')
            self.server.save()
        else :
            print(f'Unknown option : {choice} \n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def see_users(self) :
        self.clear_screen()
        server = self.server
        print('\n')
        for user in server.users :
            print(f'{user.id}. {user.name}\n')
        print('a. Create user')
        print('b. Delete user')
        print('c. Back to main menu')
        print('\n')
        choice = input('Select an option : ')
        if choice == 'a' :
            self.create_user()
        elif choice == 'b' :
            self.delete_user()
        elif choice == 'c' :
            self.main_menu()
        else :
            print(f'Unknown option : {choice} \n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def see_channels(self) :
        self.clear_screen()
        server = self.server
        print('\n')
        for channel in server.channels :
            if len(channel.member_ids) == 0 :
                print(f'No user in channel {channel.id}. {channel.name}. Please delete this channel. \n')
                input('Press <Enter> to go to main menu.')
                self.main_menu()
                return None
            else : 
                names = ''
                for member_id in channel.member_ids :
                    user = server.id_to_user(member_id)
                    username = user.name
                    names = names + username + ', '
            names = names[ :-2] + '.'
            print(f'{channel.id}. {channel.name} : {names}\n')
        print('a. See messages')
        print('b. Create new channel')
        print('c. Delete channel')
        print('d. Add user to channel')
        print('e. Remove user from channel')
        print('f. Back to main menu')
        print('\n')
        choice = input('Select an option : ')
        if choice == 'a' :
            channel_id = int(input('\nChannel id : '))
            if channel_id not in [channel.id for channel in server.channels] :
                print('\nNo such channel. \n')
                input('Press <Enter> to see channels.')
                self.see_channels()
            else :
                self.see_messages(channel_id)
        elif choice == 'b' :
            self.create_channel()
        elif choice == 'c' :
            self.delete_channel()
        elif choice == 'd' :
            self.add_user()
        elif choice == 'e' :
            self.remove_user()
        elif choice == 'f' :
            self.main_menu()
        else :
            print(f'\nUnknown option : {choice} \n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def create_user(self) :
        self.clear_screen()
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
            print(f'Unknown option : {choice} \n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def delete_user(self) :
        self.clear_screen()
        server = self.server
        user_id = int(input('Which user do you want to delete ? (id) \n'))
        if user_id not in [user.id for user in server.users] :
            print('\nNo such user. \n')
            input('Press <Enter> to see users.')
            self.see_users()
        else :
            user = server.id_to_user(user_id)
            choice = input(f'\nUser {user.id}. {user.name} will be deleted. Confirm ? (y/n) \n')
            if choice == 'y' :
                user_index = client.premier_indice(server.users, user)
                server.users.pop(user_index)
                server.save()
                for channel in server.channels :
                    if user.id in channel.member_ids :
                        channel.member_ids.pop(self.premier_indice(channel.member_ids, user.id))
                messages2 = []
                for message in server.messages :
                    if message.sender_id != user.id :
                        messages2.append(message)
                server.messages = messages2
                self.clear_screen()
                print(f'\nUser {user_id}. {user.name} deleted successfully. \n')
            elif choice != 'n' :
                print(f'Unknown choice : {choice} \n')
            input('Press <Enter> to see users.')
            self.see_users()

    def see_messages(self, channel_id : 'int') :
        self.clear_screen()
        server = self.server
        channel = server.id_to_channel(channel_id) # Vérifié par see_channels
        if len(channel.member_ids) == 0 :
            print(f'No user in channel {channel.id}. {channel.name}. Please delete this channel. \n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()
            return None
        messages = [message for message in server.messages if message.channel == channel.id]
        print(f'Channel {channel.id} : {channel.name} \n')
        print(f'Members : {self.list_to_str([server.id_to_user(member_id).name for member_id in channel.member_ids])} \n')
        for message in messages :
            user = server.id_to_user(message.sender_id)
            print(f'({message.reception_date}) - {user.name} : {message.content}')
        print('\n')
        print('a. See channels')
        print('b. Write a message')
        print('c. Back to main menu')
        print('\n')
        choice  = input('Select an option  : ')
        if choice == 'a' :
            self.see_users()
        elif choice == 'b' :
            self.write_message(channel.id)
        elif choice == 'c' :
            self.main_menu()
        else :
            print(f'Unknown option : {choice} \n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def create_channel(self) :
        self.clear_screen()
        server = self.server
        channel_name = input('Channel name : ')
        member_ids = []
        choice = '0'
        size = 0
        names = []
        while choice != 'n' :
            choice = input('\nDo you want to add a new user to this channel ? (y/n) \n')
            if choice == 'y' :
                user_id = int(input('\nUser Id : \n'))
                if user_id not in [user.id for user in server.users] :
                    print('No such user.')
                    answer = input('Create new user ? (y/n) \n')
                    if answer == 'y' :
                        self.create_user()
                    elif answer != 'n' :
                        print(f'Unknown option : {answer} \n')
                member_ids.append(user_id)
                names.append(server.id_to_user(user_id).name)
                size += 1
            elif choice == 'n' :
                if size > 0:
                    break
                else :
                    print('\nPlease add a user to this channel.')
            else :
                print(f'Unknown option : {choice} \n')
        channel = Channel(max(channel.id for channel in server.channels) + 1, channel_name, member_ids)
        server.channels.append(channel)
        
        print(f'\nNew channel created : \n{channel.id}. {channel.name} : {self.list_to_str(names)} \n')  
        input('Press <Enter> to see channels.')
        server.save()
        self.see_channels()

    def delete_channel(self, channel : 'Channel' = None, automatic : 'bool'= False) :
        self.clear_screen()
        server = self.server
        choice = 'y'
        if not automatic :
            channel_id = int(input('Which channel do you want to delete ? (id) \n'))
            if channel_id not in [channel.id for channel in server.channels] :
                    print('No such channel.')
                    input('Press <Enter> to see channels.')
                    self.see_channels()
            else :
                channel = server.id_to_channel(channel_id)
                choice = input(f'\nChannel {channel.id}. {channel.name} will be deleted. Confirm ? (y/n) \n')
        if choice == 'y' :
            channel_index = self.premier_indice(server.channels, channel)
            server.channels.pop(channel_index)
            messages2 = []
            for message in server.messages :
                if message.channel != channel.id :
                    messages2.append(message)
            server.messages = messages2 
            server.save()
            print(f'\nChannel {channel.id} deleted successfully. \n')
        elif choice != 'n' :
            print(f'Unknown choice: {choice} \n')
        if not automatic :
            input('Press <Enter> to see channels.')
            self.see_channels()

    def add_user(self, user_id = None) :
        self.clear_screen()
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
                        print(f'Unknown option : {answer} \n')
                        input('Press <Enter> to add user.')
                        self.add_user()
        channel = server.id_to_channel(channel_id)
        if user_id == None :
            user_id = int(input('User Id ? \n'))
        if user_id not in [user.id for user in server.users] :
            print('No such user.')
            answer = input('Create new user ? (y/n) \n')
            if answer == 'y' :
                self.create_user()
            else :
                if answer != 'n' :
                    print(f'Unknown option : {answer} \n')
                input('Press <Enter> to see channels.')
                self.see_channels()
        else :
            user = server.id_to_user(user_id)
            if user_id in channel.member_ids :
                print(f'User {user.id}. {user.name} is already in channel {channel.id}. {channel.name} \n')
            else :
                channel.member_ids.append(user_id)
                print(f'\nUser {user.id}. {user.name} has been added to channel {channel.id}. {channel.name} \n')
            input('Press <Enter> to see channels.')
            server.save()
            self.see_channels()

    def remove_user(self) :
        self.clear_screen()
        server = self.server
        channel_id = int(input('From which channel ? \n'))
        if channel_id not in [channel.id for channel in server.channels] :
            print('\nNo such channel. \n')
            input('Press <Enter> to see channels.')
            self.see_channels()
        else :
            channel = server.id_to_channel(channel_id)
            user_id = int(input('\nUser Id ? \n'))
            if user_id not in channel.member_ids :
                print(f'User {user.id} is not in channel {channel.id}. \n')
            else :
                user = server.id_to_user(user_id)
                choice = input(f'\nUser {user.id}. {user.name} will be removed from channel {channel.id}. {channel.name}. Confirm ? (y/n) \n')
                if choice == 'y' :
                    answer = '' # Permet de savoir s'il faut supprimer le channel.
                    if len(channel.member_ids) == 1 :
                        answer = input(f'\n Channel {channel.id}. {channel.name} will be deleted. Confirm ? (y/n) \n')
                        if answer not in ['y', 'n'] :
                            print(f'\nUnknown option : {answer} \n')
                        if answer != 'y' :
                            input('Press <Enter> to see channels.')
                            self.see_channels()
                    channel.member_ids.pop(self.premier_indice(channel.member_ids, user.id))
                    print(f'\nUser {user.id} has been removed from channel {channel.id}. \n')
                    if answer == 'y' :
                        self.delete_channel(channel, automatic = True)
                elif choice != 'n' :
                    print(f'\nUnknown option : {choice} \n')
            server.save()
            input('Press <Enter> to see channels.')
            self.see_channels()

    def write_message(self, channel_id : 'int') :
        self.clear_screen()
        server = self.server
        channel = server.id_to_channel(channel_id) # Vérifié par see_messages()
        print(f'Message to channel {channel.id} : {channel.name} \n')
        username = input('Who writes ? (enter username) \n')
        if username not in [user.name for user in server.users] :
            print('No such user. \n')
            choice = input('Create new user ? (y/n) \n')
            if choice == 'y' :
                self.create_user()
            elif choice == 'n' :
                self.see_messages(channel.id)
            else :
                print(f'\nUnknown option : {choice} \n')
                input('Press <Enter> to see messages in channel {channel.}.')
                self.see_messages(channel.id)
        else :
            user = server.name_to_user(username)
        if user.id not in channel.member_ids :
            print(f'User {user.id}. {user.name} is not in channel {channel.id} : {channel.name}.')
            choice = input('Do you want to add this user to this channel ? (y/n) \n')
            if choice == 'y' :
                self.add_user(user.id)
            elif choice == 'n' :
                self.see_messages(channel.id)
            else :
                print(f'\nUnknown option : {choice} \n')
                input('Press <Enter> to go to main menu.')
                self.main_menu()
        else :
            message = input('\nMessage : ')
            server.messages.append(Message(max(message.id for message in server.messages) + 1, str(datetime.now()).split('.')[0], user.id, channel.id, message))
            server.save()
            self.see_messages(channel.id)

server = Server.load()
client = Client(server)
client.main_menu()
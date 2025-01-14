import os
import colorama

from model import Channel
from server import Server


class Client :
    def __init__(self, server : 'Server') :
        self.server = server

    def __repr__(self) -> 'str' :
        return f'Client({self.server})'

# Fonctions annexes

    @staticmethod
    def first_index(L : 'list', e) :
        for i in range(len(L)) :
            if L[i] == e :
                return i

    @staticmethod
    def clear_screen() :
        os.system('clear')
        print(f'{colorama.Fore.LIGHTGREEN_EX}¤========¤===========¤========¤')
        print(f'------>    {colorama.Fore.BLUE}MESSENGER{colorama.Fore.LIGHTGREEN_EX}    <------')
        print('¤========¤===========¤========¤\n')
        print(colorama.Style.RESET_ALL)

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
        else :
            print(f'Unknown option : {choice} \n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def see_users(self) :
        self.clear_screen()
        server = self.server
        for user in server.get_users() :
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
        for channel in server.get_channels() :
            if len(channel.member_ids) == 0 :
                print(f'{channel.id}. {channel.name} : No user in this channel. Please add a user to this channel or delete it. \n')
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
            if channel_id not in [channel.id for channel in server.get_channels()] :
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
        result = server.post_user(name)
        if result[0] == True :
            user_id = result[1]
            print(f'New user created : {user_id}. {name}\n')
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
        else :
            print(f'\nFailed to create user {name} on remote server ({server.url}) : {result[1]}.\n')
            input('Press <Enter> to see users.')
            self.see_users()

    def delete_user(self) :
        self.clear_screen()
        server = self.server
        user_id = int(input('Which user do you want to delete ? (id) \n'))
        if user_id not in [user.id for user in server.get_users()] :
            print('\nNo such user. \n')
            input('Press <Enter> to see users.')
            self.see_users()
        else :
            user = server.id_to_user(user_id)
            choice = input(f'\nUser {user.id}. {user.name} will be deleted. Confirm ? (y/n) \n')
            if choice == 'y' :
                user_index = self.first_index(server.get_users(), user)
                server.get_users().pop(user_index)
                server.save()
                for channel in server.get_channels() :
                    if user.id in channel.member_ids :
                        channel.member_ids.pop(self.first_index(channel.member_ids, user.id))
                messages2 = []
                for message in server.get_messages() :
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
        messages = [message for message in server.get_messages() if message.channel == channel.id]
        print(f'Channel {channel.id} : {channel.name} \n')
        print(f'Members : {Server.list_to_str([server.id_to_user(member_id).name for member_id in channel.member_ids])} \n')
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
            self.see_channels()
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
        result = server.post_channel(channel_name)
        if not result[0] :
            if len(result) == 1 :
                print('No such user.')
                answer = input('Create new user ? (y/n) \n')
                if answer == 'y' :
                    self.create_user()
                elif answer != 'n' :
                    print(f'Unknown option : {answer} \n')
            else :
                print(f'\nFailed to post channel on remote server ({server.url}) : {result[1]}.\n')
        elif len(result) == 3 :
            self.add_user(result[1], result[2])
        else :
            input('Press <Enter> to see channels.')
            self.see_channels()

    def delete_channel(self, channel : 'Channel' = None, automatic : 'bool'= False) :
        self.clear_screen()
        server = self.server
        choice = 'y'
        if not automatic :
            channel_id = int(input('Which channel do you want to delete ? (id) \n'))
            if channel_id not in [channel.id for channel in server.get_channels()] :
                    print('No such channel.')
                    input('Press <Enter> to see channels.')
                    self.see_channels()
            else :
                channel = server.id_to_channel(channel_id)
                choice = input(f'\nChannel {channel.id}. {channel.name} will be deleted. Confirm ? (y/n) \n')
        if choice == 'y' :
            channel_index = self.first_index(server.get_channels(), channel)
            server.get_channels().pop(channel_index)
            messages2 = []
            for message in server.get_messages() :
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

    def add_user(self, user_id = None, channel_id = None) :
        self.clear_screen()
        server = self.server
        if channel_id == None :
            channel_id = int(input('To which channel ? (id) \n'))
            if channel_id not in [channel.id for channel in server.get_channels()] :
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
            user_id = int(input('\nUser Id ? \n'))
        if user_id not in [user.id for user in server.get_users()] :
            print('\nNo such user.')
            answer = input('Create new user ? (y/n) \n')
            if answer == 'y' :
                self.create_user()
            else :
                if answer != 'n' :
                    print(f'Unknown option : {answer} \n')
                input('\nPress <Enter> to see channels.')
                self.see_channels()
        else :
            user = server.id_to_user(user_id)
            if user.id in channel.member_ids :
                print(f'User {user.id}. {user.name} is already in channel {channel.id}. {channel.name} \n')
            result = server.post_user_in_channel(channel_id, user_id)
            if result == True :
                print(f'\nUser {user.id}. {user.name} has been added to channel {channel.id}. {channel.name} \n')
            else :
                print(f'\nFailed to add user {user.id}. {user.name} to channel {channel.id}. {channel.name} on remote server ({server.url}) : {result}.\n')
            input('Press <Enter> to see channels.')
            self.see_channels()

    def remove_user(self) :
        self.clear_screen()
        server = self.server
        channel_id = int(input('From which channel ? \n'))
        if channel_id not in [channel.id for channel in server.get_channels()] :
            print('\nNo such channel. \n')
            input('Press <Enter> to see channels.')
            self.see_channels()
        else :
            channel = server.id_to_channel(channel_id)
            user_id = int(input('\nUser Id ? \n'))
            if user_id not in channel.member_ids :
                print(f'\nUser {user_id} is not in channel {channel.id}. \n')
            else :
                user = server.id_to_user(user_id)
                choice = input(f'\nUser {user.id}. {user.name} will be removed from channel {channel.id}. {channel.name}. Confirm ? (y/n) \n')
                if choice == 'y' :
                    answer = '' # Permet de savoir s'il faut supprimer le channel.
                    if len(channel.member_ids) == 1 :
                        answer = input(f'\nChannel {channel.id}. {channel.name} will be deleted. Confirm ? (y/n) \n')
                        if answer not in ['y', 'n'] :
                            print(f'\nUnknown option : {answer} \n')
                        if answer != 'y' :
                            input('\nPress <Enter> to see channels.')
                            self.see_channels()
                            return None
                    channel.member_ids.pop(self.first_index(channel.member_ids, user.id))
                    print(f'\nUser {user.id} has been removed from channel {channel.id}. \n')
                    if answer == 'y' :
                        self.delete_channel(channel, automatic = True)
                elif choice != 'n' :
                    print(f'\nUnknown option : {choice} \n')
            server.save()
            input('\nPress <Enter> to see channels.')
            self.see_channels()

    def write_message(self, channel_id : 'int') :
        self.clear_screen()
        server = self.server
        channel = server.id_to_channel(channel_id) # Vérifié par see_messages()
        print(f'Message to channel {channel.id} : {channel.name} \n')
        user_id = int(input('Who writes ? (enter user id) \n'))
        if user_id not in [user.id for user in server.get_users()] :
            print('\nNo such user. \n')
            choice = input('Do you want to see users ? (y/n) \n')
            if choice == 'y' :
                self.see_users()
                return None
            elif choice == 'n' :
                self.see_messages(channel.id)
                return None
            else :
                print(f'\nUnknown option : {choice} \n')
                input('Press <Enter> to see messages in channel {channel.}.')
                self.see_messages(channel.id)
                return None
        else :
            user = server.id_to_user(user_id)
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
            result = server.post_message(channel.id, user.id, message)
            if result == True :
                self.see_messages(channel.id)
            else :
                print(f'\nFailed to post message on remote server ({server.url}) : {result}.\n')
                input(f'Press <Enter> to see messages in channel {channel.id}.')
                self.see_messages(channel.id)


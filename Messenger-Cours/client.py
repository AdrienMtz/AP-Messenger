import os
import colorama

from model import Channel
from server import Server


class Client :
    def __init__(self, server : 'Server') :
        self.server = server
        self.CLIENT_ID = None
        self.LEAVE = False #Permet d'arrêter tous les programmes lorsque le client choisit de partir.

    def __repr__(self) -> 'str' :
        return f'Client({self.server})'

# Fonctions annexes

    @staticmethod
    def first_index(L : 'list', e) -> 'int':
        for index, element in enumerate(L) :
            if element == e :
                return index
        print(f'{colorama.Fore.LIGHTRED_EX}Error : {e} is not in {L}.{colorama.Style.RESET_ALL}\n')
        return None

    def clear_screen(self) :
        server = self.server
        os.system('clear')
        print(f'{colorama.Fore.LIGHTGREEN_EX}¤========¤===========¤========¤')
        print(f'------>    {colorama.Fore.BLUE}MESSENGER{colorama.Fore.LIGHTGREEN_EX}    <------')
        if self.CLIENT_ID != None :
            client = server.id_to_user(self.CLIENT_ID)
            print(f'{colorama.Fore.LIGHTYELLOW_EX}Connected as : {colorama.Style.RESET_ALL}{colorama.Fore.LIGHTCYAN_EX}{client.id}. {client.name}{colorama.Fore.LIGHTGREEN_EX}')
        print('¤========¤===========¤========¤')
        print(colorama.Style.RESET_ALL)

# Fonctionnalités de Messenger

    def main_menu(self) :
        self.clear_screen()
        print('a. See users')
        print('b. See channels')
        if self.CLIENT_ID == None :
            print('l. Log in')
        else :
            print('l. Log out')
        print('x. Leave\n')
        choice = input('Select an option : ')
        if choice == 'a' :
            self.see_users()
        elif choice == 'b' :
            self.see_channels()
        elif choice == 'l' :
            if self.CLIENT_ID == None :
                self.log_in()
            else :
                self.log_out()
        elif choice == 'x' :
            self.log_out(automatic = True)
            self.clear_screen()
            print('Bye !\n')
            self.LEAVE = True
        else :
            print(f'{colorama.Fore.LIGHTRED_EX}Unknown option : {choice} \n{colorama.Style.RESET_ALL}')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def log_in(self) :
        self.clear_screen()
        server = self.server
        for user in server.get_users() :
            print(f'{colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}\n{colorama.Style.RESET_ALL}')
        client_id_str = input('Please enter your user id.\n')
        while not Server.test_int(client_id_str) :
            self.clear_screen()
            print(f'{colorama.Fore.LIGHTRED_EX}Please enter an integer.{colorama.Style.RESET_ALL}')
            client_id_str = input('\nPlease enter your user id.\n')
        client_id = int(client_id_str)
        if client_id not in [user.id for user in server.get_users()] :
            print(f'\n{colorama.Fore.LIGHTRED_EX}No such user. \n{colorama.Style.RESET_ALL}')
            input('Press <Enter> to go to main menu.')
            self.main_menu()
        else :
            self.CLIENT_ID = client_id
            user = server.id_to_user(client_id)
            print(f'\nWelcome {colorama.Fore.LIGHTCYAN_EX}{user.name}{colorama.Style.RESET_ALL} !\n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def log_out(self, automatic : 'bool' = False) :
        self.CLIENT_ID = None
        if not automatic :
            self.clear_screen()
            print(f'{colorama.Fore.LIGHTGREEN_EX}You have logged out successfully.{colorama.Style.RESET_ALL}\n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def see_users(self) :
        self.clear_screen()
        server = self.server
        for user in server.get_users() :
            print(f'{colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}\n{colorama.Style.RESET_ALL}')
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
            print(f'{colorama.Fore.LIGHTRED_EX}\nUnknown option : {choice} \n{colorama.Style.RESET_ALL}')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def see_channels(self) :
        self.clear_screen()
        server = self.server
        for channel in server.get_channels() :
            if len(channel.member_ids) == 0 :
                print(f'{colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTRED_EX}No user in this channel. Please add a user to this channel or delete it. {colorama.Style.RESET_ALL}\n')
            else : 
                names = Server.list_to_str([server.id_to_user(member_id).name for member_id in channel.member_ids], color_words = colorama.Fore.LIGHTCYAN_EX)
                print(f'{colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Style.RESET_ALL} : {names}\n')
        print('a. See messages')
        print('b. Create new channel')
        print('c. Delete channel')
        print('d. Add user to channel')
        print('e. Remove user from channel')
        print('f. Back to main menu')
        print('\n')
        choice = input('Select an option : ')
        if choice == 'a' :
            channel_id_str = input('\nIn which channel ? (id)\n')
            while not Server.test_int(channel_id_str) :
                self.clear_screen()
                print(f'{colorama.Fore.LIGHTRED_EX}Please enter an integer.{colorama.Style.RESET_ALL}')
                channel_id_str = input('\nIn which channel ? (id)\n')
            channel_id = int(channel_id_str)
            if channel_id not in [channel.id for channel in server.get_channels()] :
                print(f'\n{colorama.Fore.LIGHTRED_EX}No such channel. {colorama.Style.RESET_ALL}\n')
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
            print(f'\n{colorama.Fore.LIGHTRED_EX}Unknown option : {choice} {colorama.Style.RESET_ALL}\n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def create_user(self) :
        self.clear_screen()
        server = self.server
        name = input('Name : ')
        result = server.post_user(name)
        if result[0] == True :
            user_id = result[1]
            print(f'\n{colorama.Fore.LIGHTGREEN_EX}New user created successfully : {colorama.Fore.LIGHTCYAN_EX}{user_id}. {name}\n{colorama.Style.RESET_ALL}')
            print('a. See users')
            print('b. Back to main menu')
            print('\n')
            choice = input('Select an option : ')
            if choice == 'a' :
                self.see_users()
            elif choice == 'b' :
                self.main_menu()
            else :
                print(f'{colorama.Fore.LIGHTRED_EX}\nUnknown option : {choice} {colorama.Style.RESET_ALL}\n')
                input('Press <Enter> to go to main menu.')
                self.main_menu()
        else :
            print(f'\n{colorama.Fore.LIGHTRED_EX}Failed to create user {name} on remote server ({server.url}) : {result[1]}.{colorama.Style.RESET_ALL}\n')
            input('Press <Enter> to see users.')
            self.see_users()

    def delete_user(self) :
        self.clear_screen()
        server = self.server
        user_id_str = input('Which user do you want to delete ? (id)\n')
        while not Server.test_int(user_id_str) :
            self.clear_screen()
            print(f'{colorama.Fore.LIGHTRED_EX}Please enter an integer.{colorama.Style.RESET_ALL}')
            user_id_str = input('\nWhich user do you want to delete ? (id)\n')
        user_id = int(user_id_str)
        if user_id not in [user.id for user in server.get_users()] :
            print(f'\n{colorama.Fore.LIGHTRED_EX}No such user. {colorama.Style.RESET_ALL}\n')
            input('Press <Enter> to see users.')
            self.see_users()
        else :
            user = server.id_to_user(user_id)
            channels_to_delete = [channel for channel in server.get_channels() if channel.member_ids == [user.id]]
            if len(channels_to_delete) > 0 :
                print(f'\nUser {colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}{colorama.Style.RESET_ALL} will be deleted, and will lead to the deletion of the following channels :')
                for channel in channels_to_delete :
                    print(f'\n{colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Style.RESET_ALL}')
            else :
                print(f'\nUser {colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}{colorama.Style.RESET_ALL} will be deleted.')
            choice = input('\nConfirm ? (y/n) \n')
            if choice == 'y' :
                if user_id == self.CLIENT_ID :
                    self.CLIENT_ID = None
                user_index = self.first_index(server.get_users(), user)
                server.get_users().pop(user_index)
                for channel in channels_to_delete :
                    self.delete_channel(channel)
                for channel in server.get_channels() :
                    if user.id in channel.member_ids :
                        while user.id in channel.member_ids :
                            channel.member_ids.pop(self.first_index(channel.member_ids, user.id))
                messages2 = []
                for message in server.get_messages() :
                    if message.sender_id != user.id :
                        messages2.append(message)
                server.messages = messages2
                server.save()
                self.clear_screen()
                print(f'\n{colorama.Fore.LIGHTGREEN_EX}User {colorama.Fore.LIGHTCYAN_EX}{user_id}. {user.name}{colorama.Fore.LIGHTGREEN_EX} deleted successfully. \n{colorama.Style.RESET_ALL}')
            elif choice != 'n' :
                print(f'{colorama.Fore.LIGHTRED_EX}Unknown choice : {choice} {colorama.Style.RESET_ALL}\n')
            input('Press <Enter> to see users.')
            self.see_users()

    def see_messages(self, channel_id : 'int') :
        self.clear_screen()
        server = self.server
        channel = server.id_to_channel(channel_id) # Vérifié par see_channels
        if len(channel.member_ids) == 0 :
            print(f'{colorama.Fore.LIGHTRED_EX}No user in channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Fore.LIGHTRED_EX}. Please delete this channel. {colorama.Style.RESET_ALL}\n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()
            return None
        messages = [message for message in server.get_messages() if message.channel == channel.id]
        print(f'Channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}{channel.name}{colorama.Style.RESET_ALL} \n')
        print(f'Members : {Server.list_to_str([server.id_to_user(member_id).name for member_id in channel.member_ids], color_words = colorama.Fore.LIGHTCYAN_EX)} \n')
        for message in messages :
            user = server.id_to_user(message.sender_id)
            print(f'({message.reception_date}) - {colorama.Fore.LIGHTCYAN_EX}{user.name}{colorama.Style.RESET_ALL} : {message.content}')
        print('\n')
        print('a. Write a message')
        print('b. See channels')
        print('c. Back to main menu')
        print('\n')
        choice  = input('Select an option  : ')
        if choice == 'a' :
            self.write_message(channel.id)
        elif choice == 'b' :
            self.see_channels()
        elif choice == 'c' :
            self.main_menu()
        else :
            print(f'{colorama.Fore.LIGHTRED_EX}Unknown option : {choice} {colorama.Style.RESET_ALL}\n')
            input('Press <Enter> to go to main menu.')
            self.main_menu()

    def create_channel(self) :
        self.clear_screen()
        server = self.server
        channel_name = input('Channel name : ')
        result = server.post_channel(channel_name)
        if not result[0] :
            if len(result) == 1 : #Cas où un user ajouté au channel n'existe pas.
                print(f'{colorama.Fore.LIGHTRED_EX}No such user.{colorama.Style.RESET_ALL}\n')
                answer = input('Create new user ? (y/n) \n')
                if answer == 'y' :
                    self.create_user()
                elif answer != 'n' :
                    print(f'Unknown option : {answer} \n')
            else :
                print(f'\n{colorama.Fore.LIGHTRED_EX}Failed to post channel on remote server ({server.url}) : {result[1]}.{colorama.Style.RESET_ALL}\n')
        elif len(result) == 3 : 
            self.add_user(result[1], result[2])
        else :
            input('Press <Enter> to see channels.')
            self.see_channels()

    def delete_channel(self, channel : 'Channel' = None) :
        self.clear_screen()
        server = self.server
        choice = 'y'
        automatic = True
        if type(channel) == type(None) :
            automatic = False
            channel_id_str = input('Which channel do you want to delete ? (id)\n')
            while not Server.test_int(channel_id_str) :
                self.clear_screen()
                print(f'{colorama.Fore.LIGHTRED_EX}Please enter an integer.{colorama.Style.RESET_ALL}')
                channel_id_str = input('\nWhich channel do you want to delete ? (id)\n')
            channel_id = int(channel_id_str)
            if channel_id not in [channel.id for channel in server.get_channels()] :
                    print(f'\n{colorama.Fore.LIGHTRED_EX}No such channel.{colorama.Style.RESET_ALL}')
                    input('Press <Enter> to see channels.')
                    self.see_channels()
            else :
                channel = server.id_to_channel(channel_id)
                choice = input(f'\nChannel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Style.RESET_ALL} will be deleted. Confirm ? (y/n) \n')
        if choice == 'y' :
            channel_index = self.first_index(server.get_channels(), channel)
            server.get_channels().pop(channel_index)
            messages2 = []
            for message in server.get_messages() :
                if message.channel != channel.id :
                    messages2.append(message)
            server.messages = messages2 
            server.save()
            print(f'\n{colorama.Fore.LIGHTGREEN_EX}Channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Fore.LIGHTGREEN_EX} deleted successfully. \n{colorama.Style.RESET_ALL}')
        elif choice != 'n' :
            print(f'{colorama.Fore.LIGHTRED_EX}Unknown choice: {choice} {colorama.Style.RESET_ALL}\n')
        if not automatic :
            input('Press <Enter> to see channels.')
            self.see_channels()

    def add_user(self, user_id : 'int' = None, channel_id : 'int' = None) :
        self.clear_screen()
        server = self.server
        if channel_id == None :
            channel_id_str = input('To which channel ? (id)\n')
            while not Server.test_int(channel_id_str) :
                self.clear_screen()
                print(f'{colorama.Fore.LIGHTRED_EX}Please enter an integer.{colorama.Style.RESET_ALL}')
                channel_id_str = input('\nTo which channel ? (id)\n')
            channel_id = int(channel_id_str)
            if channel_id not in [channel.id for channel in server.get_channels()] :
                        print(f'{colorama.Fore.LIGHTRED_EX}\nNo such channel id.{colorama.Style.RESET_ALL}\n')
                        answer = input('Create new channel ? (y/n) \n')
                        if answer == 'y' :
                            self.create_channel()
                        elif answer == 'n' :
                            self.add_user()
                        else :
                            print(f'{colorama.Fore.LIGHTRED_EX}Unknown option : {answer} \n{colorama.Style.RESET_ALL}')
                            input('Press <Enter> to add user.')
                            self.add_user()
        channel = server.id_to_channel(channel_id)
        if user_id == None :
            ('\nUser Id ? \n')
            user_id_str = input('\nUser id ?\n')
            while not Server.test_int(user_id_str) :
                self.clear_screen()
                print(f'{colorama.Fore.LIGHTRED_EX}Please enter an integer.{colorama.Style.RESET_ALL}')
                user_id_str = input('\nUser id ?\n')
            user_id = int(user_id_str)
        if user_id not in [user.id for user in server.get_users()] :
            print(f'\n{colorama.Fore.LIGHTRED_EX}No such user id.{colorama.Style.RESET_ALL}')
            answer = input('Create new user ? (y/n) \n')
            if answer == 'y' :
                self.create_user()
            else :
                if answer != 'n' :
                    print(f'{colorama.Fore.LIGHTRED_EX}Unknown option : {answer} \n{colorama.Style.RESET_ALL}')
                input('\nPress <Enter> to see channels.')
                self.see_channels()
        elif not self.LEAVE :
            user = server.id_to_user(user_id)
            if user.id in channel.member_ids :
                print(f'\nUser {colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}{colorama.Style.RESET_ALL} is already in channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Style.RESET_ALL}')
            else :
                result = server.post_user_in_channel(channel_id, user_id)
                if result == True :
                    print(f'\n{colorama.Fore.LIGHTGREEN_EX}User {colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}{colorama.Fore.LIGHTGREEN_EX} has been added to channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name} \n{colorama.Style.RESET_ALL}')
                    choice = input('Do you want to add another user to this channel ? (y/n) \n')
                    if choice == 'y' :
                        self.add_user(channel_id = channel.id)
                    elif choice != 'n' :
                        print(f'\n{colorama.Fore.LIGHTRED_EX}Unknown option : {choice} \n{colorama.Style.RESET_ALL}')
                else :
                    print(f'\n{colorama.Fore.LIGHTRED_EX}Failed to add user {colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}{colorama.Fore.LIGHTRED_EX} to channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Fore.LIGHTRED_EX} on remote server ({server.url}) : {result}.{colorama.Style.RESET_ALL}')
            input('\nPress <Enter> to see channels.')
            self.see_channels()

    def remove_user(self) :
        self.clear_screen()
        server = self.server
        channel_id_str = input('From which channel ? (id)\n')
        while not Server.test_int(channel_id_str) :
            self.clear_screen()
            print(f'{colorama.Fore.LIGHTRED_EX}Please enter an integer.{colorama.Style.RESET_ALL}')
            channel_id_str = input('\nFrom which channel ? (id)\n')
        channel_id = int(channel_id_str)
        if channel_id not in [channel.id for channel in server.get_channels()] :
            print(f'\n{colorama.Fore.LIGHTRED_EX}No such channel. \n{colorama.Style.RESET_ALL}')
            input('Press <Enter> to see channels.')
            self.see_channels()
        else :
            channel = server.id_to_channel(channel_id)
            user_id_str = input('\nUser id ?\n')
            while not Server.test_int(user_id_str) :
                self.clear_screen()
                print(f'{colorama.Fore.LIGHTRED_EX}Please enter an integer.{colorama.Style.RESET_ALL}')
                user_id_str = input('\nUser id ?\n')
            user_id = int(user_id_str)
            if user_id not in [user.id for user in server.users] :
                print(f'{colorama.Fore.LIGHTRED_EX}No such user.{colorama.Style.RESET_ALL}')
            user = server.id_to_user(user_id)
            if user_id not in channel.member_ids :
                print(f'\n{colorama.Fore.LIGHTRED_EX}User {colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}{colorama.Fore.LIGHTRED_EX} is not in channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name} \n{colorama.Style.RESET_ALL}')
            else :
                choice = input(f'\nUser {colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}{colorama.Style.RESET_ALL} will be removed from channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Style.RESET_ALL}. Confirm ? (y/n) \n')
                if choice == 'y' :
                    answer = '' # Permet de savoir s'il faut supprimer le channel.
                    if len(channel.member_ids) == 1 :
                        answer = input(f'\nChannel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Style.RESET_ALL} will be deleted. Confirm ? (y/n) \n')
                        if answer not in ['y', 'n'] :
                            print(f'\n{colorama.Fore.LIGHTRED_EX}Unknown option : {answer} \n{colorama.Style.RESET_ALL}')
                        if answer != 'y' :
                            input('\nPress <Enter> to see channels.')
                            self.see_channels()
                            return None
                    channel.member_ids.pop(self.first_index(channel.member_ids, user.id))
                    print(f'\n{colorama.Fore.LIGHTGREEN_EX}User {colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}{colorama.Fore.LIGHTGREEN_EX} has been removed from channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}{colorama.Style.RESET_ALL}.')
                    if answer == 'y' :
                        self.delete_channel(channel)
                elif choice != 'n' :
                    print(f'\n{colorama.Fore.LIGHTRED_EX}Unknown option : {choice} \n{colorama.Style.RESET_ALL}')
            server.save()
            input('\nPress <Enter> to see channels.')
            self.see_channels()

    def write_message(self, channel_id : 'int') :
        self.clear_screen()
        server = self.server
        channel = server.id_to_channel(channel_id) # Vérifié par see_messages()
        if self.CLIENT_ID == None :
            print('\nPlease log in first.')
            input('\nPress <Enter> to log in.')
            self.log_in()
        else :
            user = server.id_to_user(self.CLIENT_ID)
        if not self.LEAVE and user.id not in channel.member_ids :
            print(f'{colorama.Fore.LIGHTRED_EX}User {colorama.Fore.LIGHTCYAN_EX}{user.id}. {user.name}{colorama.Fore.LIGHTRED_EX} is not in channel {colorama.Fore.LIGHTBLUE_EX}{channel.id} : {channel.name}{colorama.Fore.LIGHTRED_EX}. \n{colorama.Style.RESET_ALL}')
            choice = input('Do you want to add this user to this channel ? (y/n) \n')
            if choice == 'y' :
                self.add_user(user.id, channel.id)
            elif choice == 'n' :
                self.see_messages(channel.id)
            else :
                print(f'\n{colorama.Fore.LIGHTRED_EX}Unknown option : {choice} \n{colorama.Style.RESET_ALL}')
                input('Press <Enter> to go to main menu.')
                self.main_menu()
        elif not self.LEAVE :
            print(f'Message to channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}{channel.name}{colorama.Style.RESET_ALL}\n')
            message = input('\nMessage : ')
            result = server.post_message(channel.id, user.id, message)
            if result == True :
                self.see_messages(channel.id)
            else :
                print(f'\n{colorama.Fore.LIGHTRED_EX}Failed to post message on remote server ({server.url}) : {result}.\n{colorama.Style.RESET_ALL}')
                input(f'Press <Enter> to see messages in channel {colorama.Fore.LIGHTBLUE_EX}{channel.id}. {channel.name}.{colorama.Style.RESET_ALL}')
                self.see_messages(channel.id)


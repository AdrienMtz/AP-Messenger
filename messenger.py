from datetime import datetime
import json

with open('C:/Users/Adrien/UE12/AP/Server-Messenger.json', 'r') as f :
    server = json.load(f)

# Fonctions annexes

def id_to_object(str, id):
    L = []
    for object in server[str]:
        if object['id'] == id :
            L.append(object)
    if len(L) == 0 :
        print('No such id')
    elif len(L) > 2 :
        print(f'Error : 2 names for id {id}')
    else :
        return L[0]

def name_to_object(str, name) :
    L = []
    for object in server[str]:
        if object['name'] == name :
            L.append(object)
    if len(L) == 0 :
        print('No such name')
    elif len(L) > 2 :
        print(f'Error : 2 ids for name {name}')
    else :
        return L[0]

def premier_indice(L,e) :
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


def main_menu():
    print('\n')
    print('a. See users')
    print('b. See channels')
    print('c. Leave')
    print('\n')
    choice = input('Select an option : ')
    if choice == 'a':
        see_users()
    elif choice == 'b':
        see_channels()
    elif choice == 'c':
        print('\nBye !\n')
        save()
    else :
        print(f'Unknown option : {choice}')

def see_users():
    print('\n')
    for user in server['users']:
        print(user['id'], '. ', user['name'], '\n')
    print('a. Create user')
    print('b. Back to main menu')
    print('\n')
    choice = input('Select an option : ')
    if choice == 'a' :
        create_user()
    elif choice == 'b' :
        main_menu()
    else :
        print(f'Unknown option : {choice}')
        main_menu()

def see_channels():
    print('\n')
    for channel in server['channels']:
        names = ''
        for member in channel['member_ids']:
            username = id_to_object('users', member)['name']
            names = names + username + ', '
        names = names[:-2] + '.'
        print(channel['id'],'. ', channel['name'], ' : ', names, '\n')
    print('a. See messages')
    print('b. Create new channel')
    print('c. Add user to channel')
    print('d. Remove user from channel')
    print('e. Back to main menu')
    print('\n')
    choice = input('Select an option : ')
    if choice == 'a' :
        channel_id = input('Channel id : ')
        see_messages(int(channel_id))
    elif choice == 'b':
        create_channel()
    elif choice == 'c' :
        add_user()
    elif choice == 'd':
        remove_user()
    elif choice == 'e':
        main_menu()
    else :
        print(f'Unknown option : {choice}')
        main_menu()

def new_id(str):
    """ Id for new user or new channel """
    return max(stuff['id'] for stuff in server[str]) + 1

def create_user():
    name = input('Name : ')
    user = {'id' : new_id('users'), 'name' : name}
    server['users'].append(user)
    print('New user created : ', user['id'], '. ', name, '\n')
    save()
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

def see_messages(channel_id):
    messages = [message for message in server['messages'] if message['channel'] == channel_id]
    print(f'Channel {channel_id} : {id_to_object("channels", channel_id)["name"]}\n')
    for message in messages :
        user = id_to_object('users', message['sender_id'])['name']
        print(f'({message["reception_date"]}) - {user} : {message["content"]}')
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
    channel = {'id' : new_id('channels'), 'member_ids' : []}
    channel['name'] = input('Channel name : ')
    choice = '0'
    while choice != 'n' :
        choice = input('Do you want ot add a new user to this channel ? (y/n) \n')
        if choice == 'y':
            user_id = int(input('User Id : '))
            channel['member_ids'].append(user_id)
        elif choice != 'n':
            print(f'Unknown option : {choice}')
            main_menu()
    server['channels'].append(channel)
    print('New channel created')
    save()
    see_channels()

def add_user():
    channel_id = int(input('To which channel ? \n'))
    channel = id_to_object('channels', channel_id)
    user_id = int(input('User Id ? \n'))
    if user_id in channel['member_ids'] :
        print(f'User {user_id} is already in channel {channel_id}')
    else :
        channel['member_ids'].append(user_id)
        print(f'User {user_id} has been added to channel {channel_id}')
    save()
    see_channels()

def remove_user():
    channel_id = int(input('From which channel ? \n'))
    channel = id_to_object('channels', channel_id)
    user_id = int(input('User Id ? \n'))
    if user_id not in channel['member_ids'] :
        print(f'User {user_id} is not in channel {channel_id}')
    else :
        channel['member_ids'].pop(premier_indice(channel['member_ids'], user_id))
        print(f'User {user_id} has been removed from channel {channel_id}')
    save()
    see_channels()

def save():
    with open('C:/Users/Adrien/UE12/AP/Server-Messenger.json', 'w') as f :
            json.dump(server, f)

def write_message(channel_id) :
    print(f'Message to channel {channel_id} : {id_to_object("channels", channel_id)["name"]} \n')
    name = input('Who writes ? \n')
    user_id = name_to_object('users', name)['id']
    for channel in server['channels'] :
        if channel['id'] == channel_id :
            ch = channel
    if user_id not in channel['member_ids'] :
        print(f'User {name} is not in channel {channel["id"]} : {channel["name"]}.')
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
        server['messages'].append({'id' : new_id('messages'), 'reception_date' : str(datetime.now()).split('.')[0], 'sender_id' : name_to_object('users', name)['id'], 'channel' : channel_id, 'content' : message})
        save()
        see_messages(channel_id)


print('=== Messenger ===')
main_menu()


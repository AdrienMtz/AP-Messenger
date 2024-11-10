from datetime import datetime
import json

with open('C:/Users/Adrien/UE12/AP/Server-Messenger.json', 'r') as f :
    server = json.load(f)

# Fonctions annexes

def id_to_name(str, k):
    L = []
    for object in server[str]:
        if object['id'] == k :
            L.append(object['name'])
    if len(L) == 0 :
        print('No such id')
    elif len(L) > 2 :
        print(f'Error : 2 names for id {k}')
    else :
        return L[0]

def name_to_id(str, name) :
    L = []
    for object in server[str]:
        if object['name'] == name :
            L.append(object['id'])
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
    for ch in server['channels']:
        names = ''
        for j in ch['member_ids']:
            username = id_to_name('users', j)
            names = names + username + ', '
        names = names[:-2] + '.'
        print(ch['id'],'. ', ch['name'], ' : ', names, '\n')
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

def see_messages(k):
    L = [m for m in server['messages'] if m['channel'] == k]
    print('Channel ', k, ' : ', id_to_name('channels', k), '\n')
    for m in L :
        user = id_to_name('users', m['sender_id'])
        print(f'({m["reception_date"]}) - {user} : {m["content"]}')
    print('\n')
    print('a. See channels')
    print('b. Write a message')
    print('c. Back to main menu')
    print('\n')
    choice  = input('Select an option  : ')
    if choice == 'a' :
        see_users()
    elif choice == 'b' :
        write_message(k)
    elif choice == 'c' :
        main_menu()
    else :
        print(f'Unknown option : {choice}')
        main_menu()
    1  

def create_channel():
    ch = {'id' : new_id('channels'), 'member_ids' : []}
    ch['name'] = input('Channel name : ')
    choice = '0'
    while choice != 'n' :
        choice = input('Do you want ot add a new user to this channel ? (y/n) \n')
        if choice == 'y':
            user_id = int(input('User Id : '))
            ch['member_ids'].append(user_id)
        elif choice != 'n':
            print(f'Unknown option : {choice}')
            main_menu()
    server['channels'].append(ch)
    print('New channel created')
    save()
    see_channels()

def add_user():
    ch_id = int(input('To which channel ? \n'))
    user_id = int(input('User Id ? \n'))
    if user_id in server['channels'][ch_id-1]['member_ids'] :
        print(f'User {user_id} is already in channel {ch_id}')
    else :
        server['channels'][ch_id-1]['member_ids'].append(user_id)
        print(f'User {user_id} has been added to channel {ch_id}')
    save()
    see_channels()

def remove_user():
    ch_id = int(input('From which channel ? \n'))
    user_id = int(input('User Id ? \n'))
    if user_id not in server['channels'][ch_id-1]['member_ids'] :
        print(f'User {user_id} is not in channel {ch_id}')
    else :
        server['channels'][ch_id-1]['member_ids'].pop(premier_indice(server['channels'][ch_id-1]['member_ids'], user_id))
        print(f'User {user_id} has been removed from channel {ch_id}')
    save()
    see_channels()

def save():
    with open('C:/Users/Adrien/UE12/AP/Server-Messenger.json', 'w') as f :
            json.dump(server, f)

def write_message(k) :
    print(f'Message to channel {k} : {id_to_name("channels",k)} \n')
    name = input('Who writes ? \n')
    user_id = name_to_id('users', name)
    for channel in server['channels'] :
        if channel['id'] == k :
            ch = channel
    if user_id not in ch['member_ids'] :
        print(f'User {name} is not in channel {ch["id"]} : {ch["name"]}.')
        choice = input('Do you want to add a new user to this channel ? (y/n)\n')
        if choice == 'y' :
            add_user()
        elif choice == 'n' :
            see_messages(k)
        else :
            print(f'Unknown option : {choice}')
            main_menu()
    else :
        message = input('Message : ')
        server['messages'].append({'id' : new_id('messages'), 'reception_date' : str(datetime.now()).split('.')[0], 'sender_id' : name_to_id('users', name), 'channel' : k, 'content' : message})
        save()
        see_messages(k)


print('=== Messenger ===')
main_menu()


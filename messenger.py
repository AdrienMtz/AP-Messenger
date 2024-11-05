from datetime import datetime

server = {
    'users': [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ],
    'channels': [
        {'id': 1, 'name': 'Town square', 'member_ids': [1, 2]}
    ],
    'messages': [
        {
            'id': 1,
            'reception_date': datetime.now(),
            'sender_id': 1,
            'channel': 1,
            'content': 'Hi 👋'
        }
    ]
}

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
        print('Bye !')
        return None
    else :
        print(f'Unknown option : {choice}')
        main_menu()

def see_users():
    print('\n')
    for i in range(len(server['users'])):
        print(i+1, '. ', server['users'][i]['name'], '\n')
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

def id_to_name(str, k):
    L = []
    for object in server[str]:
        if object['id'] == k :
            L.append(object['name'])
    if len(L) == 0 :
        print('No such user')
    elif len(L) > 2 :
        print(f'Error : 2 users for id {k}')
    else :
        return L[0]

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

def create_user():
    name = input('Name : ')
    id = max(user['id'] for user in server['users']) + 1
    d = {'id' : id, 'name' : name}
    server['users'].append(d)
    print('New user created : ', d['id'], '. ', name, '\n')
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
    print('Channel ', k, ' : ', id_to_name('channels', k))
    for m in L :
        user = id_to_name('users', m['sender_id'])
        print('(', m['reception_date'], ')', ' - ', user, ' : ',  m['content'])
    print('a. See channels')
    print('b. Back to main menu')
    print('\n')
    choice  = input('Select an option  : ')
    if choice == 'a' :
        see_users()
    elif choice == 'b' :
        main_menu()
    else :
        print(f'Unknown option : {choice}')
        main_menu()
    1  

def create_channel():
    ch = {'id' : len(server['channels']) +1, 'member_ids' : []}
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
    see_channels()

def add_user():
    ch_id = int(input('To which channel ? \n'))
    user_id = int(input('User Id ? \n'))
    if user_id in server['channels'][ch_id-1]['member_ids'] :
        print(f'User {user_id} is already in channel {ch_id}')
    else :
        server['channels'][ch_id-1]['member_ids'].append(user_id)
        print(f'User {user_id} has been added to channel {ch_id}')
    see_channels()

def premier_indice(L,e) :
    for i in range(len(L)) :
        if L[i] == e :
            return i

def remove_user():
    ch_id = int(input('From which channel ? \n'))
    user_id = int(input('User Id ? \n'))
    if user_id not in server['channels'][ch_id-1]['member_ids'] :
        print(f'User {user_id} is not in channel {ch_id}')
    else :
        server['channels'][ch_id-1]['member_ids'].pop(premier_indice(server['channels'][ch_id-1]['member_ids'], user_id))
        print(f'User {user_id} has been removed from channel {ch_id}')
    see_channels()



print('=== Messenger ===')
main_menu()
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

def options():
    print('x. Main Menu')
    print('n. Create user')
    choice = input('Select an option : ')
    if choice == 'x':
        main_menu()
    elif choice == 'n':
        create_user()
    else :
        print('Unknown option :', choice)

def main_menu():
    print('1. See users')
    print('2. See channels')
    choice = input('Select an option : ')
    if choice == '1' :
        see_users()
    elif choice == '2' :
        see_channels()
    else :
        print('Unknown option :', choice)

def see_users():
    for i in range(len(server['users'])):
        print(i+1, '. ', server['users'][i]['name'], '\n')
    options()

def id_to_name(k):
    L = []
    for user in server['users']:
        if user['id'] == k :
            L.append(user['name'])
    if len(L) == 0 :
        print('No such user')
    elif len(L) > 2 :
        print('Error : 2 users for id {k}')
    else :
        return L[0]

def see_channels():
    for ch in server['channels']:
        names = ''
        for j in ch['member_ids']:
            username = id_to_name(j)
            names = names + username + ', '
        names = names[:-2] + '.'
        print(ch['id'],'. ', ch['name'], names, '\n')
    options()

def create_user():
    name = input('Name : ')
    d = {'id' : len(server['users'])+1, 'name' : name}
    server['users'].append(d)
    print('New user created : ', d['id'], '. ', name)
    options()





print('=== Messenger ===')
options()
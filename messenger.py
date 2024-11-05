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
    print('a. See users')
    print('b. See channels')
    choice = input('Select an option : ')
    if choice == 'a':
        see_users()
    elif choice == 'b':
        see_channels()
    else :
        print('Unknown option : ', choice)

def see_users():
    for i in range(len(server['users'])):
        print(i+1, '. ', server['users'][i]['name'], '\n')
    print('a. Create user')
    print('b. Back to main menu')
    choice = input('Select an option : ')
    if choice == 'a' :
        create_user()
    elif choice == 'b' :
        main_menu()
    else :
        print('Unknown option : ', choice)

def id_to_name(str, k):
    L = []
    for object in server[str]:
        if object['id'] == k :
            L.append(object['name'])
    if len(L) == 0 :
        print('No such user')
    elif len(L) > 2 :
        print('Error : 2 users for id {}'.format(k))
    else :
        return L[0]

def see_channels():
    for ch in server['channels']:
        names = ''
        for j in ch['member_ids']:
            username = id_to_name('users', j)
            names = names + username + ', '
        names = names[:-2] + '.'
        print(ch['id'],'. ', ch['name'], names, '\n')
    print('a. See messages')
    print('b. Back to main menu')
    choice = input('Select an option : ')
    if choice == 'a' :
        channel_id = input('Channel id : ')
        see_messages(int(channel_id))
    elif choice == 'b' :
        main_menu()
    else :
        print('Unknown option : ', choice)

def create_user():
    name = input('Name : ')
    d = {'id' : len(server['users'])+1, 'name' : name}
    server['users'].append(d)
    print('New user created : ', d['id'], '. ', name)
    print('a. See users')
    print('b. Back to main menu')
    choice = input('Select an option : ')
    if choice == 'a' :
        see_users()

def see_messages(k):
    L = [m for m in server['messages'] if m['channel'] == k]
    print('Channel {} : '.format(k), id_to_name('channels', k))
    for m in L :
        user = id_to_name('users', m['sender_id'])
        print('(', m['reception_date'], ') - ', user, ' : ',  m['content'])



print('=== Messenger ===')
main_menu()
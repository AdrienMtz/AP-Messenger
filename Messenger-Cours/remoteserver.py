import requests

from model import User
from model import Channel
from model import Message
from server import Server


class RemoteServer(Server) :
    def __init__(self, url : str) :
        self.url = url
    
    def __repr__(self) -> 'str' :
        return f'RemoteServer({self.url})'

# Fonctions utiles
    def id_to_user(self, id : 'int') -> 'User' :
        L = []
        for user in self.get_users() :
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
        for channel in self.get_channels() :
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
        for user in self.get_users() :
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
        for channel in self.get_channels() :
            if channel.name == name :
                L.append(channel)
        if len(L) == 0 :
            print('No such channel name.')
        elif len(L) > 2 :
            print(f'Error : 2 ids for name {name}')
        else :
            return L[0]

#Fonctionnalités de la classe

    def get_users(self) -> 'list[User]' :
        users_dict = requests.get(self.url + '/users').json()
        users = []
        for user_dict in users_dict :
            users.append(User(user_dict['id'], user_dict['name']))        
        return users

    def get_channels(self) -> 'list[Channel]' :
        channels_dict = requests.get(self.url + '/channels').json()
        channels = []
        for channel_dict in channels_dict :
            channel_dict['member_ids'] = []
            members = requests.get(self.url + f'/channels/{channel_dict['id']}/members').json()
            for member in members :
                channel_dict['member_ids'].append(member['id'])
            channels.append(Channel(channel_dict['id'], channel_dict['name'], channel_dict['member_ids'])) 
        return channels
    
    def get_messages(self) -> 'list[Message]' :
        messages_dict = requests.get(self.url + '/messages').json()
        messages = []
        for message in messages_dict :
            messages.append(Message(message['id'], message['reception_date'], message['sender_id'], message['channel_id'], message['content']))   
        return messages

    def post_user(self, name : 'str') -> 'list' :
        response = requests.post(self.url + 'users/create', json = {"name" : name})
        if response.status_code < 300 :
            return [True, response.json()['id']]
        else :
            return [False, response]
    
    def post_channel(self, channel_name : 'str') -> 'list' :
        response = requests.post(self.url + 'channels/create', json = {'name' : channel_name})
        if response.status_code>=300 :
            return [False, response]
        channel_dict = response.json()
        print(f'\nNew channel created : \n{channel_dict['id']}. {channel_dict['name']}.\n')
        user_id = int(input('\nWhich user do you want to add to this channel ? (id) \n'))
        if user_id not in [user.id for user in self.get_users()] :
            return [False]
        else :
            return [True, user_id, channel_dict['id']]

    def post_user_in_channel(self, channel_id : 'int', user_id : 'int') :
        response = requests.post(self.url + f'/channels/{channel_id}/join', json = {'user_id' : user_id})
        if response.status_code < 300 :
            return True
        else :
            return response

    def post_message(self, channel_id : 'int', sender_id : 'int', message : 'str') :
        response = requests.post(self.url + f'/channels/{channel_id}/messages/post', json = {'sender_id' : sender_id, 'content' : message})
        if response.status_code < 300 :
            return True
        else :
            return response

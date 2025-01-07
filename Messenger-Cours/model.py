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
import json
import colorama

from model import User, Channel, Message

class Server :
    # Pas besoin de déclarer __init__. Vous n'avez besoin
    # de déclarer que les fonctions qui sont appelées explicitement
    # sur des Server. Par ailleurs, cette forme n'est pas générique :
    # prendre des users, channels, et messages en paramètre
    # du constructeur n'a de sens que pour LocalServer.

    # Il vaut mieux éviter les noms de variables d'une seule lettre.
    # Par ailleurs, on réserve par convention les noms en majuscules
    # aux constantes (comme RESET_ALL ci-dessous).
    @staticmethod
    def list_to_str(word_list : 'list[str]', color_words : 'str' = '', color_commas : 'str' = colorama.Style.RESET_ALL) -> 'str' :
        '''Le nom de cette fonction est assez générique.

        Si vous n'avez pas de nom plus précis en tête,
        vous pouvez expliquer son objectif en une ligne
        et documenter son fonctionnement comme ceci.

        Ce commentaire est reconnu par les IDE, qui l'afficheront lors
        d'un survol du nom de la fonction.
        '''
        res = ''
        for word in word_list:
            res = res + color_words + word + color_commas + ', '
        res = res[ :-2] + color_commas + '.' + colorama.Style.RESET_ALL
        return res

    @staticmethod
    def test_int(input : 'str') :
        # Il y a déjà une fonction pour ça : https://docs.python.org/3/library/stdtypes.html#str.isdigit
        if len(input) == 0 :
            return False
        for character in input :
            if character not in [f'{i}' for i in range(10)] :
                return False
        return True

    # Les fonctions `from_dict` et `load` n'ont de sens que pour un LocalServer

    @classmethod
    def save(self) -> None:
        raise NotImplementedError()
    # Fonctions utiles

    def id_to_user(self, id : 'int') -> 'User':
        # Nous n'avons pas vu les exceptions en cours,
        # mais elles permettent de remonter des erreurs d'exécutions.
        # Ici ce code n'est pas censé être atteint, car la fonction
        # sera toujours appelée sur une sous-classe qui la redéfinira.
        # Si on oublie de la redéfinir, l'erreur sera assez explicite
        # (Not implemented)
        raise NotImplementedError()

    def id_to_channel(self, id : 'int') -> 'Channel' :
        raise NotImplementedError()

    def name_to_user(self, name : 'str') -> 'User' :
        raise NotImplementedError()

    def name_to_channel(self, name : 'str') -> 'Channel' :
        raise NotImplementedError()

#Fonctionnalités de la classe

    def get_users(self) -> 'list[User]' :
        raise NotImplementedError()

    def get_channels(self) -> 'list[Channel]' :
        raise NotImplementedError()
    
    def get_messages(self) -> 'list[Message]' :
        raise NotImplementedError()

    def post_user(self, name : 'str') -> 'list' :
        raise NotImplementedError()
    
    def post_channel(self, channel_name : 'str', client) -> 'list' :
        raise NotImplementedError()

    def post_user_in_channel(self, channel_id : 'int', user_id : 'int') : #LocalServer : renvoie un 'bool' ; RemoteServer : renvoie un 'bool' ou une 'requests.models.Response'
        raise NotImplementedError()

    def post_message(self, channel_id : 'int', sender_id : 'int', message : 'str') :
        raise NotImplementedError()

import argparse
import colorama

from localserver import LocalServer
from remoteserver import RemoteServer
from portailserver import PortailServer
from server import Server
from client import Client



parser = argparse.ArgumentParser()
parser.add_argument('--filename', '-f', help = 'enter json path', default = None) # 'C:/Users/Adrien/UE12/AP/Messenger-Cours/Server-Messenger.json'
parser.add_argument('--url', '-u', help = 'enter server url', default = 'https://groupe5-python-mines.fr')
parser.add_argument('--portail', '-p', action = 'store_true')
args = parser.parse_args()

server : Server
if args.filename is not None :
    server = LocalServer(args.filename)
elif args.url is not None :
    server = RemoteServer(args.url)
elif args.portail is not None :
    server = PortailServer()
else :
    print(f'{colorama.Fore.LIGHTRED_EX}Error: -f or -u should be set.{colorama.Style.RESET_ALL}')
    exit(-1)

local = type(server) == LocalServer

client = Client(server, local)
client.main_menu()

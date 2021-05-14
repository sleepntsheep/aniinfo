import os
from os.path import expanduser
import json

user_path = f"{expanduser('~')}/.config/aniinfo/config.json"
default_path = f'{os.path.dirname(__file__)}/config.json'

if os.path.exists(user_path): 
	config_path = user_path
else :
	config_path = default_path

def config_read():
	with open(config_path) as content:
		config   = json.load(content)
	return config

if __name__ == '__main__':
	print(config_read())
import argparse
import sys
import os
from .data import anime

def help():
    args = sys.argv[1:]
    if len(args) < 1:
        print( "Ayaya")
        print("to config, paste content of https://github.com/r4yish/aniinfo/blob/main/aniinfo/data/config.json\n to $HOME/.config/aniinfo/config.json")


parser = argparse.ArgumentParser()
parser.add_argument("--anime", '-a')
parser.add_argument("--manga", '-m')
parser.add_argument("--characters", '-c')

parser.add_argument("--page", '-p')
args = parser.parse_args()

if args.anime:
	anime.search_anime(args.anime, args.page)

elif args.manga:
	anime.search_manga(args.manga, args.page)

elif args.characters:
	anime.search_char(args.characters, args.page)
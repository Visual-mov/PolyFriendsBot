import tweepy, sys
from random import choice
from time import tzname
from datetime import datetime
from image_generator import PolyFriendGenerator

# The PolyFriends Bot
# Created by Ryan Danver 2020

# Files
NAMES = "names.txt"
HOBBIES = "hobbies.txt"
COLORS = "colors.txt"
FONT = "PixelSplitter-Bold.ttf"

SEED = ""

def main(argv):
    if len(argv) <= 0:
        print("Usage: python3 bot.py [--tweet] []")
        exit()
    generator = PolyFriendGenerator((1000,1000), 5, open(NAMES,"r"), FONT, SEED)
    time = datetime.now()
    generator.generate_image()
    generator.save_image()
    #print(generate_status(generator.name, time))

def generate_status(name, time):
    hobby = choice([s.replace('\n','').lower() for s in open(HOBBIES,"r").readlines()])
    color = choice([s.replace('\n','').lower() for s in open(HOBBIES,"r").readlines()])
    minutes = time.minute if len(str(time.minute)) != 1 else "0" + str(time.minute)
    return f"This is {name}, and they like {hobby}!\nCreated on: {time.month}/{time.day}/{time.year} at {time.hour}:{minutes} {tzname[0]}"

if __name__ == "__main__":
    main(sys.argv)
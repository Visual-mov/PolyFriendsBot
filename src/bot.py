import tweepy, sys, os
from random import choice
from time import tzname
from datetime import datetime
from image_generator import PolyFriendGenerator

# The PolyFriends Bot
# Created by Ryan Danver 2020

# Files
IMAGE_PATH = "./img.png"
KEYS_PATH = "./keys.txt"

NAMES = "./text/names.txt"
HOBBIES = "./text/hobbies.txt"
COLORS = "./text/colors.txt"
FONT = "./PixelSplitter-Bold.ttf"

SEED = ""

def main(argv):
    tweet = False
    for arg in argv:
        if arg == "--tweet": tweet = True

    generator = PolyFriendGenerator((1000,1000), 5, open(NAMES,"r"), FONT, "img.png", SEED)
    generator.generate_image()
    generator.save_image()
    
    if tweet:
        keys = list(getkeys())
        auth = tweepy.OAuthHandler(keys[0],keys[1])
        auth.set_access_token(keys[2],keys[3])
        api = tweepy.API(auth)
        time = datetime.now()
        try:
            api.update_with_media(IMAGE_PATH, generate_status(generator.name, time))
            print("Tweeted image.")
        except tweepy.TweepError as e:
            print(f"Tweepy error:\n{e.reason}")

def generate_status(name, time):
    hobby = choice([s.replace('\n','').lower() for s in open(HOBBIES,"r").readlines()])
    color = choice([s.replace('\n','').lower() for s in open(COLORS,"r").readlines()])
    minutes = time.minute if len(str(time.minute)) != 1 else "0" + str(time.minute)
    return f"This is {name}, and they like {hobby}!\nTheir favorite color is {color}.\nCreated on {time.month}/{time.day}/{time.year} at {time.hour}:{minutes} {tzname[0]}"

def getkeys():
    try:
        lines = open(KEYS_PATH,'r').readlines()
        for i in range(len(lines)):
            if i < 4: yield lines[i].replace('\n','')
    except FileNotFoundError:
        print("keys.txt not found")
        exit()

if __name__ == "__main__":
    main(sys.argv)
import tweepy, sys, os
from random import choice
from time import tzname
from datetime import datetime
from image_generator import PolyFriendGenerator

# The PolyFriends Bot
# Find the bot at https://twitter.com/PolyFriendsBot!
# Created by Ryan Danver 2020

# Files
KEYS_PATH = "keys.txt"

NAMES = "resources/names.txt"
HOBBIES = "resources/hobbies.txt"
COLORS = "resources/colors.txt"
FONT = "resources/PixelSplitter-Bold.ttf"

SEED = ""

def main(argv):
    tweet = False
    save_date = False
    for arg in argv:
        if arg == "--tweet":
            tweet = True
        elif arg == "--date_stamp":
            save_date = True

    time = datetime.now()
    file = real_path(get_filename(time) if save_date else "img.png")

    generator = PolyFriendGenerator((1000,1000), 5, rand_text(NAMES), real_path(FONT), file, SEED)
    generator.generate_image()
    generator.save_image()

    status = generate_status(generator.name, time)
    print(status)
    if tweet:
        keys = list(getkeys())
        auth = tweepy.OAuthHandler(keys[0],keys[1])
        auth.set_access_token(keys[2],keys[3])
        api = tweepy.API(auth)
        try:
            api.update_with_media(file, status)
            print("Tweeted image.")
        except tweepy.TweepError as e:
            print(f"Tweepy error:\n{e.reason}")

def generate_status(name, time):
    hobby, color = rand_text(HOBBIES), rand_text(COLORS)
    minutes = time.minute if len(str(time.minute)) != 1 else "0" + str(time.minute)
    return f"This is {name}, and they like {hobby}!\nTheir favorite color is {color}.\nCreated on {time.month}/{time.day}/{time.year} at {time.hour}:{minutes} {tzname[0]}"

def rand_text(file):
    try:
        return choice([s.replace('\n','') for s in open(real_path(file),"r").readlines()])
    except FileNotFoundError:
        print(f"Could not find {file}")
        exit()

def getkeys():
    try:
        lines = open(real_path(KEYS_PATH),'r').readlines()
    except FileNotFoundError:
        print("keys.txt not found")
        exit()
    for i in range(len(lines)):
        if i < 4: yield lines[i].replace('\n','')

def real_path(file):
    return f"{os.path.dirname(os.path.realpath(__file__))}/{file}"

def get_filename(time):
    return f"img_{time.month}{time.day}{time.year}{time.hour}{time.minute}{time.second}.png"

if __name__ == "__main__":
    main(sys.argv)
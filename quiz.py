#!/usr/bin/env python3

import glob
import flickrapi
import pprint
import xml
import os
import requests
import random
import json

DATA_DIRECTORY="data/"

def show_image(file_name):
    os.system("display \"" + file_name + "\" &")

def show_random_photo(directory):
    photo = random.choice(glob.glob(directory + "/*.jpg"))
    show_image(photo)

def main():
    while True:
        os.system("killall display")

        bird = random.choice(glob.glob(DATA_DIRECTORY + "/*")).split("/")[-1]

        show_random_photo(DATA_DIRECTORY + "/" + bird)

        guess=input("write name of the bird: ")

        if bird == guess:
            print("CORRECT!")
        else:
            print("INCORRECT!, was:", bird)


if __name__ == "__main__":
    main()

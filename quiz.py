#!/usr/bin/env python3

import flickrapi
import pprint
import xml
import os
import requests
import random
import json

def create_api():
    f=open("config.json", "r")

    config=json.load(f)

    api_key = config['api_key']
    api_secret = config['api_secret']

    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    return flickr

def show_image(file_name):
    os.system("display " + file_name + " &")

def download_url(url):
    file_name="/tmp/image.jpg"
    
    r=requests.get(url)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(1024*1024):
            fd.write(chunk)
    
    return file_name

def get_image_good_size(photo_sizes):
    for photo_size in photo_sizes[0]:
        if int(photo_size.attrib['height']) > 500:
            return photo_size.attrib['source']

    return None

def show_photo(bird):
    photos = flickr.photos.search(tags=bird)
    for photo in photos[0]:
        photo_sizes=flickr.photos.getSizes(photo_id=photo.attrib['id'])

        url=get_image_good_size(photo_sizes)
        file_name=download_url(url)
        show_image(file_name)
        break

def main():
    birds=["wood pigeon","dunnock","black headed gull"]
    while True:
        bird=random.choice(birds)

        show_photo(bird)

        guess=input("write name of the bird: ")

        if bird == guess:
            print("CORRECT!")
        else:
            print("INCORRECT!, was:", bird)


if __name__ == "__main__":
    flickr=create_api()
    main()

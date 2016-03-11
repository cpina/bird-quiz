#!/usr/bin/env python3

import flickrapi
import glob
import json
import os
import pprint
import random
import requests
import shutil
import xml

DATA_DIRECTORY="data/"

def create_api():
    f=open("config.json", "r")

    config=json.load(f)

    api_key = config['api_key']
    api_secret = config['api_secret']

    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    return flickr

def download_url(url):
    file_name="/tmp/image.jpg"
    
    r=requests.get(url)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(1024*1024):
            fd.write(chunk)
    
    return file_name

def select_url(photo_sizes):
    for photo_size in photo_sizes[0]:
        if int(photo_size.attrib['height']) > 500:
            return photo_size.attrib['source']

    return None

def download_photos(bird, number_of_photos):
    photos = flickr.photos.search(tags=bird)

    destination_directory = DATA_DIRECTORY + "/" + bird

    if not os.path.isdir(destination_directory):
        os.makedirs(destination_directory)

    downloaded = len(glob.glob(destination_directory + "/*.jpg"))
    for photo in photos[0]:
        downloaded += 1
        if downloaded > number_of_photos:
            break

        print("Downloading {} photo {} of {}".format(bird, downloaded, number_of_photos))
        photo_id = photo.attrib['id']
        photo_sizes = flickr.photos.getSizes(photo_id=photo_id)
        url=select_url(photo_sizes)

        file_name=download_url(url)

        shutil.move(file_name, destination_directory + "/" + photo_id + ".jpg")

    print("Done!")

def main():
    birds=["wood pigeon","dunnock","black headed gull"]
    number_of_photos=20

    for bird in birds:
        print("Will start downloading:",bird)

        download_photos(bird, number_of_photos)

if __name__ == "__main__":
    flickr=create_api()
    main()

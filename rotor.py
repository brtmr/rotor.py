#!/usr/bin/env python3
''' Background image rotation script for i3
'''

import os.path
import random
import subprocess
import sys
import time
import os

IMAGE_FOLDER = '/home/basti/owncloud/backgrounds'
UNSEEN_FILE = '/home/basti/owncloud/backgrounds_unseen'
ALL_IMAGES_FILE = '/home/basti/owncloud/backgrounds_all'
PERIOD = 60 * 5
DEVNULL = open(os.devnull, 'w')


def sync():
    UNSEEN = load(UNSEEN_FILE)
    ALL_IMAGES = load(ALL_IMAGES_FILE)
    '''opens the image folder and creates a list of all image pathnames.
    adds missing filenames to the rotor file, and removes those no longer 
    present.
    '''
    # use system find to search for images.
    command = [ 'find', IMAGE_FOLDER, '(', '-iname', '*\.jpeg', '-o', '-iname',
                '*\.jpg', '-o', '-iname', '*\.png', ')', '-print']
    find_result = subprocess.run(
            command, 
            stdout=subprocess.PIPE,)
    found_images = set(find_result.stdout.decode().split('\n'))
    new_images = found_images - ALL_IMAGES
    deleted_images = ALL_IMAGES - found_images
    UNSEEN      |= new_images
    ALL_IMAGES  |= new_images
    UNSEEN      -= deleted_images
    ALL_IMAGES  -= deleted_images
    save(ALL_IMAGES, ALL_IMAGES_FILE)
    save(UNSEEN, UNSEEN_FILE)


def save(collection, filename):
    with open(filename, 'w+') as f:
        for filename in collection:
            print(filename, file=f)


def load(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            filenames = f.read().splitlines()
        return set((filename for filename in filenames if filename))
    return set()


def display():
    ''' pick one unseen image and display. '''
    UNSEEN = load(UNSEEN_FILE)
    if not UNSEEN:
        # we have seen all images.
        # set UNSEEN to ALL_IMAGES to restart the rotation.
        UNSEEN = load(ALL_IMAGES_FILE)
    filename = random.choice(list(UNSEEN))
    subprocess.run(['feh', '--bg-fill', filename], stderr=DEVNULL)
    print(filename)
    UNSEEN.remove(filename)
    save(UNSEEN, UNSEEN_FILE)

while True:
    sync()
    display()
    # apply only once, if the -o argument was provided
    if sys.argv[-1] == '-o':
        break
    time.sleep(PERIOD) 

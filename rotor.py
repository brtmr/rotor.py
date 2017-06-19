#!/usr/bin/env python3
''' Background image rotation script for i3
'''

import json
import os.path
import subprocess
import random
import time

IMAGE_FOLDER = '/home/basti/owncloud/backgrounds'
ROTOR_FILE = '/home/basti/owncloud/backgrounds.json'
PERIOD = 60 * 5

ROTOR = {}

def sync():
    global ROTOR
    '''opens the image folder and creates a list of all image pathnames.
    adds missing filenames to the rotor file, and removes those no longer 
    present.
    '''
    # use system find to search for images.
    command = [ 'find', IMAGE_FOLDER, '(', '-iname', '*\.jpeg', '-o', '-iname',
                '*\.jpg', '-o', '-iname', '*\.png', ')', '-print']
    find_result = subprocess.run(
            command, 
            stdout=subprocess.PIPE )
    images = find_result.stdout.decode().split('\n')[:-1]
    load_rotor()
    # add the filenames that are new:
    new_images = [img for img in images if img not in ROTOR]
    for image in new_images:
        ROTOR[image] = 0
    removed_images = [img for img in ROTOR.keys() if img not in images]
    for image in removed_images:
        del ROTOR[image]
    save_rotor()

def save_rotor():
    global ROTOR
    with open(ROTOR_FILE, 'w+') as f:
        json.dump(ROTOR, f)

def load_rotor():
    global ROTOR
    if os.path.exists(ROTOR_FILE):
        with open(ROTOR_FILE) as f:
            ROTOR = json.load(f)

def display():
    global ROTOR
    ''' create the set of images that has the least amount of views, then 
    pick one and display. '''
    least_views = min(ROTOR.values())
    least_view_filenames = [fn for fn, views in ROTOR.items() 
                            if views == least_views]
    filename = random.choice(least_view_filenames)
    subprocess.run(['feh', '--bg-fill', filename])
    ROTOR[filename] += 1
    save_rotor()

while True:
    sync()
    display()
    time.sleep(PERIOD) 

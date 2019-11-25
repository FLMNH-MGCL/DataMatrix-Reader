import os
import subprocess
from timeit import default_timer as timer

valid_imgs = 'JPG', 'jpg', 'jpeg', 'JPEG']

def DirPrompt():
    target_directory = input('\nEnter the directory containing the properly named specimen images:\n --> ')

    # this check prevents trailing whitespace, an occurrence when dragging a folder into the terminal prompt in MacOS
    if target_directory.endswith(' '):
        target_directory = target_directory[:-1]

    # ensures trailing / is present
    if not target_directory.endswith('/') or not target_directory.endswith('\\'):
        target_directory += '/'

    return target_directory


def GetID(filename):
    id = filename.split('_')[1].split('.')[0]
    return int(id)


def CheckMatch(id, scanned_id):
    print('{} == {}...'.format(id, scanned_id), end='')
    if id == scanned_id:
        print('SUCCESS')
        return 0
    else:
        print('FAILURE')
        return 1


def GetImages(path):
    images = []
    for image in sorted(os.listdir(path)):
        if os.path.isfile(path + image) and image.split('.')[1] in valid_imgs:
            images.append(image)
    return images


def GetDirs(path):
    dirs = []
    for dir in sorted(os.listdir(path)):
        if os.path.isdir(path + dir + '/'):
            dirs.append(dir)
    return dirs
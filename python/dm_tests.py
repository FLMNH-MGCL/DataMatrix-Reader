"""
this program will the accuracy of the dmtxread program with already properly sorted / named files. 
Scanned in IDs will be compared with the hand recorded IDs to ensure accurate scans.
"""
import os
import subprocess
from timeit import default_timer as timer
from pyzbar.pyzbar import decode
from PIL import Image

valid_imgs = ['JPG', 'jpg', 'jpeg', 'JPEG', 'CR2', 'cr2']

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

"""
attempts to scan data from data matrix, returns result. 
result of image without data matrix will be empty string
"""
def DM_Read(path):
    p = subprocess.Popen('cat ' + path + ' | dmtxread --stop-after=1 -m40000 -Y50% -x50%', shell=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    scanned = str(p.stdout.readline())
    if scanned == "b\'\'":
        print("NOT FOUND IN DM_READ")
        scanned = ""
    elif len(scanned) > 0:
        #scanned = scanned.split(' ')[1]
        scanned = scanned.replace("b\'", '').replace(' ', '_').replace('\'', '')
    else:
        scanned = ""

    return scanned

"""
called after failed DM_Read. Attempts 1-d barcode read with pyzbar
"""
def BarcodeRead(path):
    decoded = decode(Image.open(path))
    
    if len(decoded) < 1:
        return ""

    data = str(decoded[0].data)

    if len(data) > 0:
        data = data.replace("b\'", '').replace(' ', '_').replace('\'', '')
    else:
        data = ""

    return data

"""
This script will not explore past the parent directory (ie there is no recursion).
The trials loop will repeat the scanning of the same folder X amount of times, instead.
"""
def RecursiveStandard(target_directory):
    for dir in GetDirs(target_directory):
        RecursiveStandard(target_directory + dir + '/')
    print('WORKING IN ' + target_directory)
    StandardTest(target_directory)

def StandardTest(target_directory):
    #total_failed = 0
    total_time = 0
    total_scans = 0
    
    global_start = timer()

    failed = 0
    passed = 0

    for image in GetImages(target_directory):
        path = target_directory + image
        true_id = GetID(image)
        scanned = DM_Read(path)

        # try again, looking for 1d instead
        if scanned == "":
            print("Could not find data matrix, search for barcode...")
            scanned = BarcodeRead(path)

        if scanned == "":
            print(image + '...FAILED...No Data Matrix or 1D Barcode found in image.')
            failed += 1
            total_scans += 1
            continue

        print(scanned)
        scanned_id = int(str(scanned.strip().replace('\'', '')).split('_')[1])
        
        ret = CheckMatch(true_id, scanned_id)
        if ret == 0:
            passed += 1
        else:
            failed += 1
        total_scans += 1

        
        #print ('\nTRAIL {} ENDED.\n{} / {} SCANNED CORRECTLY.\n{} SECONDS TOTAL, AVG {} IMAGES SCNANED PER SECOND.\n'.format(i + 1, passed, (passed + failed), 
        #        (end - start), (end - start) / (passed + failed)))
        #total_passed += passed
        #total_failed += failed
        

    global_end = timer()
    total_time = global_end - global_start
    print('ALL TRIALS COMPLETED.\nTOTAL ACCURACY: {} / {} CORRECTLY SCANNED\nTOTAL TIME: {}\nSECONDS PER SCAN: {}'.format(passed, total_scans, total_time, total_time / total_scans))


def StandardPrompt(target_directory):
    recurse = input ('\nDo you want to run recursively? \n [1]yes \n [2]no\n')
    if recurse == 'yes' or recurse == 'y' or recurse == '1':
        RecursiveStandard(target_directory)
    else:
        StandardTest(target_directory)

"""
This will test the differences in speed between decoding data matrices in JPG images versus PNG images
"""
def JPGvsPNG():
    JPG_directory = input('\nEnter the directory containing the properly named specimen images (JPG only):\n --> ')
    PNG_directory = input('\nEnter the directory containing the properly named specimen images (PNG only):\n --> ')

    # this check prevents trailing whitespace, an occurrence when dragging a folder into the terminal prompt in MacOS
    if JPG_directory.endswith(' '):
        JPG_directory = JPG_directory[:-1]
    if PNG_directory.endswith(' '):
        PNG_directory = PNG_directory[:-1]

    # ensures trailing / is present
    if not JPG_directory.endswith('/') or not JPG_directory.endswith('\\'):
        JPG_directory += '/'
    if not PNG_directory.endswith('/') or not PNG_directory.endswith('\\'):
        PNG_directory += '/'

    trials = int(input('\nHow many times would you like to run this test? (1-100)\n --> '))
    
    total_passed_JPG = 0
    total_failed_JPG = 0
    total_time_JPG = 0
    total_scans_JPG = 0

    total_passed_PNG = 0
    total_failed_PNG = 0
    total_time_PNG = 0
    total_scans_PNG = 0

    global_start = timer()
    for i in range(0, trials):
        print('\nSTARTING TRIAL {}\n'.format(i + 1))

        jpg_start = timer()
        for jpg in GetImages(JPG_directory):
            arg = JPG_directory + jpg
            true_id = GetID(jpg)
            p = subprocess.Popen('cat ' + arg + ' | dmtxread --stop-after=1', shell=True,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            scanned = str(p.stdout.readlines(-1)[0]).split(' ')[1]
            scanned_id = str(scanned.replace('\'', ''))
            
            ret = CheckMatch(true_id, scanned_id)
            if ret == 0:
                total_passed_JPG += 1
            else:
                total_failed_JPG += 1
            total_scans_JPG += 1
        jpg_end = timer()

        png_start = timer()
        for png in GetImages(PNG_directory):
            arg = PNG_directory + jpg
            true_id = GetID(jpg)
            p = subprocess.Popen('cat ' + arg + ' | dmtxread --stop-after=1', shell=True,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            scanned = str(p.stdout.readlines(-1)[0]).split(' ')[1]
            scanned_id = str(scanned.replace('\'', ''))
            
            ret = CheckMatch(true_id, scanned_id)
            if ret == 0:
                total_passed_PNG += 1
            else:
                total_failed_PNG += 1
            total_scans_PNG += 1
        png_end = timer()

        print ('\nTRAIL {} ENDED.\n{} / {} JPGs SCANNED CORRECTLY.\n {} / {} PNGs SCANNED CORRECTLY.\n{} JPGs SCNANED PER SECOND.\n{} PNGs SCNANED PER SECOND.\n'.format(i, total_passed_JPG, total_passed_JPG + total_failed_JPG, total_passed_PNG, 
            total_passed_PNG + total_failed_PNG, (jpg_end - jpg_start) / (total_passed_JPG + total_failed_JPG), 
            (png_end - png_start) / (total_passed_PNG + total_failed_PNG)))

    global_end = timer()

    print()


def main():
    test = input("Enter which test to run: \n [1] Standard Test (tests all images in directory) \n [2] JPG vs PNG (tests speed differences between JPG and PNG) \n --> ")
    if test == '1' or 'Standard Test':
        StandardPrompt(DirPrompt())
    else:
        JPGvsPNG()


# Driver
if __name__ == '__main__':
    main()

"""
So far, it seems that this script averages about 2.7-2.8 seconds (in a VM, 2.4 seconds on actual machine) to scan and 
decode the data matrix in a single image. This is the fastest I have accomplished, but when looking at potential workloads 
with the museum (potentially scanning hundreds or thousands of images in one sitting) time adds up. Doing the math, 
I've calculated about 37.5 hours to scan and decode 50,000 images in one sitting. 
"""
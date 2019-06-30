"""
this program will the accuracy of the dmtxread program with already properly sorted / named files. 
Scanned in IDs will be compared with the hand recorded IDs to ensure accurate scans.
"""
import os
import subprocess
from timeit import default_timer as timer

def GetID(filename):
    id = filename.split('_')[1].split('.')[0]
    return id


def CheckMatch(id, scanned_id):
    print('{} == {}...'.format(id, scanned_id), end='')
    if id == scanned_id:
        print('SUCCESS')
        return 0
    else:
        print('FAILURE')
        return 1

"""
This script will not explore past the parent directory (ie there is no recursion).
The trials loop will repeat the scanning of the same folder X amount of times, instead.
"""
def main():
    target_directory = input('\nEnter the directory containing the properly named specimen images:\n --> ')
    if not target_directory.endswith('/') or not target_directory.endswith('\\'):
        target_directory += '/'
    trials = int(input('\nHow many times would you like to run this test? (1-100)\n --> '))
    
    total_passed = 0
    total_failed = 0
    total_time = 0
    total_scans = 0
    
    global_start = timer()
    for i in range (0,trials):
        print('\nSTARTING TRIAL {}\n'.format(i + 1))

        failed = 0
        passed = 0

        start = timer()
        for image in os.listdir(target_directory):
            arg = target_directory + image
            true_id = GetID(image)
            p = subprocess.Popen('cat ' + arg + ' | dmtxread -n --stop-after=1', shell=True,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            scanned = str(p.stdout.readlines(-1)[0]).split(' ')[1]
            scanned_id = str(scanned.replace('\\n\'', ''))
            
            ret = CheckMatch(true_id, scanned_id)
            if ret == 0:
                passed += 1
            else:
                failed += 1
            total_scans += 1
        end = timer()

        print ('\nTRAIL {} ENDED.\n{} / {} SCANNED CORRECTLY.\n{} SECONDS TOTAL, AVG {} IMAGES SCNANED PER SECOND.\n'.format(i + 1, passed, (passed + failed), 
                (end - start), (end - start) / (passed + failed)))
        total_passed += passed
        total_failed += failed

    global_end = timer()
    total_time = global_end - global_start
    print('ALL TRIALS COMPLETED.\nTOTAL ACCURACY: {} / {} CORRECTLY SCANNED\nTOTAL TIME: {}\nSECONDS PER SCAN: {}'.format(total_passed, total_scans, total_time, total_time / total_scans))

if __name__ == '__main__':
    main()

"""
So far, it seems that this script averages about 2.7-2.8 seconds to scan and decode the data matrix in a single image.
This is the fastest I have accomplished, but when looking at potential workloads with the museum (potentially scanning 
hundreds or thousands of images in one sitting) time adds up. Doing the math, I've calculated about 37.5 hours to scan
and decode 50,000 images in one sitting. 
"""
import os
import subprocess

def GetID(filename):
    id = filename.split('_')[1].split('.')[0]
    return id


def CheckMatch(id, scanned_id):
    print('{} == {}...'.format(id, scanned_id), end='')
    if id == scanned_id:
        print('SUCCESS\n')
    else:
        print('FAILURE\n')

def main():
    # museum preformatted file names => MGCL_7digitnum
    path = input('\nPlease enter the path to the folder of images: \n --> ')
    if not path.endswith('/') or not path.endswith('\\'):
        path += '/'
    
    for image in os.listdir(path):
        arg = path + image
        true_id = GetID(image)
        p = subprocess.Popen('cat ' + arg + ' | dmtxread -n --stop-after=1', shell=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        scanned = str(p.stdout.readlines(-1)[0]).split(' ')[1]
        scanned_id = str(scanned.replace('\\n\'', ''))
        
        CheckMatch(true_id, scanned_id)



if __name__ == '__main__':
    main()
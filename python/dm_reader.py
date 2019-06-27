import os
import subprocess

"""
TODO:
-   Implement some way of knowing the side of the specimen (eg ventral, dorsal, lateral).
    -   This will involve keeping track of IDs that have been scanned X amount of times already, 
        perhaps 1st scan is always dorsal, 2nd is always ventral, etc. This would have to be thought of / 
        implemented during the actual phototaking sessions
    -   Use of dictionary (ID mapped to occurance count) is probably best
-   Implement recursive option for user
"""
def GetDirs(path):
    subdirectories = []
    for folder in os.listdir(path):
        if os.path.isdir(path + folder):
            subdirectories.append(folder)
    return subdirectories


def GetImages(path):
    images = []
    for image in os.listdir(path):
        if os.path.isfile(path + image):
            images.append(image)
    return images

def Rename(new_name, path):
    """
    
    """


def RecursiveRename(path):
    for dir in GetDirs(path):
        RecursiveRename(path + dir + '/')
    # Rename(path)


def DMRead():
    """
    """


def main():
    # museum preformatted file names => MGCL_7digitnum
    path = input('\nPlease enter the path to the folder of images: \n --> ')
    if not path.endswith('/') or not path.endswith('\\'):
        path += '/'
    
    for image in os.listdir(path):
        arg = path + image
        p = subprocess.Popen('cat ' + arg + ' | dmtxread -n --stop-after=1', shell=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        scanned = str(p.stdout.readlines(-1)[0]).replace("b\'", '').replace(' ', '_').replace('\\n\'', '')
        print (scanned)
        
        # rename file
        """
        new_name = scanned + '_' + view_of_spec + ext
        os.rename(path + )
        """



if __name__ == '__main__':
    main()
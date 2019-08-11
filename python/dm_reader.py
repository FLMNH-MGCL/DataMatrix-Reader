import os
import sys
import subprocess
#from tkinter import *
#from tkinter import StringVar
#from tkinter import filedialog
#import tkinter.messagebox
from pyzbar.pyzbar import decode
from PIL import Image
import time
import datetime

"""
TODO:
-   Implement some way of knowing the side of the specimen (eg ventral, dorsal, lateral).
    -   This will involve keeping track of IDs that have been scanned X amount of times already, 
        perhaps 1st scan is always dorsal, 2nd is always ventral, etc. This would have to be thought of / 
        implemented during the actual phototaking sessions
    -   Use of dictionary (ID mapped to occurance count) is probably best
- Look into implementing some way of reading the genus and species from the picture and sort it accordingly
√   Implement recursive option for user
√   Implement GUI option for user
"""

old_new_paths = []
occurrences = dict()
checkMGCL = False
SCAN_TIME = '30000'
valid_imgs = ['JPG', 'jpg', 'jpeg', 'JPEG', 'CR2', 'cr2']
"""
##############################
# ******** GUI CODE ******** #
class GUI:
    window = None
    target_dir = None
    recursively = False

    def __init__(self, window):
        self.window = self.InitWindow(window)

    def InitWindow(self, window):
        # ***** GENERAL WINDOW ***** #
        window.geometry("500x300")
        window.title('FLMNH Data Matrix Tool')
        #window.config(background='seashell3')
        #window.config(background='dimgray')

        # ***** STATUS BAR ***** #
        status_message = StringVar()
        status = Label(window, textvariable=status_message, bd=1, relief=SUNKEN, anchor=W)
        status_message.set("Waiting...")
        status.pack(side=BOTTOM, fill=X)
        
        # ***** TOP MENU ***** #
        menu = Menu(window)
        window.config(menu=menu)
        subMenu = Menu(menu)
        menu.add_cascade(label="Help", menu=subMenu)
        subMenu.add_command(label="Usage", command=self.HelpPromt)

        # ***** BUTTONS ***** #
        button = Button(window, text="Select Folder", command=self.SelectFolder)
        button.pack()

        toggle = IntVar()
        recursion_checkbox = Checkbutton(window, text='Recursive', variable=toggle, command= lambda: self.ToggleRecursive(toggle.get()))
        recursion_checkbox.pack()

        # review_data_checkbox = Checkbutton(window, text='Review MGCL (Legacy Cleanup)', variable=toggle, command= lambda: self.ToggleRevision(toggle.get()))
        # review_data_checkbox.pack()

        run_button = Button(window, text="Run", command= lambda: self.Run(status_message))
        run_button.pack()

        undo_button = Button(window, text="Undo Changes", command= lambda: self.Undo(status_message))
        undo_button.pack()

        quit_button = Button(window, text='Quit', command=window.destroy)
        quit_button.pack()

        return window


    def mainloop(self):
        self.window.mainloop()


    def Run(self, status_message):
        if self.target_dir == None:
            tkinter.messagebox.showerror(title='User Error', message='You must select a path first.')
            return

        # check trailing slash
        if not self.target_dir.endswith('/') or not self.target_dir.endswith('\\'):
            self.target_dir += '/'

        # no errors up to this point, update status to Running
        status_message.set('Running...')

        # check method
        if not self.recursively:
            ProcessData(self.target_dir)
        elif self.recursively:
            RecursiveProcessData(self.target_dir)

        # finished successfully
        status_message.set('Finished...')


    def Undo(self, status_message):
        # call non-class Undo function
        message = Undo()

        # update status bar / pop up message for error
        if message == 'There is nothing to undo.':
            tkinter.messagebox.showerror(title='User Error', message=message)
        else:
            status_message.set(message)


    def ToggleRecursive(self, value):
        if value == 0:
            self.recursively = False
        elif value == 1: 
            self.recursively = True


    def SelectFolder(self):
        self.target_dir = filedialog.askdirectory()


    def HelpPromt(self):
        prompt = str(
            "This program will help you to automate the renaming of specimen images by automatically finding and " \
            "decoding data matrices in the images. Simply select the target folder, select whether or not to run " \
            "the algorithm recursively and then hit run.\n\nTo run the algorithm recursively means that in addition " \
            "to the target directory (the folder you selected), every subdirectory (every folder within that folder) " \
            "will also undergo the scanning and renaming process. For example, if you select a target folder path of " \
            "/home/user/target/ and that filder contains a folder called random, running recursively will change files " \
            "in both target and random (and any additional subfolders in random).\n\nAll changes are temporarily recorded " \
            "in the program, so if you want to undo the script did just hit the undo button BEFORE you close the window!"
        )
        tkinter.messagebox.showinfo('Usage Help', prompt)
"""

#############################
# ******* MAIN CODE ******* #
def AskUsage():
    prompt = str(
            "This program will help to automate the renaming of specimen images by automatically finding and " \
            "decoding data matrices / barcodes in the images. On start, you will be prompted with whether or not " \
            "to view this help message. After which, the program will begin in 10 seconds. You will enter the path " \
            "to a folder containing the families of the collected speciment. On a mac, you may simply drag the folder " \
            "into the terminal window. You will then have the option to run the program recursively (scanning all " \
            "images in all subfolders) or standardly (scanning only in provided folder, no additional subfolders). " \
            "All changes to file names are temporarily saved, so please review the changes when prompted. You will " \
            "have the chance to undo the program's renaming ONLY WHEN PROMPTED, so it is important to check the results " \
            "before closing / terminating the project"
        )
    wanted = input("\nDo you want to see the usage information?\n [1]yes\n [2]no\n --> ")
    if wanted == '1' or wanted == 'y' or wanted == 'yes':
        print(prompt)
        time.sleep(10)

def GetDirs(path):
    subdirectories = []
    for folder in os.listdir(path):
        if os.path.isdir(path + folder):
            subdirectories.append(folder)
    return subdirectories


def GetImages(path):
    global checkMGCL
    images = []
    for image in os.listdir(path):
        if os.path.isfile(path + image):
            # if specified, do not rename images that already contain MGCL
            if "MGCL" not in image and checkMGCL == False:
                images.append(image)
            # default
            elif checkMGCL == True:
                images.append(image)
    return images
    

def RecursiveProcessData(path):
    for dir in GetDirs(path):
        RecursiveProcessData(path + dir + '/')
    ProcessData(path)


"""
takes path to image, scans matrix, returns new name
"""
def BarcodeRead(path):
    print("DMTX not found, looking for legacy barcode:")
    decoder = decode(Image.open(path))
    try:
        name = str(decoder[0].data)
    except:
        name = "nothing"
    return name

def DMRead(path):
    # stop if nothing is found after 15 seconds (15000 milliseconds)
    print('cat ' + path + ' | dmtxread --stop-after=1 -m' + SCAN_TIME)
    p = subprocess.Popen('cat ' + path + ' | dmtxread --stop-after=1 -m' + SCAN_TIME, shell=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return str(p.stdout.readline())

def ProcessData(path):
    print("\nWorking in... {}\n".format(path))
    
    global old_new_paths
    global occurrences

    for image in GetImages(path):
        # scanning
        ext = '.' + image.split('.')[1]
        arg = path + image

        print(image)

        new_name = DMRead(arg)
        if "MGCL" not in new_name:
            new_name = BarcodeRead(arg)
    
        # Replace garbage characters read in
        new_name = str(new_name).replace("b\'", '').replace(' ', '_').replace('\'', '')

        new_name = new_name.replace("b\'", '').replace(' ', '_').replace('\'', '')

        # get and check specimen id
        scanned_id = int(new_name.split('_')[1])
        
        if "lateral" in new_name.lower() or "lat" in new_name.lower():
            # Lateral
            new_name.replace("lat", "")
            new_name.replace("eral", "")
            new_name += '_L'
        
        else:
            if not occurrences or not scanned_id in occurrences:
                occurrences[scanned_id] = 1
            elif scanned_id in occurrences:
                occurrences[scanned_id] += 1

            if occurrences[scanned_id] == 1:
                # Dorsal
                new_name += '_D'
            elif occurrences[scanned_id] == 2:
                # Ventral
                new_name += '_V'
            else:
                new_name += '_MANUAL'


        # renaming
        # os.rename(path + image, path + (new_name + ext))
        print ('Renaming {} as {}\n'.format(path + image, path + new_name + ext))
        old_new_paths.append(tuple((path + image, path + new_name + ext)))


def Wait():
    wait = True
    print("Program completed... Please look over changes.")

    while wait == True:
        undo = input("Do you wish to undo?\n [1]yes\n [2]no\n --> ")
        if undo == '1' or undo == 'y' or undo =='yes':
            print(Undo())
            wait = False
        elif undo == '2' or undo == 'n' or undo == 'no':
            wait = False
        else:
            print('Input error. Invalid option.')
            continue

def Undo():
    global old_new_paths
    print('\nUndoing changes...')
    for old_path,new_path in old_new_paths:
        #os.rename(new_path, old_path)
        print ('Renaming {} back to {}\n'.format(new_path, old_path))
    return 'Success... Restored original state.'


def main():
    global SCAN_TIME 
    global checkMGCL
    
    #interface = input("\nWould you prefer to use a: \n [1]command-line interface \n [2]graphical interface \n--> ")
    interface = '1'
    if interface == '1':
        # museum preformatted file names => MGCL_7digitnum
        AskUsage()
        path = input('\nPlease enter the path to the folder of images: \n --> ')

        new_time = input('\nPlease enter the max amount of scan time to search for a matrix per image (in seconds): \n --> ')
        while not new_time.isdigit():
            new_time = input('Input error. Please enter an integer. \n --> ')
        SCAN_TIME = new_time + '000'

        askMGCL = 'nothing'
        while askMGCL == 'nothing':
            askMGCL = input('Would you like to scan images already containing (MGCL) in the filename \n [1] Yes \n [2] No \n --> ')
            if askMGCL.lower() == "yes" or askMGCL.lower() == "y" or askMGCL == "1":
                checkMGCL = True
            elif askMGCL.lower() == "no" or askMGCL.lower() == "n" or askMGCL == "2":
                checkMGCL = False
            else:
                askMGCL = 'nothing'
                print('Please enter a correct value: ')

        # this check removes trailing whitespace, an occurrence when dragging a folder into the terminal prompt in MacOS
        if path.endswith(' '):
            path = path[:-1]

        # ensures trailing '/' is present
        if not path.endswith('/') or not path.endswith('\\'):
            path += '/'

        method = input("\nChoose 1 of the following: \n [1]Standard (All files " \
            "in this directory level only) \n [2]Recursive (All files in this " \
            "directory level AND every level below) \n--> ")

        if method == '1':
            ProcessData(path)
            Wait()
        elif method == '2':
            RecursiveProcessData(path)
            Wait()
        else:
            print("Input error.")
            sys.exit(1)
    
    #elif interface == '2':
    #    window = Tk()
    #    my_gui = GUI(window)
    #    my_gui.mainloop()
    
    else:
        print("Input error.")
        sys.exit(1)

    print ('Program completed...\n')

if __name__ == '__main__':
    main()


"""
Notes / Bug report:
-   MacOS has a bug with tkinter revolving around a class (related to the folder finder dialog box)
    being defined twice. This is not a problem with tkinter, it is a problem with Apple. Regardless, 
    it is just a warning not an error. Since the definitions are identical it does not actually matter 
    which one is eventually chosen to be used by the OS.
-   There is a bug with tkinter and MacOS Mojave dark theme. The text on tkinter buttons / widgets is 
    not visible if dark mode is enabled. No such errors exist when running on Linux platforms, however.
"""

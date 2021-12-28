import os
from shutil import move
import shutil
class folder:
    def __init__(self, name, dir):
        self.name = name
        self.dir = dir
        self.path = os.path.join(dir, name)
        try:
            os.mkdir(self.path)
        except FileExistsError as e:
            print("Directory Already Exists!")
    
    def changeDir(self, target): 
        
        self.path = shutil.move(self.path, target)
        self.dir = target

    def kill(self):
        try:
            os.rmdir(self.path)
        except OSError:
            print("Folder is not Empty")
        self.name = None
        self.dir = None
        self.path = None


        
    
        
        
myFolder = folder('myFolder', 'D:\Libraries\Documents\Repositories\Personal\SchoolFolderAutomator')
myFolder.changeDir('D:\Libraries\Documents\Repositories\Personal')
myFolder.changeDir()
    

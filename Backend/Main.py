import json
from json.decoder import JSONDecodeError
import os
from shutil import move
import shutil

class Main:
    """"This is the Main Class of the Vincent Fang's Folder Automation Program. It handels almost all 
    backend functions.  

    :param None:

    """
    
    # TODO Figure out how to handle first time startup (prompt for archive path and find windows desktop path)
    def __init__(self):
        """Constructor Method: Creates config and Data jsons if not present in the PWD, else loads them into
        dictionaries
        Attempts to create an Archive Folder in the path specified in config
        :param None:
        :return None:
        """

        # Tags: 0 = Desktop     1 = Archive     2 = liveData    3 = archiveData     4 = Path    
        #       5 = inDesktop   6 = inArchive
        self.T0 = "Desktop"
        self.T1 = "Archive"
        self.T2 = "liveData"
        self.T3 = "archiveData"
        self.T4 = "Path"
        self.T5 = "inDesktop"
        self.T6 = "inArchive"
        self.T7 = "Backend"
        self.backend = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.backend, "config.json")
        try: 
            with open(os.path.join(self.backend, "config.json"),'r') as stream:
                self.config = json.load(stream)
        except FileNotFoundError as e:
            self.config = {
                "Archive": "D:\Libraries\Documents\Repositories\Personal\SchoolFolderManager\Archive",
                "Desktop": "D:\Libraries\Documents\Repositories\Personal\SchoolFolderManager\Desktop",
            }
            with open(os.path.join(self.backend,'config.json'), 'w') as f:
                json.dump(self.config, f)
        try:
            with open(os.path.join(self.backend,"data.json")) as stream:
                self.data = json.load(stream)
        except FileNotFoundError as e:
             self.data = {
                "archiveData" : {},
                "liveData" :    {}
             }
             with open(os.path.join(self.backend, 'data.json'),'w') as f:
                 json.dump(self.data,f)
        self.deskPath = 'Desktop'
         
        try:
            os.mkdir(self.config[self.T1])
        except FileExistsError:
            pass

        self.refresh()
         
    # TODO handle Archive dumping before dumping data.json
    def dump(self):
        """Loads any data and config changes into the json
        :param None:
        :return None:
        """
        with open(os.path.join(self.backend,'data.json'),'w') as f:
            json.dump(self.data,f)
        with open(os.path.join(self.backend,'config.json'),'w') as f:
            json.dump(self.config,f)
    
    
    def addFolder(self, Name):
        """Adds a folder, adds it to the Desktop directory
        :param Name: Name of folder to add
        :type Name: Mandetory str 

        :raise FileExisistsError: File already exists in Desktop
        :raise NotADirectoryError: User name is a windows reserved folder name
        :raise OSError: User name has illegal characteres
        :return None: 
        """
        if (type(Name) != str):
            raise ValueError("Folder Name can only be a String")

        if "\\" in Name or "/" in Name:
            raise OSError()
        toAdd = {
            "Path" : os.path.join(self.config[self.T0], Name),
            "inDesktop" : True,
            "inArchive" : False
        } 
        try:
            os.mkdir(toAdd[self.T4])
            self.data[self.T2][Name] = toAdd
        except FileExistsError:
            if Name not in self.data[self.T2].keys():
                self.data[self.T2][Name] = toAdd
                pass
            else:
                raise
        except NotADirectoryError as e:
            raise
        except FileNotFoundError:
            raise
        except OSError as e:
            raise
        

    # TODO Impliment error messages into the GUI 
    def addFolders(self, List):
            for name in List:
                try:
                    self.addFolder(name)
                except FileExistsError:
                    print(name + " already exists in " + self.config[self.T0])
                except NotADirectoryError:
                    print(name + " is a reserved folder name!")
                except FileNotFoundError:
                    print("Desktop directory lost! Reselect desktop directory!")
                except OSError:
                    print(name + " has invalid character!")

    # TODO add argument type check
    def changeDesktop(self, Path):
        """Changes the desktop folder in config to a new location. DOES NOT move folders
        :param Path: Path of new desktop directory
        :type Path: Mandetory str

        :return None:
        """
        self.config[self.T0] = Path
        liveList = self.data[self.T2].keys()
        for dir in liveList:
            self.data[self.T2][dir][self.T5] = False

    # TODO add argument type check
    def changeArchive(self,Path):
        """Changes the archive folder in config to a new location. DOES NOT move folders
        :param Path: Path of new desktop directory
        :type Path: Mandetory str 

        :return None:
        """
        self.config[self.T1] = Path
        archList = self.data[self.T3].keys()
        for dir in archList:
            self.data[self.T3][dir][self.T6] = False

    # TODO add argument type check
    def archive(self, Name):
        """ Moves a paticular file to archive. Moves folder and all contents. 
            Assumes Name is in liveData
            :param Name: Name of file to move
            :type Name: Mandetory str
        """
        try:
            path = self.data[self.T2][Name][self.T4]
        except KeyError:
            raise
        self.data[self.T2][Name][self.T4] = shutil.move(path, self.config[self.T1])  
        self.data[self.T2][Name][self.T5] = False
        self.data[self.T2][Name][self.T6] = True
        self.data[self.T3][Name] = self.data[self.T2].pop(Name)
        
    # TODO impliment dearchive, which should provide backwards functionality from archive
    def deArchive(self, Name):
        try:
            path = self.data[self.T3][Name][self.T4]
        except KeyError:
            raise
        self.data[self.T3][Name][self.T4] = shutil.move(path, self.config[self.T0])
        path = self.data[self.T3][Name][self.T5] = True
        path = self.data[self.T3][Name][self.T6] = False
        self.data[self.T2][Name] = self.data[self.T3].pop(Name)

    
    def archives(self, List):
        for name in List:
            try:
                self.archive(name)
            except KeyError:
                print(name + " is not in Desktop!")
        
        

    # TODO impliment refresh, should dump any changes to jsons, or check if folders are present
    def refresh(self):
        keysdata = self.data[self.T2].keys()
        keysarc = self.data[self.T3].keys()
        for name in keysdata:
            if os.path.exists(os.path.join(self.config[self.T0],name)):
                self.data[self.T2][name][self.T5] = True
            else:
                self.data[self.T2][name][self.T5] = False
        for name in keysarc:
            if os.path.exists(os.path.join(self.config[self.T1],name)):
                self.data[self.T3][name][self.T6] = True
            else:
                self.data[self.T3][name][self.T6] = False
        self.dump()
        


    # impliment repop, which should repopulate a paticular folder into either the Archive or Desktop
    # dir should be a boolean 0 for desktop, 1 for archive. This should not delete any folders, but simply
    # create another. This should also update the entries path and inArch/Desk fields
    def repop(self, Name, dir):
        if dir:
            try:
                os.mkdir(os.path.join(self.config[self.T1], Name))
                self.data[self.T3][Name][self.T6] = True
            except KeyError:
                raise 
        elif not dir:
            try:
                os.mkdir(os.path.join(self.config[self.T0],Name))
                self.data[self.T2][Name][self.T5] = True
            except KeyError:
                raise
    
    # TODO consider edgecase where os.path exists but is not in data
    def repopDesktop(self):
        keys = self.data[self.T2].keys()
        for Name in keys:
            if not self.data[self.T2][Name][self.T5]:
                path = self.data[self.T2][Name][self.T4]
                if os.path.exists(path):
                    shutil.move(path,self.config[self.T0])
                    self.data[self.T2][Name][self.T5] = True
                    self.data[self.T2][Name][self.T4] = os.path.join(self.config[self.T0], Name)
                else:
                    try:
                        self.repop(Name,0)
                    except KeyError:
                        print(Name + " not in data originally!")
        


    # TODO consider edgecase where os.path exists but is not in data
    def repopArchive(self):
        keys = self.data[self.T3].keys()
        for Name in keys:
            if not self.data[self.T3][Name][self.T6]:
                path = self.data[self.T3][Name][self.T4]
                if os.path.exists(path):
                    shutil.move(path,self.config[self.T1])
                    self.data[self.T3][Name][self.T6] = True
                    self.data[self.T3][Name][self.T4] = os.path.join(self.config[self.T1], Name)
                    
                else:
                    try:
                        print(Name + " archive has been lost! Merge manually, an empty directory " + Name +
                        " has been created.")
                        self.repop(Name,1)
                    except KeyError:
                        print(Name + " not in data originally!")

    # TODO Move all folders tracked in desktop to archive
    def rollover(self):
        return



main = Main()
main.repopArchive()
main.dump()

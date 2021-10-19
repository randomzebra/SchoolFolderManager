import json
from json.decoder import JSONDecodeError
import os

class Main:
    """"This is the Main Class of the Vincent Fang's Folder Automation Program. It handels almost all 
    backend functions.  

    :param None:

    """

    # TODO add a check for all files in Data to update "inDesktop field"
    def __init__(self):
        """Constructor Method: Creates config and Data jsons if not present in the PWD, else loads them into
        dictionaries
        Attempts to create an Archive Folder in the path specifiedd in config
        :param None:
        :return None:
        """
        try: 
            self.config = json.loads('config.json')
        except JSONDecodeError as e:
            self.config = {
                "Archive": "./Archive",
                "Desktop": "../Desktop"
            }
            with open('config.json', 'w') as f:
                json.dump(self.config, f)
        try:  
            self.data = json.loads('data.json')
        except JSONDecodeError as e:
             self.data = {
                "archiveData" : {},
                "liveData" :    {}
             }
             with open('data.json','w') as f:
                 json.dump(self.data,f)
        self.deskPath = 'Desktop'
         
        try:
            os.mkdir(self.config["Archive"])
        except FileExistsError:
            pass
         
    # TODO handle Archive dumping before dumping data.json
    def dump(self):
        """Loads any data and config changes into the json
        :param None:
        :return None:
        """
        with open('data.json','w') as f:
            json.dump(self.data,f)
        with open('config.json','w') as f:
            json.dump(self.config,f)
    
    
    # TODO create a invalid argument exception
    def addFolder(self, Name):
        """Adds a folder, adds it to the Desktop directory
        :param Name: Name of folder to add
        :type Name: Mandetory str 

        :return None:
        """
        toAdd = {
            "Path" : os.path.join(self.config["Desktop"], Name),
            "inDesktop" : True
        } 
        try:
            os.mkdir(toAdd['Path'])
        except FileExistsError as e:
            raise
        self.data["liveData"][Name] = toAdd

    # TODO impliment addFolder functinaltiy, which can take a list
    def addFolders(self, List):
        return
    
    # TODO update all data folder inDesktop fields to false
    # TODO add a variation that moves all folders in Data probably use a helper for archive
    def changeDesktop(self, Path):
        """Changes the desktop folder in config to a new location. DOES NOT move folders
        :param Path: Path of new desktop directory
        :type Path: Mandetory str

        :return None:
        """
        self.config["Desktop"] = Path

    # TODO update all folders inArchive fields to false
    # TODO add a variation that moves all folders in Data probably use a helper for archive
    def changeArchive(self,Path):
        """Changes the archive folder in config to a new location. DOES NOT move folders
        :param Path: Path of new desktop directory
        :type Path: Mandetory str 

        :return None:
        """
        self.config["Archive"] = Path

    # TODO impliment archive, which should move one folder to archive
    def archive(self):
        return

    # TODO impliment archives, which should take a list of folders
    def archives(self):
        return

    # TODO impliment refresh, should dump any changes to jsons, or check if folders are present
    def refresh(self):
        return

    # TODO impliment repop, which should repopulate a paticular folder into either the Archive or Desktop
    # dir should be a boolean 0 for desktop, 1 for archive. This should not delete any folders, but simply
    # create another. This should also update the entries path and inArch/Desk fields
    # TODO create a custom exception for a key not in the dictionary
    def repop(self, Name, dir):
        return
    
    def repopDesktop(self):
        return
    
    def repopArchive(self):
        return
    
    
main = Main()
main.addFolder("CS 1331")
main.dump()
        
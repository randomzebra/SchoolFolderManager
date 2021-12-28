package Backend;
import org.apache.commons.io.FileUtils;
import java.io.IOException;
import java.nio.file.FileAlreadyExistsException;
import java.nio.file.Files;
import java.nio.file.InvalidPathException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.ArrayList;
import java.lang.Boolean;
import org.json.JSONObject;

public class Main {
    HashMap<String, String> config;
    HashMap<String, HashMap<String,HashMap<String,Object>>> data;
   public Main() {
       config = new HashMap<String, String>();
       data = new HashMap<String,HashMap<String, HashMap<String,Object>>>();


       
       data.put("liveData", new HashMap<String,HashMap<String,Object>>());
       data.put("archiveData", new HashMap<String,HashMap<String,Object>>());

   } 

   private void initialize(){
        Path res = Paths.get("res");
        Path config = res.resolve("config.json");
        Path data = res.resolve("data.json");
        try {
		    Files.createDirectories(res);
	    } catch (IOException e) {}
        try {
			Files.createDirectories(config);
            //TODO initialize config from JSONobject https://javadoc.io/doc/org.json/json/latest/index.html
		} catch (IOException e) {}
        try {
			Files.createDirectories(data);
            //TODO inttialize data
		} catch (IOException e) {}
        
        
   }

   public boolean addFolder(String name) {
        Path newFolder = Paths.get(config.get("DESKTOP"), name);
        try {
            Files.createDirectory(newFolder);
        } catch (FileAlreadyExistsException e) {
            System.out.println("Directory already exists in Desktop!");
            return false;
        } catch (IOException e) {
            System.out.println("Unkown IO exception!");
            return false;
        }
        HashMap<String,Object> toAdd = new HashMap<String,Object>();
        toAdd.put("Path", newFolder);
        toAdd.put("inDesktop", true);
        toAdd.put("inArchive", false);
        data.get("liveData").put(name,toAdd);
        return true;
    }

    public ArrayList<Boolean> addFolders(ArrayList<String> names) {
        ArrayList<Boolean> listOfSuccess = new ArrayList<Boolean>();
        names.forEach((name) -> listOfSuccess.add(addFolder(name)));
        return listOfSuccess;
    }

    public boolean changeDesktop(Path desktop) {
        try {
            Paths.get(desktop.toString());
        } catch (InvalidPathException e) {
            System.out.println("Invalid path!");
            return false;
        }
        config.put("DESKTOP", desktop.toString());
        return true;

    }

    public boolean changeArchive(Path archive) {
        try {
            Paths.get(archive.toString());
        } catch (InvalidPathException e) {
            System.out.println("Invalid path!");
            return false;
        }
        config.put("ARCHIVE", archive.toString());
        return true;
    }

    public boolean archive(String name) {
        HashMap<String,Object> nameData = data.get("liveData").get(name);
        Path retPath = Paths.get(config.get("ARCHIVE")).resolve(name);
        try {

            FileUtils.moveDirectoryToDirectory(((Path)nameData.get("Path")).toFile(), Paths.get(config.get("ARCHIVE")).toFile(),false);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            return false;
        }  
        nameData = data.get("liveData").remove(name);
        nameData.put("Path", retPath);
        nameData.put("inDesktop", false);
        nameData.put("inArchive", true);
        data.get("archiveData").put(name, nameData);
        return true;
    }

    public boolean deArchive(String name) {
        HashMap<String,Object> nameData = data.get("archiveData").get(name);
        Path retPath = Paths.get(config.get("DESKTOP")).resolve(name);
        try {

            FileUtils.moveDirectoryToDirectory(((Path)nameData.get("Path")).toFile(), Paths.get(config.get("DESKTOP")).toFile(),false);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            return false;
        }  
        nameData = data.get("archiveData").remove(name);
        nameData.put("Path", retPath);
        nameData.put("inDesktop", true);
        nameData.put("inArchive", false);
        data.get("desktopData").put(name, nameData);
        return true;
    }

    public ArrayList<Boolean> archives(ArrayList<String> names) {
        ArrayList<Boolean> listOfSuccess = new ArrayList<Boolean>();
        names.forEach((name) -> listOfSuccess.add(archive(name)));
        return listOfSuccess;
    }

    public ArrayList<Boolean> deArchives(ArrayList<String> names) {
        ArrayList<Boolean> listOfSuccess = new ArrayList<Boolean>();
        names.forEach((name) -> listOfSuccess.add(deArchive(name)));
        return listOfSuccess;
    }



    public static void main(String[] args) {
       
    }
}


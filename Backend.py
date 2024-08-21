from math import ceil
import os
from win32api import GetLogicalDriveStrings
import psutil
class Path:

    def __init__(self, path: str) -> None:
        self.path = path

    def toStr(self) -> str:
        return self.path

    def getPrevDir(self) -> str:
        try:
            path = ""
            dir = Path(self.path).spDir()
            for i in range(len(dir)):
                if (len(dir) == i+1):
                    return (path[:(len(path)-1)] + path[(len(path)-1)+1:])
                else:
                    path = path + f"{dir[i]}/"
        except:
            return util().getBaseFolder().toStr()

    def isDir (self) -> bool:
        if (os.path.isdir(self.path)):
            return True
        else:
            return False

    def getListOfDir(self) -> list[str]:
        return os.listdir(self.path)

    def getMarkupListOfDir(self) -> list:
        blockSizes = ["lnk", "url", "ini", "exe"]
        res = []

        all = Path.getListOfDir(self)
        for i in range(len(all)):
            if (all[i].split(".")[0] != all[i]):
                obj = all[i].split(".")
                if (obj[1] in blockSizes):
                    continue
                else:
                    res.append(all[i])
            else:
                res.append(all[i])
        return res

    def spDir(self) -> list[str]:
        if (self.path in disk().getAllDisks()):
            return None
        else:
            separator = ""
            if ("\\" in self.path):
                separator = "\\"
            elif ("/" in self.path):
                separator = "/"
            else:
                return None
            return self.path.split(separator)

class util:

    def __init__(self):
        pass

    def writeOnConfig(self, data: list[str]):
        f = open("config", "w+", encoding="UTF-8")
        f.write((f"{data[0]}*{data[1]}"))
        f.close()

    def newConfig(self, data: dict[str:str]):
        f = open("config", "w+", encoding="UTF-8")
        for key in data.keys():
            f.write((f"{key}*{data[key]}\n"))
        f.close()

    def replOnConfig(self, repl: str):
        conf = {}
        oldConfig = util().getConfig()
        for key in oldConfig.keys():
            if key != repl.split("*")[0]:
                conf[key] = oldConfig[key]
            else:
                conf[key] = repl.split("*")[1]
        util().newConfig(conf)

    def getSep(self, str: str) -> str:
        separator = ""
        if ("\\" in str):
            separator = "\\"
        elif ("/" in str):
            separator = "/"
        else:
            return "None"
        return separator

    def getConfig(self) -> dict[str:str]:
        settings = {}
        f = open("config", "r", encoding="UTF-8")
        file = f.readlines()
        f.close()

        for i in range(len(file)):
            if ("\n" in file[i]):
                file[i] = file[i].replace("\n", "")

        for i in range(len(file)):
            obj = file[i].split("*")
            settings[obj[0]] = obj[1]

        return settings

    def getBaseFolder(self) -> Path:
        return Path(util().getConfig().get("baseDir"))

class folder:

    def __init__(self, folderName: str) -> None:
        self.folderName = folderName

    #Future
    def getListButtons(self) -> None:
        return None

    def openFolder(self, directory: Path) -> Path:
        return Path((directory.toStr() + (f"{util().getSep(directory.toStr())}{self.folderName}")))

    def openFoldere(self, directory: Path) -> Path:
        dir = directory.spDir()
        path = ""
        for i in range(len(dir)):
            if (len(dir) == i+1):
                path = path + f"{dir[i]}/{self.folderName}"
                continue
            path = path + f"{dir[i]}/"

        if (os.path.exists(path)):
            return Path(path)
        else:
            print(path)
            try:
                return Path(path)
            except:
                return Path(path.replace(f"/{self.folderName}", ""))

class file:

    def __init__(self, fileName: str):
        self.fileName = fileName

    def getListButtons(self) -> list[str]:
        return ["|Send-File|"]

class disk:

    def __init__(self):
        pass

    def byteToGB(self, bytes: int) -> int:
        return ceil((((bytes / 1024) / 1024) / 1024))

    def byteToMB(self, bytes: int) -> int:
        return ceil(((bytes / 1024) / 1024))

    def getDiskInfo(self, diskChar: str) -> str:
        data = psutil.disk_usage(diskChar)
        return f"{disk().byteToGB(data.free)} ГБ свободно из {disk().byteToGB(data.total)} ({data.percent}%)"

    def getAllDisks(self) -> list[str]:
        disks = GetLogicalDriveStrings()
        return disks.split('\000')[:-1]

    def isDisk(self, dir: str) -> bool:
        if (Path(dir).spDir() == None):
            for i in range(len(disk().getAllDisks())):
                if (dir == disk().getAllDisks()[i]):
                    return True
                else:
                    continue
            return False
        else:
            if (len(Path(dir).spDir()) > 1):
                return False
            else:
                return True

    def getDisk(self, dir: str) -> str:
        if (disk().isDisk(dir)):
            for i in range(len(disk().getAllDisks())):
                if (dir == disk().getAllDisks()[i]):
                    return disk().getAllDisks()[i].replace("\\\\", "\\")
                else:
                    continue
        else:
            return "None"

    def getListButtons(self) -> list[str]:
        lst = []
        disks = disk().getAllDisks()
        for i in range(len(disks)):
            lst.append(f"{disks[i]} | {disk().getDiskInfo(disks[i])}")

        return lst

from math import ceil
import os
from win32api import GetLogicalDriveStrings
import psutil
class Path:

    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return self.path

    def get_prev_dir(self):
        try:
            path = ""
            directory = Path(self.path).split()
            for i in range(len(directory)):
                if len(directory) != i+1:
                    path = path + f"{directory[i]}/"

            return path[:(len(path) - 1)] + path[(len(path) - 1) + 1:]
        except Exception:
            return str(Util().getBaseFolder())

    def is_dir (self) -> bool:
        return os.path.isdir(self.path)

    def get_dir_list(self) -> list[str]:
        return os.listdir(self.path)

    def get_markup_list_dir(self) -> list:
        blocking_end = ["lnk", "url", "ini", "exe"]
        res = []

        files = Path.get_dir_list(self)
        for el in files:
            obj = el.split(".")
            if obj[0] != el:
                if obj[-1] not in blocking_end:
                    res.append(el)
            else:
                res.append(el)
        return res

    def get_separator(self) -> str:
        return "/" if "/" in self.path else "\\"

    def split(self) -> list[str] | None:
        return self.path.split(self.get_separator()) if self.path not in disk().getAllDisks() else None

class Util:

    def write_config(self, data: list[str]):
        f = open("config", "w+", encoding="UTF-8")
        f.write((f"{data[0]}*{data[1]}"))
        f.close()

    def new_config(self, data: dict[str:str]):
        f = open("config", "w+", encoding="UTF-8")
        for key in data.keys():
            f.write((f"{key}*{data[key]}\n"))
        f.close()

    def repl_config(self, repl: str):
        conf = {}
        oldConfig = Util().get_config()
        for key in oldConfig.keys():
            if key != repl.split("*")[0]:
                conf[key] = oldConfig[key]
            else:
                conf[key] = repl.split("*")[1]
        Util().new_config(conf)

    def get_config(self) -> dict[str:str]:
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
        return Path(Util().get_config().get("baseDir"))

class folder:

    def __init__(self, folderName: str) -> None:
        self.folderName = folderName

    #Future
    def getListButtons(self) -> None:
        return None

    def openFolder(self, directory: Path) -> Path:
        return Path((str(directory) + (f"{directory.get_separator()}{self.folderName}")))

    def openFoldere(self, directory: Path) -> Path:
        dir = directory.split()
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
        if (Path(dir).split() == None):
            for i in range(len(disk().getAllDisks())):
                if (dir == disk().getAllDisks()[i]):
                    return True
                else:
                    continue
            return False
        else:
            if (len(Path(dir).split()) > 1):
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

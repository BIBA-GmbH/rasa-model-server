from datetime import datetime
from os import scandir, listdir, DirEntry
from os.path import isfile, isdir, relpath, join, getsize

from config import download_folder

class Scaner:
    def __init__(self, path):

        self.entries = [Entry(entry) for entry in scandir(path.encode())]
        self.entries.sort(
            key=lambda e: e.modified_time.timestamp(),
            reverse=True
        )

        self.latest_entry = max(self.entries, key=lambda e: e.modified_time.timestamp())

class Entry:

    def __init__(self, entry: DirEntry):
        
        self.name = entry.name.decode()
        
        self.path = entry.path.decode()
        self.rel_path = relpath(self.path, download_folder)
        
        self.is_dir = entry.is_dir()

        # save created_time and modified_time as date objects to provide 
        # better date comparison
        self.created_time = datetime.fromtimestamp(entry.stat().st_ctime)
        self.modified_time = datetime.fromtimestamp(entry.stat().st_mtime)

        self.size = self._human_readable_size(self._get_size(entry.path))

    def _get_size(self, path):
       
        total_size = getsize(path)
       
        if isdir(path):

            for item in listdir(path):
            
                item_path = join(path, item)
            
                if isfile(item_path):
                    total_size += getsize(item_path)
                elif isdir(item_path):
                    total_size += self._get_size(item_path)
       
        return total_size

    def _human_readable_size(self, size):
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        human_fmt = '{0:.2f} {1}'
        human_radix = 1024.

        for unit in units[:-1]:
            if size < human_radix: 
                return human_fmt.format(size, unit)
            size /= human_radix

        return human_fmt.format(size, units[-1])
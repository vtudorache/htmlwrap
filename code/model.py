import csv
import datetime

Date = datetime.date

class FileWrapper(object):
    
    def __init__(self, filelike, length=0, blocksize=1024):
        self.filelike = filelike
        self.length = length
        self.blocksize = blocksize
        self.count = 0
        
    def __iter__(self):
        return self
    

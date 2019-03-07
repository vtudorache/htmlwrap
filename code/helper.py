class FileWrapper(object):
    
    def __init__(self, filelike, length=0, blocksize=1024):
        self.filelike = filelike
        self.length = length
        self.blocksize = blocksize
        self.count = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.filelike:
            blocksize = self.length - self.count
            if (self.length == 0) or (blocksize > self.blocksize):
                blocksize = self.blocksize
            if blocksize > 0:
                content = self.filelike.read(blocksize)
                if content:
                    self.count += len(content)
                    return content
        raise StopIteration
    
    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()
        self.filelike = None
   

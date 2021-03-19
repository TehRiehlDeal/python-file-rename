class File:

    def __init__(self, id, path, startName, endName="", multiEpisode=False, numEp=0):
        self.id = id
        self.path = path
        self.startName = startName
        self.endName = endName
        self.multiEpisode = multiEpisode
        self.numEp = numEp

    def setID(self, id):
        self.id = id
    
    def setPath(self, path):
        self.path = path
    
    def setStartName(self, startName):
        self.startName = startName

    def setEndName(self, endName):
        self.endName = endName

    

from BaseClasses.Instruments import *

class Ensemble(object):
    def __init__(self, ensemble):
        if ensemble == 'JoJoQuartet':
            self.instrumentList = ['flute','clarinet','trumpet','tuba']
            self.instClassList = ['Flute','Clarinet','Trumpet','Tuba']
            self.numPartsList = [1,1,1,1]
            self.Name = ensemble
        elif ensemble == 'JoJoTrio':
            self.instrumentList = ['flute','clarinet','tuba']
            self.instClassList = ['Flute','Clarinet','Tuba']
            self.numPartsList = [1,1,1]
            self.Name = ensemble
        else:
            raise ValueError('ERROR: Ensemble \'' + ensemble + '\' not recognized.')
        self.numTracks = len(self.instrumentList)
    
            
        
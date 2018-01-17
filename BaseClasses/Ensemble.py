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
        elif ensemble == 'JoJoQuintet':
            self.instrumentList = ['flute','clarinet','trumpet','violin','tuba']
            self.instClassList = ['Flute','Clarinet','Trumpet','Violin','Tuba']
            self.numPartsList = [1,1,1,1,1]
            self.Name = ensemble
        elif ensemble == 'SATB':
            self.instrumentList = ['soprano', 'alto', 'tenor', 'bass']
            self.instClassList = ['Soprano', 'Alto', 'Tenor', 'Bass']
            self.numPartsList = [1,1,1,1]
            self.Name = ensemble
        elif ensemble == 'JoJoOctet':
            self.instClassList = ['Flute','Clarinet','Trumpet','Tuba','Violin','Viola','Cello','DoubleBass']
            self.instrumentList = []
            for inst in self.instClassList:
                self.instrumentList.append(inst.lower())
        else:
            raise ValueError('ERROR: Ensemble \'' + ensemble + '\' not recognized.')
        self.numTracks = len(self.instrumentList)
    
            
        
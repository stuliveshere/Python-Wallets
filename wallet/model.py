import tables as tb
import pandas as pd

class Observables():

    def __init__(self):
        columns = ['data','amount', 'desc', 'account']
        index = None
        self.data = pd.DataFrame(index=index, columns=columns)
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        '''
        data is a dictionary of sub-dictionary
        if sub-dictionary exists, update values
        in sub-dictionary, else create sub-
        dictionary.
        '''
        for key in data.keys():
            if key in self.data.keys():
                for subkey in data[key]:
                    self.data[key][subkey] = data[key][subkey]
            else:
                self.data[key] = data[key]
        self._docallbacks()

    def remove(self, key):
        del self.data[key]
        self._docallbacks()


    def get(self, key, subkey=None):
        if subkey:
            return self.data[key][subkey]
        elif key:
            return self.data[key]
        else:
            return self.data

    def unset(self):
        self.data = {}
        
class Model():
    ''' model is a dictionary of dictionaries.
    ie node dictionary contains a dictionary of parameters for each node
    '''
    
    def __init__(self, store):
        self.store = pd.HDFStore(store)
        self.model = Observables()

    def set(self, data):
        self.model.set(data)

    def get(self, key=None, subkey=None):
        data = self.model.get(key, subkey)
        return data

    def remove(self, key):
        self.model.remove(key)
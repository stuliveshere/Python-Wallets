from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import sys
from view import *
from model import *
import os

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

class Gui(object):
    ''' main gui controller'''
    def __init__(self, root):
        self.parent = root
        self.view = GuiView(root)
        self.view.protocol('WM_DELETE_WINDOW', self.quit)
        sys.stdout = StdoutRedirector(self.view.log.text_box)
        sys.stderr = StdoutRedirector(self.view.log.text_box)
        #bindings
        self.view.fileMenu.entryconfig(1, command=self.new)
        self.view.fileMenu.entryconfig(2, command=self.open)
        self.view.fileMenu.entryconfig(9, command=self.quit)
        self.view.toolMenu.entryconfig(1, command=self.import_statements)
        #model
        self.model = Model()

    def quit(self):
        sys.exit()
        
    def new(self):
        ''' 
        create new db.  gets filename and 
        passes to model class for initialisation
        '''
        options = {
        'defaultextension':'h5', 
        'filetypes':[('hdf5 files', '*.h5'),('all files', '.*')],
        'initialdir':'../', 
        'initialfile':'budget.h5',  
        'parent':self.view, 
        'title':'Select new db file',
        }
        self.db_name = asksaveasfilename(**options)
        print 'creating ', self.db_name
        self.model_new()

    def model_new(self):
        self.store = pd.HDFStore(self.db_name)

    def open(self):
        ''' 
        open existing db. gets filename and
        passes to model class for openning
        '''
        options = {
        'defaultextension':'h5', 
        'filetypes':[('hdf5 files', '*.h5'),('all files', '.*')],
        'initialdir':'../', 
        'initialfile':'budget.h5',  
        'parent':self.view, 
        'title':'Select new db file',
        }
        self.db_name = askopenfilename(**options)
        self.model_open()       
 
    def model_open(self):
        pass
        
        
    def import_statements(self):
        options = {
        'defaultextension':'.csv', 
        'filetypes':[('csv', '.csv')], 
        'initialdir':'../', 
        'initialfile':None, 
        'multiple':1, 
        'parent':self.parent, 
        'title':'select statement file',        
        }
        filelist = askopenfilenames(**options)
    



def main():
    root = Tk()
    root.withdraw()
    app = Gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()

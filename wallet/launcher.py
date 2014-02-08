from Tkinter import *
from tkFileDialog import *
import sys
from view import *
#from model import *

class Gui(object):
    ''' main gui controller'''
    def __init__(self, root):
        self.parent = root
        self.view = GuiView(root)
        self.view.protocol('WM_DELETE_WINDOW', self.quit)
        #bindings
        self.view.fileMenu.entryconfig(1, command=self.new)
        self.view.fileMenu.entryconfig(9, command=self.quit)
        self.view.toolMenu.entryconfig(1, command=self.import_statements)
        
        #model
        

    def quit(self):
        sys.exit()
        
    def new(self):
        '''new database wizard'''
        filename = None
        db = WizardView(self.parent, filename)
        
        #if self.v: self.h5file = tb.openFile(self.v.get(), mode = "w", title='db')
        
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

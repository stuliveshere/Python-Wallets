from Tkinter import *
from tkFileDialog import *
import sys
from view import *
from model import *
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
        
        

    def quit(self):
        sys.exit()
        
    def new(self):
        '''new database'''
        wizard = self.view.new_db_wizard()
        self.view.wizard.buttonlist[-1].configure(command=self.model_init)
        self.view.pagelist[2].tree.bind('<<TreeviewSelect>>', self.onClick)
        
    def onClick(self, event):
        thing =  self.view.pagelist[2].tree.selection()
        selection = self.view.pagelist[2].tree.item(thing)['text']
        parent = self.view.pagelist[2].tree.parent(thing)
        dir = self.view.pagelist[2].tree.item(parent)
        if selection[-3:] == '.h5': 
            print self.view.pagelist[2].tree.item(thing)
            print parent
            #need to generate full file path
            self.view.wizard.buttonlist[0].configure(state=ACTIVE)
        
    def model_init(self):
        filename = self.view.pagelist[1].v.get()
        self.view.wroot.destroy()
        self.store = pd.HDFStore(store)
        self.model = Model(filename)
        
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

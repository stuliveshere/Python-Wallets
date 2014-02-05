from Tkinter import *
from tkFileDialog import *
import sys
from view import *
#from model import *

class Wizard(object):
    def __init__(self, parent):
        '''new project wizard controller'''
        self.parent = parent
        self.view = WizardView(self.parent)


class Gui(object):
    ''' main gui controller'''
    def __init__(self, root):
        self.parent = root
        self.view = GuiView(root)
        self.view.protocol('WM_DELETE_WINDOW', self.quit)
        #bindings
        self.view.fileMenu.entryconfig(1, command=self.new)
        self.view.fileMenu.entryconfig(9, command=self.quit)

    def quit(self):
        sys.exit()
        
    def new(self):
        '''new database wizard'''
        Wizard(self.parent)


def main():
    root = Tk()
    root.withdraw()
    app = Gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()

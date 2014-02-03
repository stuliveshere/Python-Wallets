from Tkinter import *
from ttk import *
from tkFileDialog import *
import sys


class View(Toplevel):

    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.title('Python-Wallets')
        self.geometry("1280x1024")
        self.frame = Frame(self, name='descrip')
        self.frame.pack(side=TOP, fill=BOTH, expand=Y)
        self._menu()
        self._notebook()

    def _notebook(self):
        notebook = Notebook(self.frame)
        notebook.enable_traversal()  
        notebook.pack(fill='both', expand=Y, padx=5, pady=5)
        View_Config(notebook)

    def _menu(self):
        self.menuBar = Menu(self)
        self["menu"] = self.menuBar
        self.fileMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_command(label="Open...")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Close")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Save")
        self.fileMenu.add_command(label="Save As...")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Quit")
        self.toolMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label="Tools", menu=self.toolMenu)
        self.toolMenu.add_command(label="template")
        self.helpMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="About")


class View_Config():
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.view = parent.add(self.frame, text='Configure')


class controller(Toplevel):
    def __init__(self, root):
        self.parent = root
        self.view = View(root)
        self.view.protocol('WM_DELETE_WINDOW', self.quit)
        
        self.view.fileMenu.entryconfig(1, command=self.new)
        self.view.fileMenu.entryconfig(9, command=self.quit)

    def quit(self):
        sys.exit()
        
    def new(self):
        options = {
        'defaultextension':".h5",
        'filetypes':[('HDF5',"*.h5")],
        'initialdir':"../",
        'title':"new file name",
        }
        self.db_handle = asksaveasfile(**options)


def main():
    root = Tk()
    root.withdraw()
    app = controller(root)
    root.mainloop()

if __name__ == "__main__":
    main()

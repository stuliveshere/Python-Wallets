from Tkinter import *
from ttk import *
import os

class Tree(Frame):
    '''directory tree browser'''
    def __init__(self, master, path):
        Frame.__init__(self, master)
        self.tree = Treeview(self)
        ysb = Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Select New Database', anchor='center')

        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath)
        self.tree.pack(fill='both', expand=Y, padx=5, pady=5)
        self.pack(fill='both', expand=Y, padx=5, pady=5)

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)

class NewFile(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # Create widgets
        self.v = StringVar()
        self.e = Entry(self, textvariable=self.v)
        self.e.pack(side=LEFT, expand=Y, fill=X)
        self.buttonB = Button(self, text="create")
        self.buttonB.pack(side=RIGHT,)
        self.pack(fill=X, expand=N, padx=5, pady=5)
        
class Wiz1(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(fill=X, expand=N, padx=5, pady=5)
        NewFile(self)
        tree = Tree(self, path='../')
        ButtonFrame = Frame(self)
        ButtonFrame.pack(side=BOTTOM, fill=X)         
        self.next = Button(ButtonFrame, text="Next >",)
        self.next.pack(side=RIGHT, padx=5, pady=5)        
        self.back = Button(ButtonFrame, text="< Back",state=DISABLED)
        self.back.pack(side=RIGHT, padx=5, pady=5)
        self.cancel = Button(ButtonFrame, text="Cancel",command=lambda: self.destroy()).pack(side=LEFT, padx=5, pady=5)
        
    
class Wiz2(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(fill=X, expand=N, padx=5, pady=5)
        ButtonFrame = Frame(self)
        ButtonFrame.pack(side=BOTTOM, fill=X)         
        self.next = Button(ButtonFrame, text="Next >",)
        self.next.pack(side=RIGHT, padx=5, pady=5)        
        self.back = Button(ButtonFrame, text="< Back")
        self.back.pack(side=RIGHT, padx=5, pady=5)
        self.cancel = Button(ButtonFrame, text="Cancel",command=lambda: self.destroy()).pack(side=LEFT, padx=5, pady=5)

class Wiz3(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(fill=X, expand=N, padx=5, pady=5)
        ButtonFrame = Frame(self)
        ButtonFrame.pack(side=BOTTOM, fill=X)         
        self.finish = Button(ButtonFrame, text="Finish",)
        self.finish.pack(side=RIGHT, padx=5, pady=5)        
        self.back = Button(ButtonFrame, text="< Back")
        self.back.pack(side=RIGHT, padx=5, pady=5)
        self.cancel = Button(ButtonFrame, text="Cancel",command=lambda: self.destroy()).pack(side=LEFT, padx=5, pady=5)

        
class WizardView(Toplevel):
    '''top level view for new database wizard'''
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title('New Database Wizard')
        self.geometry("400x600")
        self.frame = Frame(self)
        self.frame.pack(side=TOP, fill=BOTH, expand=Y)
        self.notebook = Notebook(self.frame)
        self.notebook.enable_traversal()
        self.notebook.pack(fill='both', expand=Y, padx=5, pady=5)

        #three wizard pages:
        #select statements for import (multiple files)
        #select wallet definitions (multiple files)
        #select database file
        self.p1 = Wiz1(self.frame)
        self.notebook.add(self.p1)
        self.p2 = Wiz2(self.frame)
        self.notebook.add(self.p2)
        self.p3 = Wiz3(self.frame)
        self.notebook.add(self.p3)
        #self.p2 = notebook.add(W2(notebook))
        #self.p3 = notebook.add(W3(notebook))


        


class GuiView(Toplevel):

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
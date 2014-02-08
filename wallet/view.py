from Tkinter import *
from ttk import *
import os
import tables as tb

class Wizard(object,Notebook):
    ''' from https://code.google.com/p/python-ttk/wiki/ttkWizard'''
    def __init__(self, master=None, **kw):
        npages = kw.pop('npages', 3)
        kw['style'] = 'Wizard.TNotebook'
        Style(master).layout('Wizard.TNotebook.Tab', '')
        Notebook.__init__(self, master, **kw)
        self.master = master
        self._children = {}

        for page in range(npages):
            self.add_empty_page()

        self.current = 0
        self._wizard_buttons()

    def _wizard_buttons(self):
        """Place wizard buttons in the pages."""
        for indx, child in self._children.iteritems():
            btnframe = Frame(child)
            btnframe.pack(side='bottom', fill='x', padx=6, pady=12)

            nextbtn = Button(btnframe, text="Next", command=self.next_page)
            nextbtn.pack(side='right', anchor='e', padx=6)
            if indx != 0:
                prevbtn = Button(btnframe, text="Previous",
                    command=self.prev_page)
                prevbtn.pack(side='right', anchor='e', padx=6)

                if indx == len(self._children) - 1:
                    nextbtn.configure(text="Finish", command=self.close)

    def next_page(self):
        self.current += 1

    def prev_page(self):
        self.current -= 1

    def close(self):
        self.master.destroy()

    def add_empty_page(self):
        child = Frame(self)
        self._children[len(self._children)] = child
        self.add(child)

    def add_page_body(self, body):
        body.pack(side='top', fill='both', padx=6, pady=12)

    def page_container(self, page_num):
        if page_num in self._children:
            return self._children[page_num]
        else:
            raise KeyError("Invalid page: %s" % page_num)

    def _get_current(self):
        return self._current
    
    def _set_current(self, curr):
        if curr not in self._children:
            raise KeyError("Invalid page: %s" % curr)

        self._current = curr
        self.select(self._children[self._current])

    current = property(_get_current, _set_current)

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
        self.buttonB = Button(self, text="create",)
        self.buttonB.pack(side=RIGHT,)
        self.pack(fill=X, expand=N, padx=5, pady=5)
    
        
       
class WizardView(Toplevel):
    '''top level view for new database wizard'''
    def __init__(self, parent, callback):
        self.callback = callback
        Toplevel.__init__(self, parent)
        self.title('New Database Wizard')
        self.geometry("400x600")
        wizard = Wizard(master=self, npages=2)
        self.pagelist = []
        self.pagelist.append(Label(wizard.page_container(0), text='Create new database file'))
        self.pagelist[0].pack(side=TOP)
        self.pagelist.append(NewFile(wizard.page_container(0)))
        self.pagelist.append(Tree(wizard.page_container(0), '../'))
        for page in self.pagelist: wizard.add_page_body(page)
        wizard.pack(fill='both', expand=True)
        
    def exit(self):
        print 'stuff'
        self.callback(self.pagelist[1].v.get())


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
        self.toolMenu.add_command(label="Import statements...")
        self.helpMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="About")


class View_Config():
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.view = parent.add(self.frame, text='Configure')
from Tkinter import *
from ttk import *
import tkFont
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as Tkcanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as Tktoolbar
import numpy as np
import pandas as pd
import matplotlib.pyplot as pylab
import datetime as dt 

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
        self.buttonlist = []
        for indx, child in self._children.iteritems():
            btnframe = Frame(child)
            btnframe.pack(side='bottom', fill='x', padx=6, pady=12)
            nextbtn = Button(btnframe, text="Next", command=self.next_page, state=DISABLED)
            nextbtn.pack(side='right', anchor='e', padx=6)
            self.buttonlist.append(nextbtn)
            if indx != 0:
                prevbtn = Button(btnframe, text="Previous",
                    command=self.prev_page)
                prevbtn.pack(side='right', anchor='e', padx=6)

                if indx == len(self._children) - 1:
                    nextbtn.configure(text="Finish")


def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sortself.rows
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))

    def next_page(self):
        self.current += 1

    def prev_page(self):
        self.current -= 1

    def close(self):
        self.destroy()

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
        self.log = View_Log(notebook)
        self.summary = View_Summary(notebook)
        self.walletsummary = View_Wallet_Summary(notebook)
        self.wallets = View_Wallets(notebook)
        

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
        self.toolMenu.add_command(label="Parse Wallets...")
        self.toolMenu.add_command(label="Remove Duplicates...")
        self.toolMenu.add_command(label="Edit accounts...")
        self.toolMenu.add_command(label="Edit wallets...")
        self.helpMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="About")
    

class View_Wallets():
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.view = parent.add(self.frame, text='Wallets')
        self.notebook = Notebook(self.frame)
        self.notebook.enable_traversal()  
        self.notebook.pack(fill='both', expand=Y, padx=5, pady=5)

    def draw(self, data):
        wallets = data.wallet.unique()
        pages = {}
        for wallet in wallets:
            pages[wallet] = View_Pages(wallet, self.notebook)
            
class View_Wallet_Summary():
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.view = parent.add(self.frame, text='Wallet Summary')
        self.notebook = Notebook(self.frame)
        self.notebook.enable_traversal()  
        self.notebook.pack(fill='both', expand=Y, padx=5, pady=5) 
        
    def draw(self):
        pass          

            
class View_Pages():
    def __init__(self, wallet, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.view = parent.add(self.frame, text=wallet)

class View_Summary():
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.view = parent.add(self.frame, text='Account Summary')
        self.fig = pylab.figure(figsize=(10,8), dpi=100)
        self.axes = {'veridian':self.fig.add_subplot(411),
                     'mastercard':self.fig.add_subplot(412),
                     'visa':self.fig.add_subplot(413),
                     }
        self.total = self.fig.add_subplot(414)
        self.canvas = Tkcanvas(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


    def draw(self, dataset):
        for key in self.axes.keys():
            self.axes[key].cla()
            df = dataset[dataset.account == key]
            df = self.parse(df)
            df.plot(ax=self.axes[key], title=key)

        self.total.cla()
        df = self.parse(dataset)
        df.plot(ax=self.total, title='total')
        self.fig.tight_layout()
        self.canvas.show()
        
    def parse(self, series):
        today = dt.date.today()
        rng = pd.date_range(start='2013-07-01', end=today, freq='D')
        df = series.set_index(keys='date')
        df = df.amount
        df = df.sort_index()
        df = pd.DataFrame(df)
        df['time'] = df.index
        mask = (df.time-df.time.shift()) == np.timedelta64(0,'s')
        for index, entry in enumerate(mask):
            if entry:
                df.time.iloc[index] += pd.offsets.Second(index)
        df = df.set_index(keys='time')
        df = df.amount
        df.columns = ['amount']
        df = df.cumsum().astype(np.float)
        df = df.reindex(index=rng, method='pad', fill_value=None)
        df -= df.dropna().iloc[0]
        return df


       
class View_Log():
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.view = parent.add(self.frame, text='Log')
        self.text_box = Text(self.frame, wrap='word')
        self.text_box.pack(fill='both', expand=Y, padx=5, pady=5)


class View_table(object):
    """use a ttk.TreeView as a multicolumn ListBox"""   
    def __init__(self, table):
        self.view = Toplevel()
        self.table = table

        container = Frame(self.view)
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = Treeview(self.view, columns=self.table.columns, show='headings')
        for col in self.table.columns: self.tree.heading(col, text=col)
        vsb = Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        #self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        #vsb.grid(column=1, row=0, sticky='ns', in_=container)
        #hsb.grid(column=0, row=1, sticky='ew', in_=container)
        self.tree.pack(fill='both', expand=True)
        #container.grid_columnconfigure(0, weight=1)
        #container.grid_rowconfigure(0, weight=1)
         #self._build_tree()

    #def _build_tree(self):
        #for col in self.header:
            #self.tree.heading(col, text=col),
                #command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            #self.tree.column(col,
                #width=20)
        #for item in self.rows:
            #self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            #for ix, val in enumerate(item):
                #col_w = 20
                #if self.tree.column(self.rows[ix],width=None)<col_w:
                    #self.tree.column(self.rows[ix], width=col_w)
                    

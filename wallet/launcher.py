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
        self.view.toolMenu.entryconfig(2, command=self.editAccounts)
        self.view.toolMenu.entryconfig(3, command=self.editWallets)
        #model
        self.h5db = None
        self.Data = Model(columns=['data', 'amount', 'desc', 'account', 'wallet'])
        self.Accounts = Model(columns=['account', 'desc'])
        self.Wallets = Model(columns=['wallet', 'keys'])
        #add callbacks
        self.Accounts.model.addCallback(self.logger)
        self.Wallets.model.addCallback(self.logger)
        self.Accounts.model.addCallback(self.unsaved)
        self.Wallets.model.addCallback(self.unsaved)
        self.Data.model.addCallback(self.unsaved)
    
    def logger(self, event):
        print event
        #print self.Accounts.model.data
        
    def unsaved(self):
        #put asterix in title to show not saved
        self.view.title('Python-Wallets (**unsaved)')

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
        self.h5db = asksaveasfilename(**options)
        self.import_accounts()
        self.import_wallets()

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
        self.h5db = askopenfilename(**options)
        store = pd.HDFStore(self.h5db)
        self.Accounts.set(store['accounts']) 
        self.Wallets.set(store['wallets'])
        self.Data.set(store['data'])
        

    def process_statement(self):
        print 'do iiiiit'   
                   
    def model_open(self):
        pass

    def import_statements(self):
        options = {
        'defaultextension': '.csv',
        'filetypes': [('csv', '.csv')],
        'initialdir': '../data/statements/',
        'initialfile': None,
        'multiple': 1,
        'parent': self.parent,
        'title': 'select statement file'
        }
        filelist=askopenfilenames(**options)
        accountlist = list(self.Accounts.model.data['account'].values)
        #for each file
        for _file in filelist:
            #parse filename to find out the account
            accountname =  accountlist[[i for i, x in enumerate(accountlist) if x in _file][0]]
            #read in csv to dataframe
            _data = pd.read_csv(_file, header=None, names=['data', 'amount', 'desc', 'null'])
            _data['account'] = accountname
            _data = _data.drop('null', 1)
            self.Data.set(_data)
            
            
            
        #append account to new column
        #append dataframe to Data
        #run duplicate removal tool
        #run wallet parser

        
            

    def import_accounts(self):
        options = {
        'defaultextension': '.csv',
        'filetypes': [('csv', '.csv')],
        'initialdir': '../',
        'initialfile': None,
        'multiple': 0,
        'parent': self.parent,
        'title': 'select accounts definitions'
        }
        filename=askopenfilename(**options)
        account_data = pd.read_csv(filename, header=None)
        account_data.columns = ['account', 'desc']
        self.Accounts.set(account_data)
        
    def import_wallets(self):
        options = {
        'defaultextension': '.csv',
        'filetypes': [('csv', '.csv')],
        'initialdir': '../',
        'initialfile': None,
        'multiple': 1,
        'parent': self.parent,
        'title': 'import wallets'
        }
        filelist=askopenfilenames(**options)
        walletlist = [a.split('/')[-1].split('.')[0] for a in filelist]
        keys = [open(a, 'r').read().split('\n') for a in filelist]
        df = pd.DataFrame(data = zip(walletlist, keys), columns=['wallet', 'keys'])
        self.Wallets.set(df)


    def editAccounts(self):
        View_table(self.Accounts)
    
    def editWallets(self):
        pass

    def save(self):
        store = pd.HDFStore(self.h5db)
        store['accounts'] = self.Accounts.model.data
        store['wallets'] = self.Wallets.model.data
        store['data'] = self.Data.model.data
        self.view.title('Python-Wallets')

def main():
    root = Tk()
    root.withdraw()
    app = Gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()

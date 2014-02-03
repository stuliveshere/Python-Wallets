import Tkinter as tk
import ttk

class View(tk.Toplevel):

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        self.title('Python-Wallets')
        self.geometry("1280x768")

        self.menuBar = tk.Menu(self)
        self["menu"] = self.menuBar
        self.fileMenu = tk.Menu(self.menuBar)
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
        
        self.toolMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="Tools", menu=self.toolMenu)
        self.toolMenu.add_command(label="template")

        self.helpMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="About")
       
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=1, padx=5, pady=5)
        notebook.enable_traversal()

#        self.params = View_Param(notebook)
#        self.volumes = View_Volumes(notebook)
#        self.nodes = View_Nodes(notebook)


class controller(tk.Toplevel):
    def __init__(self, root):
        self.parent = root
        self.view = View(root)


def main():
    root = tk.Tk()
    root.withdraw()
    app = controller(root)
    root.mainloop()

if __name__ == "__main__":
    main()

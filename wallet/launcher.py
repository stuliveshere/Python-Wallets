import Tkinter as tk


class gui(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        pass


def main():
    app = gui(None)
    app.title('Python-Wallets')
    app.mainloop()

if __name__ == "__main__":
    main()

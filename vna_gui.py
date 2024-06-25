import pyvisa as visa
from tkinter import *
from tkinter import ttk

class DataViewer:

    def __init__(self, root):

        root.title("Triaxial Cell Data Viewer")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
       
        #self.feet = StringVar()
        #feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        #feet_entry.grid(column=2, row=1, sticky=(W, E))
        #self.meters = StringVar()

        self.connected = BooleanVar()

        ttk.Label(mainframe, textvariable=self.connected).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Pull Data", command=self.pullData).grid(column=3, row=3, sticky=W)

        #ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        #ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        #ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        #feet_entry.focus()
        #root.bind("<Return>", self.exit())
        
    def pullData(self, *args):
        
        rm = visa.ResourceManager()
        
        try:
            vna = rm.open_resource('blah::blah::blah::blah')
            
        except:
            print('resource does not exist')

        return True

root = Tk()
DataViewer(root)
root.mainloop()
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askdirectory
import numpy as np
import pyvisa as visa
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd

master = tk.Tk()
master.title("Data pull from VNA")
defaultName = None
saveLocation = None

def saveButton():
    if e1.index("end") == 0:
            print("Please choose a save directory")
    elif e2.index("end") == 0:
        print("Please add file name!")
    else:
        try:
            df.to_csv(defaultName + '/' + e2.get() + '.csv')
            print(defaultName + '/' + e2.get() + '.csv' + ' saved')
        except:
            print('issue saving CSV file')
    return
       
def openDialog():
    global defaultName
    defaultName= askdirectory()
    e1.delete(0, END)
    e1.insert(0, defaultName)
    print(defaultName)
    return

def pullData():
    # connects to the instrument and does some error checking
    rm = visa.ResourceManager()
    
    # simple error catching in case the resource is not available
    try:
        vna = rm.open_resource('TCPIP0::10.1.2.82::INSTR')
    except:
        print('resource does not exist')

    # if you feel like error checking
    res = vna.query('*IDN?')
    # pulls the trace data directly from active trace
    data_raw = vna.query('CALC:DATA? FDAT')
    data = np.round(np.array([float(i) for i in data_raw.split(',')]), 2)
    
    # pulls the frequency data and converts to MHz
    freq_raw = vna.query('CALC:DATA:STIM?')
    freq = np.round(np.array([float(i) for i in freq_raw.split(',')])/1E6, 6)

    # now plot data in a new window add block=False to plt.show()!
    plt.plot(freq,data)
    plt.ylim([-140,0])
    plt.semilogx()
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Data from vna at ' + dt.datetime.now().strftime('%H:%M:%S'))
    plt.show(block=False)

    global df
    # create a dataframe so we can easily save it later and transfer it between functions
    df = pd.DataFrame(np.transpose(data), index=np.transpose(freq), columns=['Magnitude (dB)'])
    df.index.name = 'Frequency (MHz)'

    return df

#Setup Frames
f1 = tk.Frame(master, width=400, height=180)
f2 = tk.Frame(f1, width=300, height=250)
f3 = tk.Frame(f1, width=200, height=50)
f4 = tk.Frame(f3, width=300, height=100)
f5 = tk.Frame(f1, width=200, height=10)
separator1 = Frame(f1, height=2, bd=1, relief=SUNKEN)
separator2 = Frame(f1, height=2, bd=1, relief=SUNKEN)

#pack the frames
f1.pack(expand=1)
f1.pack_propagate(0) #fix size
f2.pack()
separator1.pack(fill=X, padx=5, pady=5)
f3.pack(fill=X)
f4.pack(side=TOP, expand=FALSE)
separator2.pack(fill=X, padx=5, pady=5)
f5.pack(side=TOP, fill=X)

#Text entry
e1 = Entry(f2, width = 50)
e2 = Entry(f2, width = 50)
e2.focus_set() #put cursor in first box
e1.grid(row=2, column=1, padx=5, pady=3,)
e2.grid(row=4, column=1, padx=5, pady=3)

#Labels
label1 = Label(f2,text="Select Save Location..")
label1.grid(row=1,column=1, sticky = W)
label2 = Label(f2,text="Enter File Name..")
label2.grid(row=3,column=1, sticky = W)

#Buttons
button1 = Button(f2, text = "Open Folder", padx=5, pady=1, width=9, command=openDialog).grid(row=2, column = 2)
button2 = Button(f2, text = "Save File", padx=5, pady=1, width=9, command=saveButton).grid(row=4, column = 2)
button3 = Button(f5, text = "Quit", padx=5, pady=1, width=9, command=quit).pack(side=TOP)
button4 = tk.Button(f4,text="Pull", padx=10, pady=1, command=pullData).grid(row=1, column=2)

#Main
mainloop()
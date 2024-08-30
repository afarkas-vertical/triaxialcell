from csv import reader
from tkinter import filedialog
# from tkinter import tkFileDialog
from tkinter import *
import numpy as np
import csv

########################################################################################
# Function:  get_File
# Purpose: when called, the function opens a dialog box for the user to select files
# Returns: file name and extention chosen by user
########################################################################################

def get_Files():
	files = filedialog.askopenfilenames(parent=root,title='Choose raw SE .csv file')
	return files

########################################################################################b 	
# Function:  converter 
# Purpose: converts output VNA data to Transfer Impedance calculated format
# Returns: nothing
########################################################################################
def converter(files):
	for f in files:
		with open(f, newline='') as csvfile:
			wb = csv.reader(csvfile.readlines()[1:])
			new_csv_file = open(f[:-4] + str('_conv.csv'), 'w', newline='')
			wr = csv.writer(new_csv_file, quoting=csv.QUOTE_ALL)
			# write the header row
			newrow = [0,0,0,0]
			newrow[0] = 'Frequency (MHz)'
			newrow[1] = 'SA (dB)'
			newrow[2] = 'S150 (dB)'
			newrow[3] = 'Snorm (dB)'
			#newrow[5] = 'Snorm (dB)'
			wr.writerow(newrow)
			
            # some constants that need defining
			er1=1.36
			er2=1.1
			Zo=50
			Zs=150
			er2t = er2
			er2n = er1/1.21
			offset150 = 10*np.log10((2*Zs)/Zo)
			normOffset = 20*np.log10(np.sqrt(2)*((np.abs(1-np.sqrt(er2n/er1)))/(np.abs(1-(er2t/er1)))))

			for row in wb:
				# initialize
				newrow = [0,0,0,0]
				# populate
				newrow[0] = row[0]
				newrow[1] = float(row[1])
				newrow[2] = newrow[1] - offset150
				newrow[3] = newrow[1] - offset150 - normOffset
				wr.writerow(newrow)
			new_csv_file.close()

if __name__ == "__main__":
	root = Tk()
	root.wm_title("multi csv to csv")
	root.configure(background='lightgray')
	files = get_Files()
	converter(files) 
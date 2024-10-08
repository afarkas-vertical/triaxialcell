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
	files = filedialog.askopenfilenames(parent=root,title='Choose raw TI .csv file')
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
			newrow[1] = 'S21 (dB)'
			newrow[2] = 'S21 (W)'
			newrow[3] = 'ZT (mOhm/m)'
			wr.writerow(newrow)
			# now go through each row
			for row in wb:
				# remap to float for precision access
				#row = map(np.float32, row)   
				# initialize
				newrow = [0,0,0,0]
				# populate
				newrow[0] = row[0]
				newrow[1] = row[1]
				newrow[2] = 10**(float(row[1])/20)
				newrow[3] = (50*1e3)/(0.3)*10**(float(row[1])/20)	# should this be div 20? or div 10?
				wr.writerow(newrow)
			new_csv_file.close()

if __name__ == "__main__":
	root = Tk()
	root.wm_title("multi csv to csv")
	root.configure(background='lightgray')
	files = get_Files()
	converter(files) 
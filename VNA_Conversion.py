from csv import reader
from tkinter import filedialog
# from tkinter import tkFileDialog
from tkinter import *
import numpy as np
import csv


########################################################################################
# Program Name:  VNAcsv_to_standard_csvMHz.py
# Author: Stephen Board
# Purpose: convert user-selected .csv files from format from VNA to typical format
# Notes: you must select a .csv file
########################################################################################


########################################################################################
# Function:  get_File
# Purpose: when called, the function opens a dialog box for the user to select a file
# Returns: file name and extention chosen by user
########################################################################################

def get_Files():
	files = filedialog.askopenfilenames(parent=root,title='Choose raw csvs file')
	return files

########################################################################################b 	
# Function:  converter 
# Purpose: converts output VNA data to more easily parsable data
# Returns: nothing
########################################################################################
def converter(files):
	for f in files:
		with open(f, newline='') as csvfile:
			wb = csv.reader(csvfile.readlines()[2:])
			your_csv_file = open(f[:-4]+'.csv', 'w', newline='') 
			wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
			for row in wb:
				newrow = row[0].split(';')
				newnewrow = [0,0,0,0,0]
				try: 
					newnewrow[0] = float(newrow[0])*1e-6
					newnewrow[1] = float(newrow[1])
					newnewrow[2] = 10**(float(newrow[1])/20)
					newnewrow[3] = (50*1e3)/(0.3)*10**(float(newrow[1])/20)
					newnewrow[4] = float(newrow[2])
				except:
					newnewrow[0] = 'freq[MHz]'
					newnewrow[1] = 'dB Mag'
					newnewrow[2] = 'S21'
					newnewrow[3] = 'ZT(mOhm/m)'
					newnewrow[4] = 'db Phase'
				wr.writerow(newnewrow)
			your_csv_file.close()

if __name__ == "__main__":
	root = Tk()
	root.wm_title("multi csv to csv")
	root.configure(background='lightgray')
	files = get_Files()
	converter(files) 
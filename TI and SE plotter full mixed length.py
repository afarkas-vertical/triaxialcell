import matplotlib.pyplot as pt 
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker
import numpy as np
from csv import reader
from tkinter import filedialog
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from PIL import Image

pt.rcParams.update({'font.size':24})
pt.rcParams["font.family"] = "Times New Roman"
#im = Image.open('C:/Users/sboard/PythonSDB/Reference/images/logo.jpg')
TI_filenames = []
SA_filenames = []
Legend = []
Datum = []
TI_cut = np.linspace(83,100)   # TI Cutoff
SA_cut = np.linspace(100,350)  # SA Cutoff
root = Tk()
root.wm_title("Transfer Coupling Plotter")
root.configure(background='lightgray')
c = ['olivedrab','sienna','m','gold','c','k']

s = [(0,(1,10)),(0,(5,10)), (0,(3,5,1,4,1,4)),(0,(5,5)), 'solid','dashed']
ls = ['-','--',':']
cs=[['olivedrab','dashed'],['m','dotted'],['sienna','solid'],['gold','dashed'],['k','dotted'],['green','solid']]

def get_File():
	TF_file = filedialog.askopenfiles(parent=root,mode='rb',title='Choose a Transfer Impedance file')
	for f in TF_file:
		TF_name = f.name.split("/")
		if TF_name[len(TF_name)-1][-4:] == ".csv":
			error_clear = 1
		Legend.append((TF_name[len(TF_name)-1][:-4]))#+'\n'+(SA_name[len(SA_name)-1][:-4]))
			# TIlegend.append(TF_name[len(TF_name)-1][:-4])
	SA_file = filedialog.askopenfiles(parent=root,mode='rb',title='Choose a Screening Attenuation file')
	for f in SA_file:
		SA_name = f.name.split("/")
		if SA_name[len(SA_name)-1][-4:] == ".csv":
			error_clear = 1
			# SAlegend.append(SA_name2[len(SA_name)-1][:-4])
		else: error_clear = 0
		
	return TF_file,SA_file,error_clear


def draw_UI():
	S1 = Button(root, text="Add Trace", command=main)
	S1.pack()
	S2 = Button(root, text="save", command = save)
	S2.pack()

def get_TI_Data(file):
	xarr = []
	yarr = []
	i = 0
	found = 0
	while not found:
		first = list(reader(open(file.name,errors="ignore")))[i][0]
		try:
			test = float(first)
			found = 1
		except:
			i += 1
	data = list(reader(open(file.name,errors="ignore")))[i:]
	for d in data:
		try:
			if float(d[0]) < 100:
				xarr.append(float(d[0]))
				yarr.append(np.abs((50*1e3)/(0.3)*10**(float(d[1])/20))) # vulnerability: we need the milli-ohm per meter column only
		except:

			print(d[0])
	
	return(xarr,yarr)

def get_SA_Data(file,er1=1.36,er2=1.1,Zo=50,Zs=150,as150=True,norm=True):
	# we will fill these and then return them later
	freq = []
	smeas = []
	s150 = []
	sNorm = []
	i = 0 # this is an iterator so we can skip the unncessary header lines
	found = 0 # boolean to signal whether we ahve started finding data
	while not found: # we iterate through each line in the csv until we start finding numbers
		first = list(reader(open(file.name)))[i][0]
		try:
			float(first) # this is called a float-cast. if it works, we're good
			
			found = 1
		except:  # if it breaks, we need to go to the next line and try again
			i += 1

	# now we know where the data begins so we should grab everything else
	data = list(reader(open(file.name)))[i:]

	offset150 = 10*np.log10((2*Zs)/Zo)


	er2t = er2
	er2n = er1/1.21 # this is an assumed 10% velocity difference for as150
	normOffset = 20*np.log10(np.sqrt(2)*((np.abs(1-np.sqrt(er2n/er1)))/(np.abs(1-(er2t/er1)))))
	# print("normOffset = " + str(normOffset))
	# now we go through the rows and we know the first row (0) is the frequency, and based on experience
	# and checking the files (THIS CAN BE A MISTAKE WHICH MUST BE CHANGED SOMETIMES), the 6th column (5)
	# holds the 'normalized' as(150) Screening attentuation data
	for d in data:
		#s_measured = 20*np.log10(np.abs(np.float64(d[1]))) 
		s_measured = np.float64(d[1])
		# s_measured = float(d[5]) 
		smeas.append(s_measured)
		s150.append(s_measured-offset150)
		sNorm.append(s_measured-offset150-normOffset)
		freq.append(float(d[0]))

	# return the data
	return(freq,smeas,s150,sNorm,offset150)

def getEnvelope(xarr,yarr,flong):
	xenv,yenv = [],[]
	prevx = 0 
	curx = 0
	prevy = -150
	cury = -150
	
	for i in range(len(xarr)):
		curx = xarr[i]
		cury = yarr[i]
		if curx > flong:
			if curx <8000:
				if cury > prevy:
					prevx = xarr[i-1]
					prevy = cury
					while yarr[i+1] > yarr[i]:
						i += 1
					prevy = yarr[i]
					xenv.append(prevx)
					yenv.append(prevy+1)
				else:
					xenv.append(curx)
					yenv.append(prevy+1)
	return(xenv,yenv)

def save():

	pt.savefig('filename.png', dpi=300)
	print('here')

def main():

	TI_File, SA_File, clear = get_File()

	for f in TI_File:
		TI_filenames.append(f)
	for f in SA_File:
		SA_filenames.append(f)

	TI_Datum = []
	SA_Datum = []
	envelopes = []

	for f in TI_filenames:
		TI_Datum.append(get_TI_Data(f))
	for f in SA_filenames:
		SA_Datum.append(get_SA_Data(f))
	for d in SA_Datum:
		envelopes.append(getEnvelope(d[0],d[3],max(SA_cut)))

	#TI_Datum_Array = np.array(TI_Datum)
	TI_Datum_Array = (TI_Datum)
	#SA_Datum_Array = np.array(SA_Datum)
	SA_Datum_Array = (SA_Datum)
	EnvelopesArray = np.array(envelopes)


	TC_Plot_Fig = pt.figure(1,figsize=(17,10))
	TI_Plot = pt.axes()

	for i in range(len(TI_filenames)):
		TI_Plot.plot(TI_Datum_Array[i][0],TI_Datum_Array[i][1],linewidth=3,color=c[i],linestyle=ls[i%len(ls)],label=Legend[i])

	divider = make_axes_locatable(TI_Plot)
	SA_Plot = divider.append_axes("right", size=7, pad=0)

	for i in range(len(TI_filenames)):
		SA_Plot.plot([100,EnvelopesArray[i][0][0]],[EnvelopesArray[i][1][0],EnvelopesArray[i][1][0]],color=c[i],linewidth=2,linestyle=ls[i%len(ls)])
		SA_Plot.plot(EnvelopesArray[i][0],(EnvelopesArray[i][1]),color=c[i],linewidth=5,linestyle=ls[i%len(ls)])
		SA_Plot.plot(SA_Datum_Array[i][0],(SA_Datum_Array[i][1]),color=c[i+1],linewidth=5,linestyle=ls[i%len(ls)])

	TI_Plot.set_xlim([TI_Datum_Array[0][0][0],100])
	TI_Plot.set_xscale('log')
	TI_Plot.set_yscale('log')
	TI_Plot.spines['right'].set_visible(False)
	TI_Plot.xaxis.set_ticks_position('bottom')
	TI_Plot.grid(True)
	TI_Plot.set_title("Transfer Impedance")
	TI_Plot.set_ylabel(r"$Z_T$"+" (mΩ/m)")
	TI_Plot.set_xlabel("                                                                          Frequency (MHz)")
	TI_Plot.xaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
	TI_Plot.yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
	TI_Plot.fill_between(TI_cut,0.01,120000,facecolor = 'grey', alpha = 1)
	TI_Plot.set_ylim([0.1667,116000])		
	TI_Plot.legend(loc = 'upper center', bbox_to_anchor=(0.3, -0.05),fancybox=True, shadow=True, prop={'size':16}, ncol = 2, handlelength=3)
	TI_box = TI_Plot.get_position()
	TI_Plot.set_position([TI_box.x0, TI_box.y0 + TI_box.height * 0.1,TI_box.width, TI_box.height * 0.9])
	SA_Plot.set_xscale('linear')
	SA_Plot.set_yscale('linear')
	SA_Plot.set_xlim([100,8000])
	SA_Plot.set_ylim([-123,0-SA_Datum[0][4]])
	SA_Plot.spines['left'].set_visible(False)
	SA_Plot.set_ylabel(r'$A_N$' +'  (dB)')
	SA_Plot.yaxis.set_ticks_position('right')
	SA_Plot.yaxis.set_label_position('right')
	SA_Plot.set_title('Screening Attenuation')
	SA_Plot.grid(True,which="both")
	SA_box = SA_Plot.get_position()
	SA_Plot.set_position([SA_box.x0, SA_box.y0 + SA_box.height * 0.1,SA_box.width, SA_box.height * 0.9])
	SA_Plot.yaxis.set_major_locator(MultipleLocator(20))
	SA_Plot.yaxis.set_major_locator(MultipleLocator(10))
	newax = TC_Plot_Fig.add_axes([0.82, (0.0 *(np.ceil(len(TI_filenames)/2)-1)), 0.1, 0.1], anchor='NE', zorder=-1)
	#im.thumbnail((1000,1000), )
	#newax.imshow(im)
	newax.axis('off')
	pt.subplots_adjust(top=0.96,bottom=0.14 + (0.01 *(np.ceil(len(TI_filenames)/2)-1)), right=0.92, left=0.11)
	pt.show()
draw_UI()
main()
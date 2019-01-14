# Used to read Nur's DAQ files, make plots from them
# Author: Aaron Bercellie
# Date:   4/8/2016
# Modified by Nur for the DAQ Uptime Plot

from StatusPlotClasses import *
from glob import glob
from ROOT import *
from array import array
from re import search
from sys import argv
from time import mktime, strptime
import curses 

#Draw parameters 
#SetStyle is from StatusPlotClasses
############################################################################
SetStyle()
############################################################################

ROOT.gROOT.SetBatch(True)
script, days = argv

#Set the directory here...
#sourceDir="logs/special/"
sourceDir="logs/"
lognames="_live_time.txt"
files=glob("{0}/*{1}".format(sourceDir,lognames))
files=sorted(files)#Get them in chronological order

arrday=array('d',[_ for _ in range(1,int(days)+1)])
arrdate=[]
arreff=array('d')
arrdate2=[]

#Get rid of the excess.  Only want the most recent
for _ in range(len(files)-int(days)):
    files.pop(0)

for f in files:
    #Get the date labels
    filename=search("[0-9]+{0}".format(lognames),f)
    if filename:
        strdate="{0}/{1}".format(filename.group(0)[4:6],filename.group(0)[6:8])
        arrdate.append(strdate)#This assumes a very particular format of filename
        strdate2="{0}-{1}".format(filename.group(0)[4:6],filename.group(0)[6:8])
        arrdate2.append(strdate2)#This assumes a very particular format of filename

    minT=0;maxT=0;evtCounter=0;evtOn=0;#Reset counters
    #I'm assuming column 1=time, column 2=daq status, can change
    DAQLog=TimeCSV(f)
    DAQLog.SetDelimiter(" ")
    for tstamp,status in DAQLog.CSVLoop():
        time=mktime(strptime(tstamp,"%Y%m%d%H%M%S"))
        evtCounter+=1
        if int(status+0.1)==1:#Super paranoid about rounding errors
            evtOn+=1
        #Not sure how important it is to know the amount of time that data was taken
        if time<minT or minT==0:
            minT=time
        if time>maxT:
            maxT=time
    arreff.append(100*float(evtOn)/evtCounter)

#Plots
statPlot=StatusPlots.load(len(files),arrday,arreff)

#Make the plot nice and pretty
statPlot.FormatMain(kRed+1)

#Set the title
statPlot.SetMainTitle("MINERvA DAQ Clock Livetime;Date;DAQ Livetime [%]")

#Set the range
statPlot.SetMainRange((),(0,115))#(xrange,yrange)

#Add x labels
statPlot.SetMainBinLabels(arrdate)

#Set Bar labels
statPlot.SetMainBarLabels(arreff)

#Total Percentage 
avgeff=sum(arreff)/len(arreff)
statPlot.SetMainPercentageText("Avg. {0}-{1} = {2:0.1f}%".format(arrdate[0],strdate,avgeff))

#Label saying what plots this is "weekly, monthly"  Not used for livetime
statPlot.SetTimeScaleText("(Weekly)",kBlue,-0.3)

statPlot.draw("B","","plots/AaronTestLiveWeekly.png")

#raw_input("Press any key")


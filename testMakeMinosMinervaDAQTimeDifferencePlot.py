# Used to read MINOS MINERvA DAQ time difference logs and make plots from them
# Author: Nuruzzaman
# Date:   01/21/2017

from StatusPlotClasses import *
from glob import glob
from ROOT import *
from array import array
from re import search
from sys import argv
from time import mktime, strptime,localtime,strftime
import curses 

#############################################################################
#Draw parameters
#############################################################################
#SetStyle is from StatusPlotClasses
############################################################################
SetStyle()
############################################################################
#Draw parameters 
typecolor=[kBlack,kRed+1,kBlue,kPink,kOrange-3,kYellow,kSpring,kTeal-6,kAzure,kViolet,kGreen,kGreen+2,kRed]
typetext=[0.04,0.045,0.055,0.060,0.065]
#############################################################################
#Pad parameters
gStyle.SetPadColor(0) 
gStyle.SetPadBorderMode(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetFrameBorderSize(0)
gStyle.SetPadBorderSize(0)
gStyle.SetCanvasColor(0)
gStyle.SetStatColor(0)
gStyle.SetPadTopMargin(0.09)
gStyle.SetPadBottomMargin(0.12)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadLeftMargin(0.12)

# histo parameters
gStyle.SetTitleYOffset(0.88)
gStyle.SetTitleXOffset(0.73)
gStyle.SetLabelSize(0.16,"x")
gStyle.SetLabelSize(0.06,"y")
gStyle.SetTitleSize(0.07,"x")
gStyle.SetTitleSize(0.07,"y")
gStyle.SetTitleX(0.55)
gStyle.SetTitleY(0.99)
gStyle.SetTitleW(0.90)
gStyle.SetTitleBorderSize(0)
gStyle.SetTitleFillColor(0)
gStyle.SetTitleFontSize(typetext[2])

gStyle.SetTextFont(42)
gStyle.SetStatFont(42)
gStyle.SetTitleFont(42)
gStyle.SetTitleFont(42,"y")
gStyle.SetTitleFont(42,"x")
gStyle.SetLabelFont(42)
gStyle.SetLabelFont(42,"y")
gStyle.SetLabelFont(42,"x")
#Live only
gStyle.SetNdivisions(500,"X");
gStyle.SetPadTickX(1);
############################################################################

ROOT.gROOT.SetBatch(True)#Kill output
opts=argv
if len(argv)==1:
    date=-1
else:
    date=opts[1]

#Set the directory here...
sourceDir="logs/"
lognames="_minerva_minos_daq_time_difference.txt"
files=glob("{0}/*{1}".format(sourceDir,lognames))
files=sorted(files)#Get them in chronological order

arrhour=array('d')
arreff=array('d')
arrtime=[]

#Find current time, subtract 24 hours, then fill plot for the last 24 hours
#Every 10 minutes

localT=localtime()
localComp=mktime(localT)
startDayOffset=localT.tm_hour*3600+localT.tm_min*60+localT.tm_sec
for f in files:
    #Get filenames and times
    if date<0:
        filename=search("([0-9]+){0}".format(lognames),f)
        StatusWindow=24*3600#Number of hours times seconds
    else:
        filename=search("([0-9]+{0}){1}".format(date,lognames),f)
        StatusWindow=-1
    if filename:
        logfileTime=mktime(strptime(filename.group(1),"%Y%m%d"))
    if StatusWindow>0 and logfileTime<(localComp-StatusWindow-startDayOffset): #if the logfile date less than the start of the day-status window 
        continue

    MINOSLog=TimeCSV(f)
    MINOSLog.SetDelimiter(" ")
    MINOSLog.SetColumnSelect([0,3])

    avgWindow=10*60#Window to average is 10 minutes
    first=True
    sumdiff=0;evtCounter=0
    for t,diff in MINOSLog.CSVLoop():
        tstamp=time.strptime(str(t),"%Y%m%d%H%M%S")
        if mktime(tstamp)<localComp-StatusWindow:
            continue
        #When we finally hit the last 24 hours
        if first:
            currentTime=mktime(tstamp)
            arrhour.append(mktime(tstamp))
            arrtime.append(time.strftime("%H:%M",tstamp)) 
            first=False
        #Average over the last avgWindow, reset counters
        if currentTime<mktime(tstamp)-avgWindow:
            arrhour.append(mktime(tstamp))
            arrtime.append(time.strftime("%H:%M",tstamp)) 
            arreff.append((sumdiff/evtCounter)*1e-9)
            #Mew iteration
            sumdiff=0;evtCounter=1;
            currentTime=mktime(tstamp)
        #Keep ticking if we haven't gone over the last counters
        else:
            evtCounter+=1
        #Add the difference
        sumdiff+=diff
    #Have to repeat one last time
    arreff.append((sumdiff/evtCounter)*1e-9)
#Plots
statPlot=StatusPlots.load(len(arrhour),arrhour,arreff)

#Make the plot nice and pretty
statPlot.FormatMain(kMagenta+1)

#Set the title
statPlot.SetMainTitle("MINOS MINERvA DAQ Clock Time Difference;Time;Time Difference [s]")

#Set the range
#statPlot.SetMainRange((),(-1,1))#(xrange,yrange)

#Add x labels
statPlot.SetMainBinLabels(arrtime,20,arrhour)

localDate=strftime("%m/%d %H:%M",localT)

#Total Percentage 
avgeff=sum(arreff)/len(arreff)
#statPlot.SetMainPercentageText("Avg. over 24 hrs = {0:0.2f} s".format(avgeff))
avgtext=TLatex(0.12,0.94,"#splitline{{Avg. over 24 hrs}}{{     {0:0.2f} s   }}".format(avgeff))
avgtext.SetNDC()
avgtext.SetTextColor(kBlue);
avgtext.SetTextSize(0.04)
statPlot._Texts.append(avgtext)

#axhline(y=-0.09, xmin=15, xmax=25)

#Line that show the current time (only for liveTime)
statPlot.SetMainNowLine(currentTime,localDate)

statPlot.draw("L","","plots/test_minerva_minos_daq_time_difference_plot.png")

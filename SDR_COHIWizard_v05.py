# -*- coding: utf-8 -*-
#self.menubar = QtWidgets.QMenuBar(MainWindow)
"""
Created on Fri Dec 24 10:15:44 2021

@author: scharfetter_admin
"""
from pickle import FALSE, TRUE
import sys
import time
import os
import numpy as np
import math
import re
import datetime as ndatetime
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM
from struct import pack
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QMutex
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QFont, QBrush, QColor
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,  NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from scipy import signal as sig
import scipy
import paramiko
import pandas as pd
import soundfile as sf
from soundfile import SEEK_SET, SEEK_CUR, SEEK_END
import yaml
from COHIWizard_GUI_v4 import Ui_MainWindow as MyWizard
from SDR_wavheadertools import WAVheader_tools


class WizardGUI(QMainWindow):
    #signals
    SigToolbar = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Constants
        self.TEST = True    # Test Mode Flag for testing the App  ##NOT USED
        self.DATA_FILEEXTENSION = ["dat","wav",'raw']
        self.CURTIMEINCREMENT = 5
        self.DATABLOCKSIZE = 1024*32
        self.DELTAF = 5000 #minimum peak distance in Hz  for peak detector
        self.PEAKWIDTH = 5 # minimum peak width in Hz  for peak detector
        self.PROMINENCE = 15 # minimum peak prominence in dB above baseline for peak detector
        self.FILTERKERNEL = 5 # length of the moving median filter kernel in % of the spectral span
        self.NUMSNAPS = 5 #number of segments evaluated for annotation
        self.STICHTAG = datetime(2023,2,25,0,0,0)
        self.autoscan_ix = 0
        #TODO: remove self.autoscan_active = False
        self.locs_union = []
        self.freq_union = []
        self.oldposition = 0
        self.open_template_flag = False
        self.ovwrt_flag = False
        self.ui = MyWizard()
        self.ui.setupUi(self)

        ## TODO: wavheader-Writing zum Button Insert Header connecten
        # connect menubar events
        self.ui.actionFile_open.triggered.connect(self.open_file)
        # self.ui.actionSave_header_to_template.triggered.connect(self.write_template_wavheader)
        self.ui.actionSave_header_to_template.triggered.connect(self.save_header_template)
        self.ui.actionLoad_template_header.triggered.connect(self.open_template_file)
        self.ui.actionOverwrite_header.triggered.connect(self.overwrite_header)
        self.ui.pushButton_Scan.setEnabled(False)
        self.ui.pushButtonAnnotate.setEnabled(False)
        self.ui.pushButton_Scan.clicked.connect(self.autoscan)
        self.ui.pushButtonAnnotate.clicked.connect(self.ann_stations) 
        self.ui.pushButtonDiscard.setEnabled(False)
        self.ui.pushButtonDiscard.clicked.connect(self.discard_annot_line)
        self.ui.spinBoxminSNR.valueChanged.connect(self.minSNRupdate)
        self.ui.spinBoxminSNR_ScannerTab.valueChanged.connect(self.minSNRupdate_ScannerTab)
        self.Baselineoffset = self.ui.spinBoxminBaselineoffset.value()
        self.ui.spinBoxminBaselineoffset.valueChanged.connect(self.set_baselineoffset)
        self.ui.tabWidget.setCurrentIndex(2)
        self.ui.pushButton_InsertHeader.setEnabled(False)
        self.ui.pushButton_InsertHeader.clicked.connect(self.overwrite_header)
        self.ui.label_8.setEnabled(False)
        
        # initialize some GUI elements
        self.ui.radioButton_WAVEDIT.setEnabled(True)
        self.ui.radioButton_WAVEDIT.setChecked(False)
        self.ui.radioButton_WAVEDIT.clicked.connect(self.activate_WAVEDIT)
        #self.ui.pushButton_ScanAnn.clicked.connect(self.listclick_test)
        self.ui.Annotate_listWidget.itemClicked.connect(self.ListClicked)
        self.ui.Annotate_listWidget.clear()

        self.ui.tableWidget.setEnabled(False)
        self.ui.tableWidget_3.setEnabled(False)
        self.ui.tableWidget_starttime.setEnabled(False)

        #self.ui.horizontalScrollBar.sliderMoved.connect(self.plot_spectrum_evth)
        #self.ui.horizontalScrollBar.valueChanged.connect(self.plot_spectrum_evth)
        self.ui.progressBar_2.setProperty("value", 0)
        #self.ui.progressBar.setEnabled(True)
        self.ui.horizontalScrollBar.sliderReleased.connect(self.plot_spectrum_evth)
        #self.ui.horizontalScrollBar.actionTriggered.connect(self.plot_spectrum_evth)
        self.SigToolbar.connect(lambda: self.plot_spectrum(self,self.position))
        self.ui.spinBoxNumScan.setProperty("value", 10)
        self.ui.spinBoxminBaselineoffset.setProperty("value", 5)
        # initialize status flags
        self.fileopened = False
        self.scanplotcreated = False

        #read config file if it exists
        self.standardpath = os.getcwd()
        self.metadata = {"last_path": self.standardpath}
        self.ismetadata = False
        try:
            stream = open("config_wizard.yaml", "r")
            self.metadata = yaml.safe_load(stream)
            stream.close()
            self.ismetadata = True
        except:
            print("cannot get metadata")
        
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ui.gridLayout_4.addWidget(self.canvas,3,0,1,4)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ui.gridLayout_4.addWidget(self.toolbar,1,0,2,1)
        self.ax = self.figure.add_subplot(111)

        self.ax.plot([], [])
        self.canvas.draw()

        self.timeref = datetime.now()

    def reset_GUI(self):
        """
        reset GUI elements to their defaults, re-initialize important variables
        code is executed after new file open
        :param none
        :type: none
        :raises [ErrorType]: [ErrorDescription]
        :return: True after completion
        :rtype: booleal
        """
        self.autoscan_ix = 0
        #TODO: remove self.autoscan_active = False
        self.locs_union = []
        self.freq_union = []
        self.oldposition = 0
        self.ui.pushButtonAnnotate.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.pushButton_Scan.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.pushButtonAnnotate.setStyleSheet("background-color : rgb(220, 220, 220)")
        self.ui.pushButton_Scan.setStyleSheet("background-color : rgb(220, 220, 220)")
        self.ui.lineEdit.setText('')
        self.ui.lineEdit.setStyleSheet("background-color : white")
        self.ui.lineEdit.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.Annotate_listWidget.clear()
        self.ui.tab_2.setEnabled(True)
        self.ui.tab_3.setEnabled(True)
        self.ui.tab_4.setEnabled(True)
        self.ui.pushButton_InsertHeader.setEnabled(False)
        self.ui.label_8.setEnabled(False)
        #self.open_template_flag = False
        return True

    def annotation_completed(self):
        self.ui.pushButtonAnnotate.setStyleSheet("background-color : rgb(170, 255, 127)")
        self.ui.pushButtonAnnotate.setEnabled(False)
        self.ui.pushButtonAnnotate.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.pushButtonDiscard.setEnabled(False)
        self.ui.lineEdit.setText('Record has already been annotated. For re-annotation delete annotation folder')
        self.ui.lineEdit.setStyleSheet("background-color : yellow")
        self.ui.lineEdit.setFont(QFont('MS Shell Dlg 2', 12))

    def annotation_activate(self):
        self.ui.pushButtonAnnotate.setStyleSheet("background-color : rgb(220,220,220)")
        self.ui.pushButtonAnnotate.setEnabled(True)
        self.ui.pushButtonAnnotate.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.pushButtonDiscard.setEnabled(False)
        self.ui.lineEdit.setText('annotation can be started or continued')
        self.ui.lineEdit.setStyleSheet("background-color : yellow")
        self.ui.lineEdit.setFont(QFont('MS Shell Dlg 2', 12))

    def annotation_deactivate(self):
        self.ui.pushButtonAnnotate.setStyleSheet("background-color : rgb(220,220,220)")
        self.ui.pushButtonAnnotate.setEnabled(False)
        self.ui.pushButtonAnnotate.setFont(QFont('MS Shell Dlg 2', 12))

    def scan_completed(self):
        self.ui.pushButton_Scan.setStyleSheet("background-color : rgb(170, 255, 127)")
        self.ui.pushButton_Scan.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.pushButton_Scan.setEnabled(False)
        self.ui.pushButtonAnnotate.setEnabled(True)
        self.ui.pushButtonAnnotate.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.lineEdit.setText('autoscan has been completed, peaks and SNRs identified')
        self.ui.lineEdit.setStyleSheet("background-color : yellow")
        self.ui.lineEdit.setFont(QFont('MS Shell Dlg 2', 12))

    def scan_activate(self):
        self.ui.pushButton_Scan.setStyleSheet("background-color : rgb(220,220,220)")
        self.ui.pushButton_Scan.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.pushButton_Scan.setEnabled(True)
        self.ui.pushButtonAnnotate.setEnabled(False)
        self.ui.pushButtonAnnotate.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.lineEdit.setText('autoscan can be started (search for TX peaks and SNR values)')
        self.ui.lineEdit.setStyleSheet("background-color : yellow")
        self.ui.lineEdit.setFont(QFont('MS Shell Dlg 2', 12))

    def scan_deactivate(self):
        self.ui.pushButton_Scan.setStyleSheet("background-color : rgb(220,220,220)")
        self.ui.pushButton_Scan.setFont(QFont('MS Shell Dlg 2', 12))
        self.ui.pushButton_Scan.setEnabled(False)
        self.ui.lineEdit.setText('')
        self.ui.lineEdit.setStyleSheet("background-color : white")
        self.ui.lineEdit.setFont(QFont('MS Shell Dlg 2', 12))

    def minSNRupdate(self):
        self.PROMINENCE = self.ui.spinBoxminSNR.value()
        self.ui.spinBoxminSNR_ScannerTab.setProperty("value", self.PROMINENCE)

    def minSNRupdate_ScannerTab(self):
        self.PROMINENCE = self.ui.spinBoxminSNR_ScannerTab.value()
        self.ui.spinBoxminSNR.setProperty("value", self.PROMINENCE)
        self.position = self.ui.horizontalScrollBar.value()
        self.plot_spectrum(self,self.position)
        #self.plot_spectrum_evth()

    def set_baselineoffset(self):        
        self.Baselineoffset = self.ui.spinBoxminBaselineoffset.value()
        self.ui.label_6.setText("Baseline Offset:" + str(self.ui.spinBoxminBaselineoffset.value()))
        self.position = self.ui.horizontalScrollBar.value()
        self.plot_spectrum(self,self.position)
        #.plot_spectrum_evth()

    def activate_WAVEDIT(self):
        self.show()
        if self.ui.radioButton_WAVEDIT.isChecked() is True:
                    self.ui.tableWidget.setEnabled(True)
                    self.ui.tableWidget_starttime.setEnabled(True)
                    self.ui.tableWidget_3.setEnabled(True)      
        else:
                    self.ui.tableWidget.setEnabled(False)
                    self.ui.tableWidget_starttime.setEnabled(False)
                    self.ui.tableWidget_3.setEnabled(False)

    def ann_spectrum(self,dummy,data):
        """
        generate a single spectrum from complex data
        scale x-axis as frequencies in the recorded AM band
        scale y-axis in dB
        calculate baseline basel from moving median filtering
        find spectral peaks (= transmitters) and calculate the corresponding properties
        requires the following properties to exist:
            self.DATABLOCKSIZE
        :param self: An instance of the class containing attributes such as header information and filtering parameters.
        :type self: object
        :param dummy: A dummy variable not used in the function.
        :type dummy: any
        :param data: A numpy array containing the complex data IQ data read from wav file
        :type data: numpy.ndarray of float32, even entries = real odd entries = imaginary
                part of the IQ signal
        :raises [ErrorType]: [ErrorDescription]
        :return: A dictionary containing various arrays related to the spectral analysis:
                - datax: The frequency data.type: float32
                - datay: The amplitude data.type: float32
                - datay_filt: The filtered amplitude data.type: float32
                - peaklocs: The indices of the identified peaks in the amplitude data.type: float32
                - peakprops: Properties of the identified peaks, such as their height and width. type: dict
                - databasel: The baseline data used in the filtering process.type: float32
        :rtype: dict
        """
        # extract imaginary and real parts from complex data 
        realindex = np.arange(0,self.DATABLOCKSIZE,2)
        imagindex = np.arange(1,self.DATABLOCKSIZE,2)
        #calculate spectrum and shift/rescale appropriately
        spr = np.abs(np.fft.fft((data[realindex]+1j*data[imagindex])))
        N = len(spr)
        spr = np.fft.fftshift(spr)
        flo = self.wavheader['centerfreq'] - self.wavheader['nSamplesPerSec']/2
        fup = self.wavheader['centerfreq'] + self.wavheader['nSamplesPerSec']/2
        freq0 = np.linspace(0,self.wavheader['nSamplesPerSec'],N)
        freq = freq0 + flo
        datax = freq
        datay = 20*np.log10(spr)
        # filter out all data below the baseline; baseline = moving median
        # filter kernel is self.FILTERKERNEL % of the spectral span
        datay_filt = datay
        kernel_length = int(N*self.FILTERKERNEL/100)
        # kernel length must be odd integer
        if (kernel_length % 2) == 0:
            kernel_length += 1
        databasel = sig.medfilt(datay,kernel_length)
        datay_filt[datay_filt < databasel] = databasel[datay_filt < databasel]         
        # find all peaks which are self.PROMINENCE dB above baseline and 
        # have a min distance of self.DELTAF and a min width of self.PEAKWIDTH
        dist = np.floor(self.DELTAF/self.wavheader['nSamplesPerSec']*N)
        wd = np.floor(self.PEAKWIDTH/self.wavheader['nSamplesPerSec']*N)
        peaklocs, peakprops = sig.find_peaks(datay_filt,
                        prominence=(self.PROMINENCE,None), distance=dist, width = wd)
        ret = {"datax": datax, "datay": datay, "datay_filt": datay_filt,
               "peaklocs": peaklocs, "peakprops": peakprops, "databasel": databasel}
        return ret

    def plot_spectrum_evth(self):
        #TODO: in dieser Form Obsolet, ersetzen !
        self.position = self.ui.horizontalScrollBar.value()
        self.plot_spectrum(self,self.position)
        self.oldposition = self.position

    def readsegment(self):
        """
        opens file self.f1 and reads a data segment from position 216 + position determined by scrollbar
        segment is returned as float array of complex numbers, even entries = real, odd entries = imaginary
        :param self: An instance of the class containing attributes such as header information and filtering parameters.
        :type self: object
        :raises [ErrorType]: [ErrorDescription]
        :return: data: 
        :rtype: np.float32 array of size self.DATABLOCKSIZE
        """
        self.fileHandle = open(self.f1, 'rb')
        if self.wavheader['nBitsPerSample'] == 16:
            position = int(np.floor(4*np.round(self.wavheader['data_nChunkSize']*self.horzscal/4000)))
            self.fileHandle.seek(216+position, 0)
            dataraw = np.empty(self.DATABLOCKSIZE, dtype=np.int16)
            size = self.fileHandle.readinto(dataraw)
            if size == 0:
                return False
            data = dataraw.astype(np.float32)/32767
            self.duration = self.wavheader['data_nChunkSize']/4/self.wavheader['nSamplesPerSec']
        if self.wavheader['nBitsPerSample'] == 32:
            position = int(np.floor(8*np.round(self.wavheader['data_nChunkSize']*self.horzscal/8000)))
            self.fileHandle.seek(216+position, 0)
            dataraw = np.empty(self.DATABLOCKSIZE, dtype=np.int32)
            size = self.fileHandle.readinto(dataraw)
            if size == 0:
                return False
            data = dataraw.astype(np.float32)
            self.duration = self.wavheader['data_nChunkSize']/8/self.wavheader['nSamplesPerSec']
        print('data read')
        self.fileHandle.close()
        return data

    def plot_spectrum(self,dummy,position):
        """assign a plot window and a toolbar to the tab 'scanner'
        :param : none
        :type : none
        :raises [ErrorType]: [ErrorDescription]
        :return: flag False or True, False on unsuccessful execution
        :rtype: Boolean
        """
        if self.fileopened == False:
            return(False)
        else:
            print('plot spectrum')
            self.horzscal = position
            print(f"scrollbar value:{self.horzscal}")
            
            # read datablock corresponding to current sliderposition
            #TODO: correct 32 bit case
            data = self.readsegment()
            pdata = self.ann_spectrum(self,data)
            print('annotated')
            #TODO: make function for plotting data , reuse in autoscan
            datax = pdata["datax"]
            datay = pdata["datay"]
            basel = pdata["databasel"] + self.Baselineoffset
            peaklocs = pdata["peaklocs"]
            peakprops = pdata["peakprops"]
            # create axis, clear old one and plot data
            print('start axes')
            self.ax.clear()
            self.ax.plot(datax,datay, '-')
            self.ax.plot(datax[peaklocs], datay[peaklocs], "x")
            self.ax.plot(datax,basel, '-', color = "C2")
            self.ax.set_xlabel('frequency (Hz)')
            self.ax.set_ylabel('amplitude (dB)')
            # self.ax.vlines(x=datax[peaklocs], ymin=datay[peaklocs] - peakprops["prominences"],
            #     ymax = datay[peaklocs], color = "C1")
            self.ax.vlines(x=datax[peaklocs], ymin = basel[peaklocs],
                ymax = datay[peaklocs], color = "C1")
            self.ax.hlines(y=peakprops["width_heights"], xmin=datax[peakprops["left_ips"].astype(int)],
                xmax=datax[peakprops["right_ips"].astype(int)], color = "C1")
            self.canvas.draw()

            #display ev<luation time
            displtime = str(self.rectime + (self.recstop-self.rectime)*self.horzscal/1000)
            self.ui.lineEdit_2.setText('Evaluation time: '+ displtime + ' UTC')

            self.plotcompleted = True
            
            #TODO: remove 
            #if self.autoscan_active == True:
                #self.autoscan()

        return(True)
        #time_axis = np.empty(self.DATABLOCKSIZE)
        # duration of the record
        # tax_start = horzscal/1000*self.duration
        # tax_stop = tax_start + self.DATABLOCKSIZE/2/self.wavheader['nSamplesPerSec']
        # time_axis = np.linspace(tax_start,tax_stop,int(self.DATABLOCKSIZE/2))

    def autoscan(self):
        """scan through the recording, plot spectra and calculate mean peak info
            in tab 'scanner' as well as SNR
        :param : none
        :type : none
        :raises [ErrorType]: [ErrorDescription]
        :return: none
        :rtype: none
        """
        self.ui.label.setText("Status: Scan spectra for prominent TX peaks")
        #TODO: check after threading implementation if Text update is done
        #print('autoscan')
        #TODO: remove 
        #######CHECK   self.autoscan_active = True
        self.scan_deactivate()
        self.ui.pushButton_Scan.setEnabled(False)
        self.ui.horizontalScrollBar.setEnabled(False)
        self.NUMSNAPS = self.ui.spinBoxNumScan.value()
        self.PROMINENCE = self.ui.spinBoxminSNR.value()
        self.annot = [dict() for x in range(self.NUMSNAPS)]
        for self.autoscan_ix in range(self.NUMSNAPS+1):
            #set scrollbar to position
            print(f"autoindex:{self.autoscan_ix}")
            self.position = int(np.floor(self.autoscan_ix/self.NUMSNAPS*1000))
            self.horzscal = self.position
            if self.autoscan_ix > self.NUMSNAPS-1:
                self.autoscan_ix = 0  #??????????? necessary
                #TODO: remove self.autoscan_active = False  #?????????? necessary
                plt.close()
            else:
                print(f"autoindex:{self.autoscan_ix}")
                data = self.readsegment()
                pdata = self.ann_spectrum(self,data)
                self.annot[self.autoscan_ix]["FREQ"] = pdata["datax"] 
                self.annot[self.autoscan_ix]["PKS"] = pdata["peaklocs"]
                #TODO: remove: peakprops = pdata["peakprops"]
                peaklocs = pdata["peaklocs"]
                datay = pdata["datay"]
                basel = pdata["databasel"] + self.Baselineoffset
                self.annot[self.autoscan_ix]["SNR"] = datay[peaklocs] - basel[peaklocs]

                #collect all peaks which have occurred at least once in an array
                self.locs_union = np.union1d(self.locs_union, self.annot[self.autoscan_ix]["PKS"])
                self.freq_union = np.union1d(self.freq_union, self.annot[self.autoscan_ix]["FREQ"][self.annot[self.autoscan_ix]["PKS"]])
                
                if self.autoscan_ix > 0:
                    plt.cla()
                plt.plot(pdata["datax"],pdata["datay"])
                plt.show()
                plt.pause(0.001)
        # purge self.locs.union and remove elements the frequencies of which are
        # within 1 kHz span 
        uniquefreqs = pd.unique(np.round(self.freq_union/1000))
        xyi, x_ix, y_ix = np.intersect1d(uniquefreqs, np.round(self.freq_union/1000), return_indices=True)

        self.locs_union = self.locs_union[y_ix]
        self.freq_union = self.freq_union[y_ix]

        meansnr = np.zeros(len(self.locs_union))
        minsnr = 1000*np.ones(len(self.locs_union))
        maxsnr = -1000*np.ones(len(self.locs_union))

        reannot = {}
        for ix in range(self.NUMSNAPS): 
            # find indices of current LOCS in the unified LOC vector self.locs_union
            sharedvals, ix_un, ix_ann = np.intersect1d(self.locs_union, self.annot[ix]["PKS"], return_indices=True)
            # write current SNR to the corresponding places of the self.reannotated matrix
            reannot["SNR"] = np.zeros(len(self.locs_union))
            reannot["SNR"][ix_un] = self.annot[ix]["SNR"][ix_ann]
            #Global Statistics, without consideration whether some peaks vanish or
            #appear when running through all values of ix
            meansnr = meansnr + reannot["SNR"]
            #min and max SNR data are currently not being used.
            minsnr = np.minimum(minsnr, reannot["SNR"])
            maxsnr = np.maximum(maxsnr, reannot["SNR"])

        # collect cumulative info in a dictionary and write the info to the annotation yaml file 
        self.annotation = {}
        self.annotation["MSNR"] = meansnr/self.NUMSNAPS
        self.annotation["FREQ"] = np.round(self.freq_union/1000) # signifikante Stellen
        yamldata = [dict() for x in range(len(self.annotation["FREQ"]))]

        for ix in range(len(self.annotation["FREQ"])):
            yamldata[ix]["FREQ:"] = str(self.annotation["FREQ"][ix])
            yamldata[ix]["SNR:"] = str(np.floor(self.annotation["MSNR"][ix]))
        
        if os.path.isdir(self.my_dirname + '/' + self.my_filename) == False:
            os.mkdir(self.my_dirname + '/' + self.my_filename)

        #self.annotation_filename = self.my_dirname + '/' + self.my_filename + '/snrannotation.yaml'
        #TODO: check if file exists
        stream = open(self.annotation_filename, "w")
        yaml.dump(yamldata, stream)
        stream.close()
        self.ui.horizontalScrollBar.setEnabled(True)
        self.ann_stations()
        return True

    def ann_stations(self):
        self.stations_filename = self.my_dirname + '/' + self.my_filename + '/stations_list.yaml'
        if os.path.exists(self.stations_filename) == False:

            # read Annotation_basis table from mwlist.org
            self.ui.label.setText("Status: read MWList table for annotation")
            MWlistname = self.standardpath + '\\MWLIST_Volltabelle.xlsx'
            print('read MWLIST table from ' + MWlistname)
            time.sleep(0.1)
            T = pd.read_excel(MWlistname)
            #print("generate annotation basis")
            self.ui.label.setText("Status: Generate annotation basis")
            freq = [] # column with all tabulated frequencies in MWtabelle
            closed = [] # column with dates of corresponding closure times if available (if element in table is type datetime)
            for ix in range(len(T)):
                testclosed = T.closed.iloc[ix]
                dummytime = datetime(5000,1,1,1,1,1)
                if type(testclosed) == datetime:
                    closed.append(datetime.strptime(str(testclosed), '%Y-%m-%d %H:%M:%S'))
                    #stations which are not closed must have dummy entries where no datetime
                else:
                    closed.append(datetime.strptime(str(dummytime), '%Y-%m-%d %H:%M:%S'))
                freq.append(float(T.freq.iloc[ix]))
            self.ui.label.setText("Status: annotate peaks and write stations list to yaml file")

            with open(self.stations_filename, 'w', encoding='utf-8') as f:
                # TODO: rectime prüfen, was wenn dummy eintrag ?
                # Laufe durch alle Peak-Frequenzen des Spektrums mit index ix
                for ix in range(len(self.locs_union)):
                    progress = np.floor(100*ix/len(self.locs_union))
                    print(f"peak index during annotation:{ix}")
                    f.write('- frequency: "{}"\n'.format(self.annotation["FREQ"][ix]))
                    f.write('  snr: "{}"\n'.format(round(self.annotation["MSNR"][ix])))
                    # locs union enthält nur Frequenzindices, nicht Frequenzen ! ggf. umrechnen !
                    # suche für jede freq ix alle MWtabellen-Einträge mit der gleichen Frequenz und sammle die entspr Tabellenindices im array ixf
                    ixf = [i for i, x in enumerate(freq) if np.abs((x - self.annotation["FREQ"][ix])) < 1e-6]
                    if np.size(ixf) > 0:
                        # wenn ixf nicht leer setze Landeszähler ix_c auf 0, initialisiere flag cs auf 'none'
                        cs = [] # memory for current country
                        sortedtable = [] #Setze sortedtable zurück
                        yaml_ix = 0
                        for ix2 in ixf:
                            print(ix2)
                            # für jeden index ix2 in ixf zum Peak ix prüfe ob es den String 'ex ' in der Stationsspalte der MWTabelle gibt
                            if type(T.station.iloc[ix2]) != str:
                                curr_station = 'No Name'
                            else:
                                curr_station = T.station.iloc[ix2]
                            if type(T.programme.iloc[ix2]) != str:
                                curr_programme = 'No Name'
                            else:
                                curr_programme = T.programme.iloc[ix2]
                            if type(T.tx_site.iloc[ix2]) != str:
                                curr_tx_site = 'No Name'
                            else:
                                curr_tx_site = T.tx_site.iloc[ix2]

                            stdcheck = 'ex ' in curr_station
                            # für jeden index ix2 in ixf zum Peak ix prüfe ob es den String 'INACTI' in der Stationsspalte der MWTabelle gibt
                            inactcheck = 'INACTI' in curr_station
                            # logisches label falls ()'ex ' oder 'INACT') und recording-time > Stichtag der MWTabellen-Erstellung
                            # kennzeichnet, wenn ein Sender sicher zum Zeitpunkt der Aufnahme geschlossen war
                            auto_closedlabel = (stdcheck or inactcheck) and (self.rectime >= self.STICHTAG)
                            if not ((closed[ix2] - self.rectime).days <= 0 or auto_closedlabel):
                                #wenn NICHT (geschlossen oder recording-time >= explizite Schließzeit in der Spalte closed) --> Sender ist Kandidat
                                # Progeamm und Station aus MWTabelle übernehmen
                                # Land country aus MWTabelle übernehmen
                                station = '{}{}'.format(curr_programme, curr_station)
                                tx_site = curr_tx_site
                                country = T.country.iloc[ix2]
                                if country in cs:  # falls cs bereits das aktuelle Land innerhalb der aktuellen Liste ixf der Einträge zu Frequenz ix beinhaltet 
                                    cix = [i for i,x in enumerate(cs) if x == country][0]
                                    sortedtable[cix]['station' + str(cix)] += station + '; '
                                    sortedtable[cix]['tx_site' + str(cix)] += tx_site + '; '
                                else:
                                # Trag ins dictionary sortedtable die Felder Station, Tx-site und country 
                                # als neuen Block ein
                                    sortedtable.append({'station' + str(yaml_ix): station + '; ',
                                                    'tx_site' + str(yaml_ix): tx_site + '; ',
                                                    'country' + str(yaml_ix): country})
                                    cs.append(country)  # memorize the entered country
                                    yaml_ix += 1
                        # for this ixf (i.e. this peak frequency) write all entries of the sorted table
                        for ix2 in range(len(sortedtable)):
                            
                            country_string = '  country' +str(ix2) + ': "{}"\n'.format(sortedtable[ix2]['country' + str(ix2)])
                            programme_string = '  programme' +str(ix2) + ': "{}"\n'.format(sortedtable[ix2]['station' + str(ix2)])
                            tx_site_string = '  tx-site' +str(ix2) + ': "{}"\n'.format(sortedtable[ix2]['tx_site' + str(ix2)])
                            f.write(country_string)
                            f.write(programme_string)
                            f.write(tx_site_string)
                            time.sleep(0.1)
                    else:
                        f.write('  country0: "not identified"\n')
                        f.write('  programme0: "not identified"\n')
                        f.write('  tx-site0: "not identified"\n')
                    self.ui.progressBar_2.setProperty("value", int(progress))
                    self.ui.progressBar_2.update()
                    self.ui.progressBar_2.hide()
                    self.ui.progressBar_2.show()
                    time.sleep(0.1)
            #memorize status in status-yaml: curent frequency index = 0 and annotation not completed
            #self.status_filename = self.my_dirname + '/' + self.my_filename + '/status.yaml'
            status = {}
            status["freqindex"] = 0
            status["annotated"] = False
            stream = open(self.status_filename, "w")
            yaml.dump(status, stream)
            stream.close()

            self.ui.progressBar_2.setProperty("value", 0)
            self.scan_completed()
            #self.ui.pushButton_Scan.setStyleSheet("background-color : rgb(170, 255, 127)")
            #self.ui.pushButtonAnnotate.setEnabled(True)
        else:
            self.scan_completed()
            try:
                stream = open(self.status_filename, "r")
                status = yaml.safe_load(stream)
                stream.close()
            except:
                print("cannot get status")
                return False 
            
            if status["annotated"] == True:
                self.annotation_completed()
            else:
                freq_ix = status["freqindex"]
                try:
                    stream = open(self.stations_filename, "r", encoding="utf8")
                    self.stations = yaml.safe_load(stream)
                    stream.close()
                except:
                    print("cannot get stations list")
                    return False
                self.ui.lineEdit.setText('Frequency: ' + str(self.stations[freq_ix]['frequency'] + ' kHz'))
                self.ui.lineEdit.setFont(QFont('MS Shell Dlg 2', 12))
            self.interactive_station_select()


    def interactive_station_select(self):
        """
        read yaml stations_list.yaml

        """
        self.ui.Annotate_listWidget.clear()
        ### reading again the yaml is inefficient: could be passed from ann_stations
        try:
            stream = open(self.status_filename, "r")
            status = yaml.safe_load(stream)
            stream.close()
        except:
            print("cannot get status")
            return False 
        try:
            stream = open(self.stations_filename, "r", encoding="utf8")
            self.stations = yaml.safe_load(stream)
            stream.close()
        except:
            print("cannot get stations list")
            return False
        
        freq_ix = status["freqindex"] # read last frequency index which was treated in interactive list checking
        if freq_ix >= len(self.stations):
            self.annotation_completed()
            status["annotated"] = True
            stream = open(self.status_filename, "w")
            yaml.dump(status, stream)
            stream.close()
            return False
        plen = int((len(self.stations[freq_ix])-2)/3) #number of station candidates
        self.ui.lineEdit.setText('Frequency: ' + str(self.stations[freq_ix]['frequency'] + ' kHz'))
        time.sleep(0.1)
        
        for ix2 in range(plen):
            country_string = self.stations[freq_ix]['country' + str(ix2)]
            programme_string = self.stations[freq_ix]['programme' + str(ix2)]
            tx_site_string = self.stations[freq_ix]['tx-site' + str(ix2)]
            item = QtWidgets.QListWidgetItem()
            self.ui.Annotate_listWidget.addItem(item)
            item = self.ui.Annotate_listWidget.item(ix2)
            item.setText(country_string.strip('\n') + ' | ' + programme_string.strip('\n') + ' | ' + tx_site_string.strip('\n'))
            time.sleep(0.1)
        self.ui.pushButtonDiscard.setEnabled(True)
        #self.ui.lineEdit.setText('Frequency: ' + str(self.stations[freq_ix]['frequency'] + ' kHz'))
        #QMessageBox.information(self, "ListWidget", "select station by clicking on respective table entry, scroll down if appropriate")
        #print(f"table edited : {str(freq_ix)}")
        #at the end leave and wait for advancement by button >

    def ListClicked(self,item):

        #memorize status and advance freq_ix
        try:
            stream = open(self.status_filename, "r")
            status = yaml.safe_load(stream)
            stream.close()
        except:
            print("cannot get status")
            return False 
        freq_ix = status["freqindex"] # read last frequency index which was treated in interactive list checking
        if freq_ix < len(self.stations):
            #read index of clicked row and fetch associated content from stations list
            cr_ix = self.ui.Annotate_listWidget.currentRow()
            country_string = '  country: "{}"\n'.format(self.stations[freq_ix]['country' + str(cr_ix)])
            programme_string = '  programme: "{}"\n'.format(self.stations[freq_ix]['programme' + str(cr_ix)])
            tx_site_string = '  tx-site: "{}"\n'.format(self.stations[freq_ix]['tx-site' + str(cr_ix)])
            self.ui.lineEdit.setText('Frequency: ' + str(self.stations[freq_ix]['frequency']) + ' kHz | ' + country_string + ' | ' + programme_string)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("station selected")
            msg.setInformativeText("Station selected; Append to annotation list ?")
            msg.setWindowTitle("annotate")
            msg.addButton('remove from record',QMessageBox.AcceptRole)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.buttonClicked.connect(self.popup)
            ret = msg.exec_()

            if self.yesno == "&Yes":
                #cr_ix = self.ui.Annotate_listWidget.currentRow()
                #print(f"you clicked Item : {item.text()[9]}")
                with open(self.cohiradia_metadata_filename, 'a+', encoding='utf-8') as f:
                    # append selected station to cohiradia annotation file
                    f.write('- frequency: "{}"\n'.format(self.stations[freq_ix]['frequency']))
                    f.write('  snr: "{}"\n'.format(self.stations[freq_ix]['snr']))
                    f.write(country_string)
                    f.write(programme_string)
                    f.write(tx_site_string)
                    self.ui.Annotate_listWidget.clear()
                freq_ix += 1
                status["freqindex"] = freq_ix
                status["annotated"] = False
                stream = open(self.status_filename, "w")
                yaml.dump(status, stream)
                stream.close()
                self.interactive_station_select()
                return True
            else:
                if self.yesno == '&No':
                    return False
                    #TODO: set button Annotate green
                else:
                    #Discard this frequency, advance freq counter, do not write to cohiradia annotation
                    freq_ix += 1
                    status["freqindex"] = freq_ix
                    status["annotated"] = False
                    stream = open(self.status_filename, "w")
                    yaml.dump(status, stream)
                    stream.close()
                    self.interactive_station_select()
                    return False
        # end of stationslist reached
        status["freqindex"] = freq_ix
        status["annotated"] = True
        stream = open(self.status_filename, "w")
        yaml.dump(status, stream)
        stream.close()
        self.annotation_completed()

    def discard_annot_line(self):
        try:
            stream = open(self.status_filename, "r")
            status = yaml.safe_load(stream)
            stream.close()
        except:
            return False 
        freq_ix = status["freqindex"] # read last frequency index which was treated in interactive list checking
        #Discard this frequency, advance freq counter, do not write to cohiradia annotation
        freq_ix += 1
        status["freqindex"] = freq_ix
        status["annotated"] = False
        stream = open(self.status_filename, "w")
        yaml.dump(status, stream)
        stream.close()
        self.interactive_station_select()
        return False

    def open_template_file(self):
        print(f"current path:{self.standardpath}")
        self.open_template_flag = True
        
        if self.FileOpen() is False:
            self.fileopened = False
            return False
        else:
            self.fileopened = True

    def open_file(self):
        self.open_template_flag = False
        try:
            stream = open("config_wizard.yaml", "r")
            self.metadata = yaml.safe_load(stream)
            stream.close()
            self.ismetadata = True
        except:
            print("cannot get metadata")
        
        self.ui.spinBoxminSNR_ScannerTab.setProperty("value", self.PROMINENCE)
        
        if self.fileopened is True:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("open new file")
            msg.setInformativeText("you are about o open another file. Current file will be closed; Do you want to proceed")
            msg.setWindowTitle("FILE OPEN")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.buttonClicked.connect(self.popup)
            msg.exec_()

            if self.yesno == "&Yes":
                #self.fileHandle.close()
                if self.FileOpen() is False:
                    self.fileopened = False
                    return False
        else:
            if self.FileOpen() is False:
                self.fileopened = False
                return False
            else:
                self.fileopened = True
                #print("self.fileopened called")

    def save_header_template(self):
        # TODO: if the file extension is type .dat, then also rename the file appropriately
        print("save header template")
        if self.fileopened == False:
            return False
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("write wav header template")
        msg.setInformativeText("you are about to overwrite the template wav header. Do you really want to proceed ?")
        msg.setWindowTitle("overwrite template wav header")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.popup)
        msg.exec_()

        if self.yesno == "&Yes":
            self.ovwrt_flag = False
            self.write_edited_wavheader()

    def overwrite_header(self):
        print("overwrite header")
        if self.fileopened == False:
            return False
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("overwrite wav header")
        msg.setInformativeText("you are about to overwrite the header of the current wav file with the values in the tables of Tab 'WAV Header'. Do you really want to proceed ?")
        msg.setWindowTitle("overwrite")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.popup)
        msg.exec_()

        if self.yesno == "&Yes":
            self.ovwrt_flag = True
            self.write_edited_wavheader()

        #TODO: write backup dump header

    def popup(self,i):
        self.yesno = i.text()
        # print(i.text())

    def listclick_test(self):
        #widget = self.Annotate_listWidget
       # QtCore, QtGui, QtWidgets
        
        item = self.ui.Annotate_listWidget.item(0)
        item.setText("TESTITEM1 changed")
        item = self.ui.Annotate_listWidget.item(1)
        item.setText("TESTITEM2 changed")

    def FileOpen(self):
        '''
        Purpose: 
        If self.####### == True:
            (1) Open data file for read
            (2) call routine for extraction of recording parameters from filename
            (3) present recording parameters in info fields
        Returns: True, if successful, False otherwise
        '''
        self.reset_GUI()
        filters = "SDR wav files (*.wav);;Raw IQ (*.dat *.raw )"
        selected_filter = "SDR wav files (*.wav)"
        if self.open_template_flag == False:
            if self.ismetadata == False:
                filename =  QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "Open data file"
                                                                , self.standardpath, filters, selected_filter)
            else:
                print('open file with last path')
                filename =  QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "Open data file"
                                                                ,self.metadata["last_path"] , filters, selected_filter)
            self.f1 = filename[0]    
        else:
            
            filename = self.standardpath + '/templatewavheader.wav'
            if os.path.exists(filename) == True:
                self.open_template_flag = False
                self.f1 = filename
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("File not found")
                msg.setInformativeText("Standard template with filename templatewavheader.wav not found in root directory, cannot proceed")
                msg.setWindowTitle("file not found")
                msg.exec_()
        
        if not self.f1:
            return False

        self.my_dirname = os.path.dirname(self.f1)
        self.my_filename, ext = os.path.splitext(os.path.basename(self.f1))
        self.stations_filename = self.my_dirname + '/' + self.my_filename + '/stations_list.yaml'
        self.status_filename = self.my_dirname + '/' + self.my_filename + '/status.yaml'
        self.annotation_filename = self.my_dirname + '/' + self.my_filename + '/snrannotation.yaml'
        self.cohiradia_metadata_filename = self.my_dirname + '/' + self.my_filename + '/cohiradia_metadata.yaml'
        
        self.annotation_deactivate()
        self.scan_deactivate()
        self.ui.pushButtonDiscard.setEnabled(False)
        
        if ext == ".dat": 
            self.filetype = "dat"
            self.ui.tab_2.setEnabled(False)
            self.ui.tab_3.setEnabled(False)
            self.ui.tab_4.setEnabled(False)
            ##TODO: write current wavheader to start of dat file
            ## TODO: wavheader-Writing zum Button Insert Header connecten
            self.ui.label_8.setEnabled(True)
            self.ui.pushButton_InsertHeader.setEnabled(True)

            print('dat header writing currently not yet fully supported')
        else:
            if ext == ".wav":
                self.filetype = "wav"
                self.ui.tab_2.setEnabled(True)
                self.ui.tab_3.setEnabled(True)
                self.ui.tab_4.setEnabled(True)
                self.ui.label_8.setEnabled(False)
                self.ui.pushButton_InsertHeader.setEnabled(False)
            else:
                #TODO error dialogue
                print("Error , neither dat nor wav format")

            if self.filetype == "dat" and self.filenameparams_extract() == False: # namecheck only if dat --> makes void all wav-related operation sin filenameextract
                print('dat files not yet supported')
                return False
            
            else:
                # TODO: open with PERSEUS header if appropriate
                # open with SDRUno fileheader
                self.wavheader = WAVheader_tools.get_sdruno_header(self)
                self.next_filename = self.extract_startstoptimes_auxi(self.wavheader)
                self.ifreq = self.wavheader['centerfreq']
                self.irate = self.wavheader['nSamplesPerSec']
                SDRtypestr = str(self.wavheader['sdrtype_chckID'])
                if SDRtypestr.find('auxi'):
                    self.sdrtype = 'AUXI'
                else:                
                    if SDRtypestr.find('rcvr'):
                        self.sdrtype = 'PERSEUS'
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("under construction")
                        msg.setInformativeText("PERSEUS HEader, not yet implemented")
                        msg.setWindowTitle("under construction")
                        msg.exec_()
                        return False
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("SDRTYPE UNKNOWN")
                        msg.setInformativeText("cannot process wav header")
                        msg.setWindowTitle("SDR TYPE UNKNOWN")
                        msg.exec_()
                        return False
                self.fill_wavtable()
            
            # TODO rootpath for config file ! 
            # TODO: append metadata instead of new write
            self.metadata = {"last_path": self.my_dirname}
            stream = open("config_wizard.yaml", "w")
            yaml.dump(self.metadata, stream)
            stream.close()

            self.stations_filename = self.my_dirname + '/' + self.my_filename + '/stations_list.yaml'
            if os.path.exists(self.stations_filename) == True:
                self.scan_completed()
                try:
                    stream = open(self.status_filename, "r")
                    status = yaml.safe_load(stream)
                    stream.close()
                except:
                    print("cannot get status")
                    return False 
                if status["annotated"] == True:
                    self.annotation_completed()
                else:
                    self.annotation_activate()
            else:
                self.scan_activate()
        self.fileopened = True
        self.ui.label_6.setText("Bseline Offset:" + str(self.ui.spinBoxminBaselineoffset.value()))
        return True

    def fill_wavtable(self):
        """
        fill tables on TAB wavedit with the respective values from the vaw header
        """
        if self.sdrtype == 'AUXI':
            starttime = self.wavheader['starttime']
            stoptime = self.wavheader['stoptime']
            self.rectime = datetime(starttime[0],starttime[1],starttime[3],starttime[4],starttime[5],starttime[6])
            self.recstop = datetime(stoptime[0],stoptime[1],stoptime[3],stoptime[4],stoptime[5],stoptime[6])
            start_str = str(self.rectime)
            print(start_str)
            
        else:
            starttime = ['x', 'x', 'x', 'x', 'x', 'x','x','x']
            stoptime = starttime
        
        ###Einträge der Tabelle 1 nur Integers
        metastring1 = [self.wavheader['filesize'], self.wavheader['sdr_nChunkSize']]
        metastring1.append(self.wavheader['wFormatTag'])
        metastring1.append(self.wavheader['nChannels'])
        metastring1.append(self.wavheader['nSamplesPerSec'])
        metastring1.append(self.wavheader['nAvgBytesPerSec'])
        metastring1.append(self.wavheader['nBlockAlign'])
        metastring1.append(self.wavheader['nBitsPerSample'])
        metastring1.append(self.wavheader['centerfreq'])
        metastring1.append(self.wavheader['data_nChunkSize'])
        metastring1.append(self.wavheader['ADFrequency'])
        metastring1.append(self.wavheader['IFFrequency'])
        metastring1.append(self.wavheader['Bandwidth'])
        metastring1.append(self.wavheader['IQOffset'])               
        for ix in range(0,14):
            self.ui.tableWidget.item(ix, 0).setData(0,metastring1[ix])
        for ix in range(0,8):
            self.ui.tableWidget_starttime.item(ix, 0).setData(0,starttime[ix])
            self.ui.tableWidget_starttime.item(ix, 1).setData(0,stoptime[ix])

        # write other info to table 3 (strings)                    
        self.ui.tableWidget_3.item(2, 0).setText(start_str)
        self.ui.tableWidget_3.item(1, 0).setText(str(self.wavheader['sdrtype_chckID']))
        self.ui.tableWidget_3.item(0, 0).setText(str(self.wavheader['nextfilename']))
        self.ui.tableWidget_3.item(3, 0).setText(str(self.wavheader['data_ckID']))

    def check_consistency(self,item,dtype,label):
        typetab = {"long": [-2147483647, 2147483647], "ulong": [0, 4294967295], 
                    "short": [-32768, 32767]  , "ushort": [0, 65535],
                    "float": [-3.4E38, 3.4E38]}

        if item < typetab[dtype][0] or item > typetab[dtype][1]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Value error")
            msg.setInformativeText(label + "must be of type " + dtype + ", i.e. in range " + str(typetab[dtype]) + "\n Please correct !")
            msg.setWindowTitle("please correct value")
            msg.exec_()
            return False
        else:
            return True
        
    def write_edited_wavheader(self):

        crit1 = False
        #TODO : ?Sonderzeichencheck ??
        self.wavheader['nextfilename'] = self.ui.tableWidget_3.item(0, 0).text()
        preview = {}
        for ix in range(0,8):
            preview[ix] = int(self.ui.tableWidget_starttime.item(ix, 0).text())
        try:
            a = datetime(preview[0],preview[1],preview[3],preview[4],preview[5],preview[6])
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Date error")
            msg.setInformativeText("start date or time entry is out of valid range, please check and retry")
            msg.setWindowTitle("Date error")
            msg.exec_()
            return False
        if preview[6] > 999:
            crit1 = True

        for ix in range(0,8):
            preview[ix] = int(self.ui.tableWidget_starttime.item(ix, 1).text())
        try:
            a = datetime(preview[0],preview[1],preview[3],preview[4],preview[5],preview[6])
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Date error")
            msg.setInformativeText("stop date or time entry is out of valid range, please check and retry")
            msg.setWindowTitle("Date error")
            msg.exec_()
            return False
        if preview[6] > 999 or crit1 == True:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Date error")
            msg.setInformativeText("ms value in start or stoptime must not be > 999, please check and retry")
            msg.setWindowTitle("Date error")
            msg.exec_()
            return False      
           
        for ix in range(0,8):
            self.wavheader['starttime'][ix] = int(self.ui.tableWidget_starttime.item(ix, 0).text())
            self.wavheader['stoptime'][ix] = int(self.ui.tableWidget_starttime.item(ix, 1).text())

        # ck1 = np.array([])
        # ck1 = self.wavheader['starttime']
        # if 
        # ckref1 = np.array([65536,13,65000,31,25,60,60,1000])
        checklist = ['filesize','sdr_nChunkSize','wFormatTag','nChannels', 'nSamplesPerSec',
            'nAvgBytesPerSec', 'nBlockAlign','nBitsPerSample','centerfreq','data_nChunkSize',
            'ADFrequency','IFFrequency','Bandwidth','IQOffset']
        typelist = ['ulong', 'long', 'short', 'short', 'long', 
                    'long', 'short', 'short', 'long', 'long',
                     'long',  'long',  'long',  'long']
        for ix2 in range(len(checklist)):
            self.wavheader[checklist[ix2]] = int(self.ui.tableWidget.item(ix2, 0).text())
            chk = False
            chk = self.check_consistency(self.wavheader[checklist[ix2]],typelist[ix2],checklist[ix2])
            if chk == False:
                return False
                #self.wavheader[checklist[ix2]] = int(self.ui.tableWidget.item(ix2, 0).text())

        if self.fileopened == True:
            if self.ovwrt_flag == False:
                wav_filename = self.my_dirname + '/templatewavheader.wav'
            else: 
                wav_filename = self.f1
            
            WAVheader_tools.write_sdruno_header(self,wav_filename,self.wavheader,self.ovwrt_flag)   

    def extract_startstoptimes_auxi(self, wavheader):
        """_synthetize next filename in the playlist in case the latter cannot be extracted
        from auxi SDR-wav-header because it is longar than 96 chars_
        can only be used for SDRUno and RFCorder header

        :param : wavheader [dictionary]
        :type : dictionary
        :raises [ErrorType]: [ErrorDescription]
        :return: next_filename
        :rtype: str
        """
        ###TODO error handling
        wavheader['nextfilename'] = (wavheader['nextfilename']).replace('x00','')
        wavheader['nextfilename'] = (wavheader['nextfilename']).replace("'","")
        wavheader['nextfilename'] = (wavheader['nextfilename']).replace('b''','')
        #TODO strip off last \\\\\\
        wavheader['nextfilename'] = wavheader['nextfilename'].rstrip(' ')
        wavheader['nextfilename'] = wavheader['nextfilename'].rstrip('\\')
        nextfilename = wavheader['nextfilename']
        nextfilename_purged = nextfilename.replace('/','\\')
        #nextfilename_purged = nextfilename_purged.replace('x00','')
        # nextfilename_purged = nextfilename_purged.replace('\\','/')
        # nextfilename_purged = nextfilename_purged.replace('//','/')
        # nextfilename_purged = nextfilename_purged.replace('//','/')
        nextfile_dirname = os.path.dirname(nextfilename_purged)
        #TODO: nextfilename dirname is frequently 0 --> quest is invalid
        if len(nextfile_dirname) > 3:
            if (wavheader['nextfilename'][0:2] == "'\\") is False:
                self.loopalive = False   ### stop playlist loop  #######################  loop must be handled inside this method !
                true_nextfilename = ''
            else:
                if wavheader['nextfilename'].find('.wav') != -1: ### take next filename from wav header
                    true_nextfilename, next_ext = os.path.splitext(os.path.basename(nextfilename_purged))
                else: ### synthetize next filename because wav header string for nextfile longer 92 chars
                    datetimestring = self.extract_stopdatetimestring(wavheader)
                    filename_tail = datetimestring + '_' + str(int(wavheader['centerfreq']/1000)) + 'kHz'
                    filename_trunk = self.my_filename[0:self.my_filename.find(datetimestring[1:3])-1]
                    true_nextfilename = filename_trunk + filename_tail + '.wav'
                self.loopalive = True
            return true_nextfilename

    def filenameparams_extract(self):

            #TODO: erkennt COHIRADIA Namenskonvention nicht, wenn vor den _lo_r_c literalen noch andere _# Felder existieren.
            """ extract control parameters from filename (dat, raw files) and/or fileheader (wav-files)
            and check for consistency with COHIRADIA file name convention

            :param [ParamName]: none
            :type [ParamName]: none
            :raises Filename error 1: center frequency offset not integer
            :raises Filename error 2: filename convention not met, cannot extractplayback/resording parameters
            :raises Filename error 3: center frequency not in range (0 - 62500000)
            :raises Filename error 4: sampling rate not in set 20000, 50000, 100000, 250000, 500000, 1250000, 2500000
            :raises Filename error 5: center frequency offset out of range +/- 100 ppm
            :raises warning 1: LO frequency not identifiable in wav-filename, default value 1250 kS/s is used
            :return: Returns: True, if successful, False otherwise (if error exception raised)
            :rtype: Boolean
            """
            if self.filetype == "dat":
                loix = self.my_filename.find('_lo')
                cix = self.my_filename.find('_c')
                rateix = self.my_filename.find('_r')
            #TODO else für wav ? siehe unten bei wav-Metadatenextraktion################
            # in Zukunft obsolet, da Wechsel der Filenamenskonvention
            else:
                rateix = 0
                cix = 0
                loix = 0

            errorf = False                            # test for invalid filename

            if rateix == -1 or cix == -1 or loix == -1:
                errorf = True
                errortxt = "Probably not a COHIRADIO File \n \
                    Filename does not comply with COHIRADIA naming convention"

            if self.filetype == "dat":
                freq = self.my_filename[loix+3:rateix]
                self.ui.label_showLO.setText(str(freq))
                freq = freq + '000'
                if freq.isdecimal():
                    self.ifreq = int(freq, 10) + 1000*i_LO_bias
                else:
                    errorf = True
                    errortxt = "Probably not a COHIRADIO File \n \
                        Literal after _lo does not comply with COHIRADIA\
                        naming convention"

                rate = self.my_filename[rateix+2:cix]
                self.ui.label_showBW.setText(str(rate))
                rate = rate + '000'
                if rate.isdecimal():
                    self.irate = int(rate)
                else:
                    errorf = True
                    errortxt = "Probably not a COHIRADIO dat File \n \
                        Literal after _rate does not comply with COHIRADIA\
                        naming convention"

                corr = self.my_filename[cix+2:len(self.my_filename)]

                if corr.isdecimal():
                    self.icorr = int(corr)
                    if(len(corr) == 0):
                        corr = '000'
                else:
                    errorf = True
                    errortxt = "Probably not a COHIRADIO dat File \n \
                        Literal after _c does not comply with COHIRADIA\
                        naming convention"
            else: # wird derzeit nicht verwendet, eher obsolet da:
                dummy = 0
                    
if __name__ == '__main__':
    
    #initialize logging method
    #logging.basicConfig(filename='cohiradia.log', encoding='utf-8', level=logging.DEBUG)
    
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication([])
    win = WizardGUI()
    #win.setupUi(MyWizard)
#    app.aboutToQuit.connect(win.stop_worker)    #graceful thread termination on app exit
    win.show()
    sys.exit(app.exec_())

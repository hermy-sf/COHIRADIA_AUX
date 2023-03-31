from struct import pack

#methods for wavheader manipulations 

class WAVheader_tools():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Constants
        self.TEST = True    # Test Mode Flag for testing the App without a


    def get_sdruno_header(self):
        """
        opens a file with name self.f1
        extracts meta information from SDR-wav-header_
        recognized formats: SDRUno, PERSEUS, SpectraVue
        closes file after headerreading

        :param : none
        :type : none
        :raises : none
        :return: dictionary wavheader containing the individual metadata items
        :rtype: dictionary
        """
        self.fileHandle = open(self.f1, 'rb')
        wavheader={}
        wavheader['riff_chckID'] = str(self.fileHandle.read(4))
        wavheader['filesize'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        wavheader['wave_string'] = str(self.fileHandle.read(4))
        wavheader['fmt_chckID'] = str(self.fileHandle.read(4))
        wavheader['fmt_nChunkSize'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        wavheader['wFormatTag'] = int.from_bytes(self.fileHandle.read(2), byteorder='little')
        wavheader['nChannels'] = int.from_bytes(self.fileHandle.read(2), byteorder='little')
        wavheader['nSamplesPerSec'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        wavheader['nAvgBytesPerSec'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        wavheader['nBlockAlign'] = int.from_bytes(self.fileHandle.read(2), byteorder='little')
        wavheader['nBitsPerSample'] = int.from_bytes(self.fileHandle.read(2), byteorder='little')
        wavheader['sdrtype_chckID'] = str(self.fileHandle.read(4))
        #####TODO: if sdrtype == 'auxi' do the next, else if 'rcvr' do PERSEUS, else error
        wavheader['sdr_nChunkSize'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        starttime=[0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            starttime[i] = int.from_bytes(self.fileHandle.read(2), byteorder='little')
        stoptime=[0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            stoptime[i] = int.from_bytes(self.fileHandle.read(2), byteorder='little')
        wavheader['starttime'] = starttime
        wavheader['stoptime'] = stoptime
        wavheader['centerfreq'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        wavheader['ADFrequency'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        wavheader['IFFrequency'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        wavheader['Bandwidth'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        wavheader['IQOffset'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        self.fileHandle.read(16) #dummy read, unused fields
        aaa = str(self.fileHandle.read(96))
        wavheader['nextfilename'] = aaa.replace('\\\\','\\')
        wavheader['data_ckID'] = str(self.fileHandle.read(4))
        wavheader['data_nChunkSize'] = int.from_bytes(self.fileHandle.read(4), byteorder='little')
        self.fileHandle.close()
        return(wavheader)
    
    def write_sdruno_header(self,wavfilename,wavheader,ovwrt_flag):
                    
        """write wavheader to the beginning of the current file 'wavfilename'
        if ovwrt_flag == True: 
            overwrite the first 216 bytes of an existing file with wavheader
        else:
            write a new file with the wavheader only; size is always 216 bytes
        
        Important: no check for the right datatypes in wavheader; if incorrect --> program crashes

        :param : wavtargetfilename, wavheader
        :type : file path; dictionary
        :raises : none
        :return: 
        :rtype: 
        """
        if ovwrt_flag == True:
            fid = open(wavfilename, 'r+b')
            fid.seek(0)
        else:
            fid = open(wavfilename, 'wb')

        fid.write(pack("<4sL4s", wavheader['riff_chckID'][2:6].encode('ascii'), wavheader['filesize'], wavheader['wave_string'][2:6].encode('ascii')))
        #  self.wavheader['starttime'][ix] = int(self.ui.tableWidget_starttime.item(ix, 0).text())
        #  self.wavheader['stoptime'][ix] = int(self.ui.tableWidget_starttime.item(ix, 1).text())
        fid.write(pack("<4sI", wavheader['fmt_chckID'][2:6].encode('ascii'), wavheader['fmt_nChunkSize']))
        fid.write(pack("<hhllhh", wavheader['wFormatTag'], wavheader['nChannels'], wavheader['nSamplesPerSec'], 
                       wavheader['nAvgBytesPerSec'], wavheader['nBlockAlign'], wavheader['nBitsPerSample']))
        fid.write(pack("<4sl", wavheader['sdrtype_chckID'][2:6].encode('ascii'), wavheader['sdr_nChunkSize']))
        fid.write(pack("<16h", wavheader['starttime'][0], wavheader['starttime'][1], wavheader['starttime'][2], 
                       wavheader['starttime'][3], wavheader['starttime'][4], wavheader['starttime'][5], 
                       wavheader['starttime'][6], wavheader['starttime'][7], wavheader['stoptime'][0], 
                       wavheader['stoptime'][1], wavheader['stoptime'][2], wavheader['stoptime'][3], 
                       wavheader['stoptime'][4], wavheader['stoptime'][5], wavheader['stoptime'][6], wavheader['stoptime'][7]))
        fid.write(pack("<l", wavheader['centerfreq']))
        # Write ADFrequency, IFFrequency, Bandwidth, and IQOffset as long integers
        fid.write(pack('<l', wavheader['ADFrequency']))
        fid.write(pack('<l', wavheader['IFFrequency']))
        fid.write(pack('<l', wavheader['Bandwidth']))
        fid.write(pack('<l', wavheader['IQOffset']))

        # Write Unused array as four long integers
        dum = 0
        for i in range(4):
            fid.write(pack('<l', dum))

        # Write up to 96 characters of nextfilename as ASCII characters
        for i in range(min(96, len(wavheader['nextfilename']))):
            fid.write(pack('<c', bytes(wavheader['nextfilename'][i], 'ascii')))

        # Write spaces to fill up to 96 characters if nextfilename is shorter
        if len(wavheader['nextfilename']) < 96:
            for i in range(len(wavheader['nextfilename']), 96):
                fid.write(pack('<c', b' '))

        # Write data_ckID and data_nChunkSize
        fid.write(pack('<4s', wavheader['data_ckID'][2:6].encode('ascii')))
        fid.write(pack('<L', wavheader['data_nChunkSize']))

        fid.close()

    def extract_startdatetimestring(self,wavheader):
        """_synthetize a string which contains the 
        start date and time and returns it in the SDRUno filename format
        Format: _YYYYMMDD_hhmmssZ

        :param : wavheader
        :type : dictionary
        :raises [ErrorType]: [ErrorDescription]
        :return: datetimestring
        :rtype: str
            """
        starttime = wavheader['starttime']
        start_year=str(starttime[0])
        if starttime[1] < 10:
            start_month ='0' + str(starttime[1])
        else:
            start_month = str(starttime[1])
        if starttime[3] < 10:
            start_day ='0' + str(starttime[3])
        else:
            start_day = str(starttime[3])
        startdate_string = start_year + start_month + start_day
        if starttime[4] < 10:
            start_hour = '0' + str(starttime[4])
        else:
            start_hour = str(starttime[4])
        if starttime[5] < 10:
            start_min = '0' + str(starttime[5])
        else:            
            start_min = str(starttime[5])
        if starttime[6] < 10:
            start_sec='0' + str(starttime[6])
        else:
            start_sec = str(starttime[6])
        datetimestring = '_' + start_year + start_month + start_day
        datetimestring = datetimestring + '_' +start_hour + start_min +start_sec + 'Z'
        ###TODO: check if also MHz names are possible
                # timeobj1 =  ndatetime.timedelta(seconds=20)
        # str(timeobj2-timeobj1)

        return datetimestring
    
    # def write_sdruno_header_old(self,wavfilename,wavheader,ovwrt_flag):
    #     ###########TODO: remove once validated new function
                    
    #     """write to the beginning of the current file in wavwriteHandle

    #     :param : wavtargetfilename, wavheader
    #     :type : file path; dictionary
    #     :raises : none
    #     :return: 
    #     :rtype: 
    #     """
    #     if ovwrt_flag == True:
    #         fid = open(wavfilename, 'r+b')
    #         fid.seek(0)
    #     else:
    #         fid = open(wavfilename, 'wb')

    #     #with open(wavtargetfilename, 'wb') as f:

    #     fid.write(pack("<4sL4s", wavheader['riff_chckID'][2:6].encode('ascii'), wavheader['filesize'], wavheader['wave_string'][2:6].encode('ascii')))
    #     #TODO: Error Error wavheader with starttime and stoptime indexing: go to 0,1,2,3,4... instead of 0,1, '0' , 2, re-index in 
    #     #  self.wavheader['starttime'][ix] = int(self.ui.tableWidget_starttime.item(ix, 0).text())
    #     #  self.wavheader['stoptime'][ix] = int(self.ui.tableWidget_starttime.item(ix, 1).text())
    #     fid.write(pack("<4sI", wavheader['fmt_chckID'][2:6].encode('ascii'), wavheader['fmt_nChunkSize']))
    #     fid.write(pack("<hhllhh", wavheader['wFormatTag'], wavheader['nChannels'], wavheader['nSamplesPerSec'], 
    #                    wavheader['nAvgBytesPerSec'], wavheader['nBlockAlign'], wavheader['nBitsPerSample']))
    #     fid.write(pack("<4sl", wavheader['sdrtype_chckID'][2:6].encode('ascii'), wavheader['sdr_nChunkSize']))
    #     fid.write(pack("<16h", wavheader['starttime'][0], wavheader['starttime'][1], 0, wavheader['starttime'][2], 
    #                    wavheader['starttime'][3], wavheader['starttime'][4], wavheader['starttime'][5], 
    #                    wavheader['starttime'][6], wavheader['stoptime'][0], 
    #                    wavheader['stoptime'][1], 0, wavheader['stoptime'][2], wavheader['stoptime'][3], 
    #                    wavheader['stoptime'][4], wavheader['stoptime'][5], wavheader['stoptime'][6]))
    #     fid.write(pack("<l", wavheader['centerfreq']))
    #     # Write ADFrequency, IFFrequency, Bandwidth, and IQOffset as long integers
    #     fid.write(pack('<l', wavheader['ADFrequency']))
    #     fid.write(pack('<l', wavheader['IFFrequency']))
    #     fid.write(pack('<l', wavheader['Bandwidth']))
    #     fid.write(pack('<l', wavheader['IQOffset']))

    #     # Write Unused array as four long integers
    #     dum = 0
    #     for i in range(4):
    #         fid.write(pack('<l', dum))

    #     # Write up to 96 characters of nextfilename as ASCII characters
    #     for i in range(min(96, len(wavheader['nextfilename']))):
    #         fid.write(pack('<c', bytes(wavheader['nextfilename'][i], 'ascii')))

    #     # Write spaces to fill up to 96 characters if nextfilename is shorter
    #     if len(wavheader['nextfilename']) < 96:
    #         for i in range(len(wavheader['nextfilename']), 96):
    #             fid.write(pack('<c', b' '))

    #     # Write data_ckID and data_nChunkSize
    #     fid.write(pack('<4s', wavheader['data_ckID'][2:6].encode('ascii')))
    #     fid.write(pack('<L', wavheader['data_nChunkSize']))

    #     fid.close()

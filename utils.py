import logging
from time import strftime
from datetime import datetime
import math
import array
import os

import numpy as np
import zmq

import PBDataDescriptor_pb2 as message_protobuf
import PBVegasData_pb2 as vegas_protobuf
import request_pb2 as request_protobuf
import DataStreamUtils as dsutils

import server_config as cfg
import read_file_data as filedata
import Gnuplot

LCLDIR = os.path.dirname(os.path.abspath(__file__))

def _get_tcp_url(urls):
    for u in urls:
        if "tcp" in u:
            return u
    return ""

def _make_dummy_frequencies(n_subbands):
    frequencies = []
    for n in range(n_subbands):
        start = n * 1000
        sf = range(start, start + cfg.NCHANS)
        frequencies.extend(sf)
    
    return frequencies

def _sky_frequencies(spectra, subbands, df):

    # ----------------------  calculate frequencies

    # create a structure resembling the SAMPLER table from
    #   the VEGAS FITS file
    sampler_dtype = [('BANK_A', np.str_, 8), ('PORT_A', int),
                     ('BANK_B', np.str_, 8), ('PORT_B', int),
                     ('SUBBAND', int), ('CRVAL1', float),
                     ('CDELT1', float)]
    SAMPLER_TABLE = np.array(zip(df.bankA, df.portA,
                                 df.bankB, df.portB,
                                 df.subband, df.crval1,
                                 df.cdelt1), dtype=sampler_dtype)

    lo1, iffile_info = filedata.info_from_files(df.project_id, df.scan_number)

    backend, port, bank = 'VEGAS', 1, SAMPLER_TABLE['BANK_A'][0]
    sff_sb, sff_multi, sff_offset = iffile_info[(backend, port, bank)]

    crval1 = []
    cdelt1 = []
    for sb in subbands:
        mask = SAMPLER_TABLE['SUBBAND']==sb
        crval1.append(SAMPLER_TABLE[mask]['CRVAL1'][0])
        cdelt1.append(SAMPLER_TABLE[mask]['CDELT1'][0])

    display_sky_frequencies = []
    for ii, _ in enumerate(spectra):
        ifval = np.array(range(1,df.number_channels+1))
        # Below I use df.number_channels/2 instead of df.crpix1 because crpix1 
        #  is currently holding the incorrect value of 0.
        # That is a bug in the protobuf Data key sent in the stream from
        #  the manager.
        ifval = crval1[ii] + cdelt1[ii] * (ifval - df.number_channels/2)
        skyfreq = sff_sb * ifval + sff_multi * lo1 + sff_offset
        # only return NCHANS numbers of frequencies for each subband
        display_sky_frequencies.extend((skyfreq[::df.number_channels/cfg.NCHANS]/1e9).tolist())

    return display_sky_frequencies

def blank_window_plot(bank, window, state):
    g = Gnuplot.Gnuplot(persist=0)
    g.xlabel('GHz')
    g.ylabel('counts')
    g('set term png enhanced font '
      '"/usr/share/fonts/liberation/LiberationSans-Regular.ttf" '
      '9 size 600,200')
    g('set data style lines')
    g.title('Spectrometer {} '
            'Window {} {}'.format(bank, window, strftime('  %Y-%m-%d %H:%M:%S')))
    g('set out "{}/static/{}{}.png"'.format(LCLDIR, bank, window))
    g('unset key')
    g('set label "Manager state:  {}" at 0,0.5 center'.format(state))
    g.plot('[][0:1] 2')

def blank_bank_plot(bank, state):
    g = Gnuplot.Gnuplot(persist=0)
    g.xlabel('GHz')
    g.ylabel('counts')
    g('set term png enhanced font '
      '"/usr/share/fonts/liberation/LiberationSans-Regular.ttf" '
      '9 size 600,200')
    g('set data style lines')
    g.title('Spectrometer {} {}'.format(bank, strftime('  %Y-%m-%d %H:%M:%S')))
    g('set out "{}/static/{}.png"'.format(LCLDIR, bank))
    g('unset key')
    g('set label "Manager state:  {}" at 0,0.5 center'.format(state))
    g.plot('[][0:1] 2')

def get_value(context, bank, poller, key, directory_socket,
              vegasdata, request_pending):

    data_socket = vegasdata['socket']

    # This is the REQ wrinkle: only send a request if the last
    # one was serviced. We might find ourselves back here if the
    # directory message was received instead of the data request,
    # in which case we must not make another request. In this
    # case, skip and drop into the poll to wait for the data.
    if not request_pending:
        logging.debug('requesting: {} from {}'.format(key, vegasdata))
        data_socket.send(key, zmq.NOBLOCK)
        request_pending = True

    # this will block. May unblock if request is serviced, *or*
    # if directory service message is received.
    logging.debug('poller.sockets', poller.sockets)
    socks = dict(poller.poll())
    logging.debug('{} socks {}'.format(strftime('%Y/%m/%d %H:%M:%S'), socks))

    # handle directory service message
    if directory_socket in socks:
        logging.debug('DIRECTORY SOCKET message')
        if socks[directory_socket] == zmq.POLLIN:
            logging.debug('POLLIN')
            key, payload = directory_socket.recv_multipart()
            vegasdata, value = _handle_snapshoter(context, bank, vegasdata, payload)
            if value=="ManagerRestart":
                poller.unregister(data_socket)
                poller.register(vegasdata['socket'], zmq.POLLIN)
                request_pending = False

            logging.debug('get_value returning {}, {}, {}'.format(value, request_pending, vegasdata))
            return value, request_pending, vegasdata
        else:
            logging.debug('ERROR')
            return "Error", request_pending, vegasdata           

    # handle data response
    if data_socket in socks:
        logging.debug('DATA SOCKET message')
        if socks[data_socket] == zmq.POLLIN:
            logging.debug('POLLIN')
            data = _handle_data(data_socket, key)
            if data:
                if key.endswith('Data'):
                    value = data
                else: # state
                    value = data.val_struct[0].val_string[0]
            else:
                value = None

            # indicate we can send a new request next time through loop.
            request_pending = False
            return value, request_pending, vegasdata
        else:
            logging.debug('ERROR')
            return "Error", request_pending, vegasdata           
    
def open_a_socket(context, url, service_type=zmq.REQ):
    socket = context.socket(service_type) # zmq.REQ || zmq.SUB
    socket.linger = 0 # do not wait for more data when closing
    socket.connect(url)
    return socket

def _handle_snapshoter(context, bank, vegasdata, payload):
    # directory service, new interface. If it's ours,
    # need to reconnect.
    reqb = request_protobuf.PBRequestService()
    reqb.ParseFromString(payload)

    # If we're here it's possibly because our device
    # restarted, or name server came back up, or some
    # other service registered with the directory
    # service. If the manager restarted the 'major',
    # 'minor' and 'interface' will mach ours, and the
    # URL will be different, so we need to
    # resubscribe. Check for the snapshot interface.
    # If not, we might respond to a message for the
    # wrong interface, in which case 'vegasdata['url']' will
    # be empty and the connection attempt below will
    # fail.
    logging.warning('SNAPSHOT {}'.format(reqb))

    major, minor = "VEGAS", "Bank{}Mgr".format(bank)
    if (reqb.major == major and
        reqb.minor == minor and
        reqb.interface == dsutils.SERV_SNAPSHOT):

        new_url = _get_tcp_url(reqb.snapshot_url)

        if vegasdata['url'] != new_url:
            restart_msg = "Manager restarted: %s.%s, %s, %s" % \
                          (reqb.major, reqb.minor, reqb.interface, new_url)
            logging.warning('{} {}'.format(datetime.now(), restart_msg))

            vegasdata['url'] = new_url

            if vegasdata['url']:
                logging.warning("new vegasdata['url']: {}".format(vegasdata['url']))
                vegasdata['socket'].close()
                vegasdata['socket'] = open_a_socket(context, vegasdata['url'], zmq.REQ)
                logging.debug('vegasdata', vegasdata)
                return vegasdata, "ManagerRestart"
            else:
                logging.warning("Manager {}.{} subscription "
                                "URL is empty! exiting...".format(major, minor))
    return vegasdata, "NoRestart"
    

def _handle_data(sock, key):
    rl = []
    rl = sock.recv_multipart()

    el = len(rl)

    if el == 1:  # Got an error
        if rl[0] == "E_NOKEY":
            logging.info("No key/value pair found: {}".format(key))
            return None
    elif el > 1:
        # first element is the key
        # the following elements are the values
        if not rl[0].endswith("Data"):
            df = message_protobuf.PBDataField()
            df.ParseFromString(rl[1])
            return df
        else:
            df = vegas_protobuf.pbVegasData()
            df.ParseFromString(rl[1])
            ff = array.array('f') # 'f' is typecode for C float
            ff.fromstring(df.data_blob)
            
            n_sig_states = len(set(df.sig_ref_state))
            n_cal_states = len(set(df.cal_state))
            n_subbands = len(set(df.subband))

            problem = False
            if n_subbands < 1:
                logging.error("Number of sub-bands is: {}".format(n_subbands))
                problem = True
            if n_sig_states < 1:
                logging.error("Number of sig switching stats is: {}".format(n_sig_states))
                problem = True
            if n_cal_states < 1:
                logging.error("Number of cal states is: {}".format(n_cal_states))
                problem = True
            if problem:
                return None

            n_chans, n_samplers, n_states = df.data_dims
            full_res_spectra = np.array(ff)
            
            logging.debug('full_res_spectra {}'.format(full_res_spectra[:10]))
            full_res_spectra = full_res_spectra.reshape(df.data_dims[::-1])
            # estimate the number of polarizations used to grab the first
            # of each subband
            n_pols = (n_samplers/n_subbands)
            logging.debug('polarization estimate: {}'.format(n_pols))

            if n_sig_states == 1:
                # assumes no SIG switching
                # average the cal-on/off pairs
                # this reduces the state dimension by 1/2
                # i.e. 2,14,1024 becomes 1,14,1024 or 14,1024
                arr = np.mean(full_res_spectra, axis=0)
            else:
                logging.debug('SIG SWITCHING')
                # get just the first spectrum
                arr = full_res_spectra[0]

            # get every n_pols spectrum and subband
            less_spectra = arr[::n_pols]
            subbands = df.subband[::n_pols]
            
            try:
                sky_freqs = _sky_frequencies(less_spectra, subbands, df)
            except:
                logging.debug('Frequency information unavailable.  '
                              'Substituting with dummy freq. data.')
                sky_freqs = _make_dummy_frequencies(n_subbands)
            
            # rebin each of the spectra
            sampled_spectra = []
            for xx in less_spectra:
                spectrum = xx
            
                # interpolate over the center channel to remove the VEGAS spike
                centerchan = int(len(spectrum)/2)
                spectrum[centerchan] = (spectrum[(centerchan)-1] + spectrum[(centerchan)+1])/2.
                # rebin to NCHANS length
                logging.debug('raw spectrum length: {}'.format(len(spectrum)))
                # sample every N channels of the raw spectrum, where
                # N = 2 ^ (log2(raw_nchans) - log2(display_nchans))
                N = 2 ** (math.log(len(spectrum),2) - math.log(cfg.NCHANS,2))
                sampled = spectrum[(N/2):len(spectrum)-(N/2)+1:N]
                logging.debug('sampled spectrum length: {}'.format(len(sampled)))
                sampled_spectra.extend(sampled.tolist())
            
            spectrum = np.array(zip(sky_freqs, sampled_spectra))
            spectrum = spectrum.reshape((n_subbands,cfg.NCHANS,2)).tolist()
            
            # sort each spectrum by frequency
            for idx,s in enumerate(spectrum):
                spectrum[idx] = sorted(s)
            
            project = str(df.project_id)
            scan = int(df.scan_number)
            integration = int(df.integration)
            
            response = (project, scan, integration, np.array(spectrum))
            return response
    else:
        return None


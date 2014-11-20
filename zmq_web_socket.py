from server_config import *

from tornado import websocket

import zmq
from zmq.eventloop import zmqstream

from time import strftime, sleep
import threading
import numpy as np
import sys
import json
import logging
import pylab as plt

from vegas_reader import VEGASReader

class ZMQWebSocket(websocket.WebSocketHandler):

    connections = []
    data = None
    server_thread = None
    requesting_data = True
    vegasReader = None

    def query_vegas_managers(self,):
        """Start up the server that reads spectra from the VEGAS manger

        This server reads from the VEGAS manager, as long as there is
        at least one browser connection, and serves it up to
        the display clients.

        """

        logging.debug('querying vegas managers')
        ZMQWebSocket.vegasReader = VEGASReader()

        # continually request data from the VEGAS managers,
        # so long as there is at least one browser connection
        while self.requesting_data:

            all_banks_spectra, metadata = {}, {}
            have_metadata = False

            # request data for each of the banks (A-H)
            for bank in self.vegasReader.banks:

                if bank not in self.vegasReader.active_banks:
                    logging.debug('Bank {} is not active.  '
                                  'Sending empty list to client'.format(bank))
                    spectrum = []

                else:
                    try:
                        # collect some data for the bank
                        response = self.vegasReader.get_data_sample(bank)
                        # structure of response is:
                        #  result_state (e.g. 'ok' 'same' 'error)
                        #  (spectrum, project, scan, integration)
                    except:
                        logging.debug('ERROR getting data sample {}'.format(sys.exc_info()))
                        response = ['error']

                    if response[0] == 'error' or response[0] == 'idle' or response[0] == 'noresponse':
                        logging.debug('{}: recording empty list for {}'.format(response[0], bank))
                        spectrum = []

                    else:
                        spectrum = response[1]

                        # get metadata from the first bank
                        #  the metadata should be the same for all banks
                        if not have_metadata:
                            metadata = response[2]

                            if response[0] == 'same':
                                print 'same, not updating'
                                metadata['update'] = 0
                            else:
                                metadata['update'] = 1

                            if ALWAYS_UPDATE: metadata['update'] = 1

                            have_metadata = True

                all_banks_spectra[bank] = spectrum#np.array(zip(np.array(range(512)),np.random.random(512))).reshape((1,512,2)).tolist()

            # by setting self.data we allow on_message to
            #  write a message back to the client
            ZMQWebSocket.data = [metadata, all_banks_spectra]

            logging.debug(strftime("%H:%M:%S"))
            sleep(2)

    def open(self):
        """
        This method is called when the JS creates a WebSocket object.

        """
        logging.debug('SOCKET OPENED')

        # Start service that reads spectra from manager
        if not self.server_thread:

            logging.info('starting display server')
            ZMQWebSocket.server_thread = threading.Thread(target=self.query_vegas_managers)
            self.server_thread.setDaemon(True)
            self.server_thread.start()
            # give it a second to get started before looking for data
            sleep(1)

        self.connections.append(self)
        logging.info("Client browser socket connections: {}".format(len(self.connections)))

        while True:
            if hasattr(ZMQWebSocket, 'data') and ZMQWebSocket.data:
                metadata, spectra = self.data
                message = {
                    'header': 'data',
                    'body' : {'metadata' : metadata, 'spectra' : spectra}
                }
                print 'message', message['header'],  message['body']['metadata']

                if message['body']:
                    specs = message['body']['spectra']
                    for bank in specs:
                        plt.figure(figsize=(6,2))
                        vals = np.array(specs[bank])
                        for win,dta in enumerate(vals): 
                            plt.plot(dta[:,0]/1e9, dta[:,1])
                        plt.title(bank + " " + strftime("%H:%M:%S"))
                        plt.savefig(bank+'.png')
                        plt.clf()
                    self.write_message(message)

                ZMQWebSocket.data = None
                sleep(2)

    def write_message(self, msg):
        """Send a message to the client.

        This method extends the write_message() method of the
        websocket.WebSocketHandler() base class [using super()] with
        the preamble code that converts the message to unicode, sets
        the message size and records timing information.

        write_message is invoked by the write_message() call in
        get_data_sample() [or socket open() on socket creation?].

        """

        # the following line sends the data to the JS client
        # python 3 syntax would be super().write_message(data)
        print 'sending'
        super(ZMQWebSocket, self).write_message( json.dumps(msg) )

    def on_close(self):
        self.connections.pop()

        if self.connections:
            ZMQWebSocket.requesting_data = False
            self.server_thread.join()

        logging.info("Connections: {}".format(len(self.connections)))

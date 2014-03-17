'''
Created on 08-09-2012

@author: Maciej Wasilak
'''
import struct
import random
import copy
import sys


from twisted.internet.defer import Deferred
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.python import log

import iot.coap as coap
import iot.resource as resource


class Agent():
    """
    Example class which performs single GET request to localhost
    port 5683 (official IANA assigned CoAP port), URI "/other/separate".
    Request is sent 2 seconds after initialization.

    Method requestResource constructs the request message to
    remote endpoint. Then it sends the message using protocol.request().
    A deferred 'd' is returned from this operation.

    Deferred 'd' is fired internally by protocol, when complete response is received.

    Method printResponse is added as a callback to the deferred 'd'. This
    method's main purpose is to act upon received response (here it's simple print).
    """

    def __init__(self, protocol):
        self.protocol = protocol
        reactor.callLater(2, self.requestResource)

    def requestResource(self):
        request = coap.Message(code=coap.POST, payload="-252.6")
        #request.opt.uri_path = ('other', 'separate')
        request.opt.uri_path = ('/1a/temp',)
        request.opt.uri_query = ('98acd7f4dc8dd67cee40462ea623f99c8bc4adf1',)
        request.remote = ("65.49.60.152", coap.COAP_PORT)
        #request.setObserve(self.printLaterResponse)
        d = protocol.request(request)
        #d.addCallback(self.printResponse)
        #d.addErrback(self.noResponse)

    def printResponse(self, response):
        print 'Result: ' + response.payload
        #reactor.stop()

    def printLaterResponse(self, response):
        print 'Newer result: ' + response.payload

    def noResponse(self, failure):
        print 'Failed to fetch resource:'
        print failure
        #reactor.stop()

log.startLogging(sys.stdout)

endpoint = resource.Endpoint(None)
protocol = coap.Coap(endpoint)
client = Agent(protocol)

reactor.listenUDP(61616, protocol)
reactor.run()

#!/usr/bin/env python3

import os.path
import subprocess
import time

RFCOMM = '/dev/rfcomm0'
API_HANDLERS = {
    '0x01': api_unimplemented
}

def p_error ( msg ):
    print('[e]: %s' % msg)

def p_info ( msg ):
    print('[i]: %s' % msg)

def p_warn ( msg ):
    print('[w]: %s' % msg)

def api_unimplemented ( payload ):
    p_info('api unimplemented')
    return ''

if __name__ == '__main__':

    # wait for connection
    while not os.path.exists(RFCOMM):
        time.sleep(1);

    # open device
    with open(RFCOMM, 'r')  as rf_rx:
        # connection established
        print('[i]: connected')

        # we need a separate stream for output
        rf_tx = open(RFCOMM, 'w')

        while True:
            # receive command
            packet = [ord(c) for c in rf_rx.readline().rstrip('\n')]
            print('[p]: %s' % cmd)

            # verify min length
            if len(cmd) < 5:
                p_error('malformed packet')
                continue

            # parse packet
            delim = packet[0]
            length = (packet[1] << 8) + packet[2]
            api = packet[3]
            payload = packet[4:-1]
            checksum = packet[-1]

            # verify delimiter
            if delim != DELIM:
                p_error('invalid delimiter: 0x%x' % delim)
                continue

            # verify length and generate a non-fatal warning on mismatch
            if length != len(packet[3:-1]):
                p_warn('length: expected 0x%x, got 0x%x' % (length, len(packet[3:-1])))

            # calculate and verify checksum and generate fatal error on mismatch
            chk = 0xFF - (sum(packet[3:-1]) & 0xFF)
            if chk != checksum:
                p_error('checksum: expected 0x%x, got 0x%x' % (checksum, chk))
                continue

            # if the API is not supported, generate a fatal error
            if api not in API_HANDLERS:
                p_error('api unsupported: 0x%x' % api)
                continue

            # execute API handler
            p_info('running api: 0x%x' % api)
            tx_payload = API_HANDLERS[api](payload)





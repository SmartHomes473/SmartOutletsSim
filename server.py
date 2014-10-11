#!/usr/bin/env python3
#
# author: Albert Huang <albert@csail.mit.edu>
# modified by: Nick Jugens <njurgens@umich.edu>

"""A python RFCOMM server."""

__license__ = 'GPL-2.0'

from bluetooth import *
import api
import sim.coordinator
import api.smartoutlets

# UUID of Bluetooth Serial Port Profile
uuid = '00001101-0000-1000-8000-00805F9B34FB'
rfcomm_channel = 22

if __name__ == '__main__':
    # initialize the simulator
    simulator = sim.coordinator.Simulator()
    api_parser = api.smartoutlets.APIParser(simulator)

    # set up the Bluetooth server
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(('', rfcomm_channel))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]

    # Register our service
    advertise_service( server_sock, "SampleServer",
            service_id = uuid,
            service_classes = [ uuid, SERIAL_PORT_CLASS ],
            profiles = [ SERIAL_PORT_PROFILE ]
    )

    print('Waiting for connection on RFCOMM channel %d' % port)

    while True:
        client_sock, client_info = server_sock.accept()
        print('Accepted connecton from ', client_info)

        try:
            while True:
                data = client_sock.recv(1024)

                # end of connection
                if len(data) == 0:
                    break

                api_parser.respond(data)

        except IOError:
            pass

        print('disconnected')
        client_sock.close()

    server_sock.close()
    print('all done')

#!/usr/bin/env python3

class APIParser():

    def __init__(self, device_id):
        self.device_id = device_id
        self.packet_handlers = dict()

    def respond(self, packet):
        """Parse a message """

        try:
            # parse packet
            device_id, packet_id, message_id, data_segment = self._parse(packet)
        except IndexError:
            Log.error('malformed header')
            return None

        Log.info('recv: [0x%x 0x%x 0x%x]' % (device_id, packet_id, message_id))

        # verify device ID
        if device_id != self.device_id:
            Log.error('invalid device id 0x%x' % device_id)
            return self.respond_with_error(device_id, packet_id, message_id)

        try:
            packet_handler = self.packet_handlers[packet_id]
        except KeyError:
            return self.respond_with_error(device_id, packet_id, message_id)

        response_id, response = packet_handler(data_segment)

        return self._package(device_id, response_id, message_id, response)

    def _parse(self, packet):
        """Parses a message and returns a tuple containing its components."""
        return (packet[0], packet[1], packet[2], packet[3:])

    def _package(self, device_id, response_id, message_id, response):
        """Constructs a message."""
        packet = [device_id, response_id, message_id] + response

        response_str = " ".join("{:02x}".format(c) for c in response)
        Log.info('send: [0x%x 0x%x 0x%x] [%s]' % (device_id, response_id, message_id, response_str))

        return bytes(packet)

    def respond_with_error(self, device_id, packet_id, message_id):
        """Returns an error message"""
        return self._package(device_id, 0xFF, message_id, [packet_id])


class Log():

    def info(mesg):
        print('[i] ' + mesg)

    def warn(mesg):
        print('[w] ' + mesg)

    def error(mesg):
        print('[e] ' + mesg)

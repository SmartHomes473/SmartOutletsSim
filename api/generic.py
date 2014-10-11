#!/usr/bin/env python3

class APIParser():

    def __init__(self, device_id):
        self.device_id = device_id
        self.packet_handlers = dict()

    def respond(self, message):
        """Parse a message """

        packet = [ord(c) for c in message]

        # parse packet
        device_id, packet_id, message_id, data_segment = self._parse(message)

        # verify device ID
        if device_id != self.device_id:
            return respond_with_error(device_id, packet_id, message_id)

        try:
            packet_handler = self.packet_handlers[packet_id]
        except KeyError:
            return respond_with_error(device_id, packet_id, message_id)

        response_id, response = packet_handler(data_segment)

        return _package(device_id, response_id, message_id, response)

    def _parse(self, message):
        """Parses a message and returns a tuple containing its components."""
        return (packet[0], packet[1], packet[2], packet[3:])

    def _package(self, device_id, response_id, message_id, response):
        """Constructs a message."""
        return list(device_id, response_id, message_id).extend(response)

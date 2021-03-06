#!/usr/bin/env python3

from . import generic

# Device ID
SMART_OUTLETS_ID = 0x03

# Request IDs
REQ_OUTLETS = 0x00
REQ_POWER_STATS = 0x01
REQ_SCHEDULE = 0x02
SET_POWER_STATE = 0x03
SCHEDULE_TASKS = 0x04
UNSCHEDULE_TASKS = 0x05

# Response IDs
ACK = 0x80
RESP_OUTLETS = 0x81
RESP_POWER_STATS = 0x82
RESP_SCHEDULE = 0x84

class APIParser(generic.APIParser):

    def __init__(self, server):
        super(APIParser, self).__init__(SMART_OUTLETS_ID)

        self.server = server

        # maps message types to their responses
        self.packet_handlers = {
            REQ_OUTLETS: self._resp_outlets,
            REQ_POWER_STATS: self._resp_power_stats,
            REQ_SCHEDULE: self._req_schedule,
            SET_POWER_STATE: self._resp_power_state,
            SCHEDULE_TASKS: self._schedule_tasks,
            UNSCHEDULE_TASKS: self._unschedule_tasks
        }

    def _resp_outlets(self, data_segment):
        # extract outlets from list and mask off the power state bit
        requested_outlets = [outlet & 0x7F for outlet in data_segment[1:]]

        outlet_info = self.server.outletInfo(requested_outlets)

        # construct the response data segment
        response = []
        response.append(len(outlet_info))
        for outlet in outlet_info:
            entry = outlet.getId() | (0x80 if outlet.isPowered() else 0x0)
            response.append(entry)

        return RESP_OUTLETS, response

    def _resp_power_stats(self, data_segment):
        # extract outlets from list and mask off the power state bit
        requested_outlets = [outlet & 0x7F for outlet in data_segment[1:]]

        outlet_info = self.server.outletInfo(requested_outlets)

        # construct the response data segment
        response = []
        response.append(len(outlet_info))
        for outlet in outlet_info:
            outlet_id = outlet.getId() | (0x80 if outlet.isPowered() else 0x0)
            response.append(outlet_id)
            power_msb, power_lsb = outlet.getPower()
            response.append(power_msb)
            response.append(power_lsb)

        return RESP_POWER_STATS, response

    def _req_schedule(self, data_segment):
        pass

    def _resp_power_state(self, data_segment):
        # Right now we only support operating on one outlet
        oid = data_segment[0] & 0x7F
        powered = data_segment[0] != oid

        print('[a] setting outlet %i to %s' % (oid, 'ON' if powered else 'OFF'))

        self.server.setOutletPower([(oid, powered)])
        return self._resp_ack()

    def _schedule_tasks(self, data_segment):
        pass

    def _unschedule_tasks(self, data_segment):
        pass

    def _resp_ack(self):
        return ACK, []

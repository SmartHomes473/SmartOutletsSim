#!/usr/bin/env python3

from . import generic


# Request IDs
REQ_OUTLETS = 0x00
REQ_POWER_STATS = 0x01
REQ_SCHEDULE = 0x02
SET_POWER_STATE = 0x03
SCHEDULE_TASKS = 0x04
UNSCHEDULE_TASKS = 0x05

class APIParser(generic.APIParser):

    def __init__(self, server):
        super(APIParser, self).__init__(0x03)

        self.server = server

        # maps message types to their responses
        self.packet_handlers = {
            REQ_OUTLETS: self._resp_outlets,
            REQ_POWER_STATS: self._req_power_stats,
            REQ_SCHEDULE: self._req_schedule,
            SET_POWER_STATE: self._set_power_state,
            SCHEDULE_TASKS: self._schedule_tasks,
            UNSCHEDULE_TASKS: self._unschedule_tasks
        }

    def _resp_outlets(self, data_segment):
        # extract outlets from list and mask off the power state bit
        requested_outlets = [outlet & 0x7F for outlet in data_segment[1:]]

        outlet_info = self.server.outletInfo(requested_outlets)

        # construct the response data segment
        response = []
        response[0] = len(outlet_info)
        for outlet in outlet_info:
            entry = outlet.getID() | 0x80 if outlet.isPowered() else 0x0
            response.append(entry)

        return response

    def _req_power_stats(self, data_segment):
        pass

    def _req_schedule(self, data_segment):
        pass

    def _set_power_state(self, data_segment):
        pass

    def _schedule_tasks(self, data_segment):
        pass

    def _unschedule_tasks(self, data_segment):
        pass

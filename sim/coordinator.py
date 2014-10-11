#!/usr/bin/env python3

import copy

class Simulator():

    def __init__(self):
        self.outlets = { }

    def outletInfo(self, outlets):
        outlet_info = []

        for outlet in outlets:
            # check if we know about the outlet
            if outlet in self.outlets:
                # clone the outlet into the output
                outlet_info.append(self.outlets[outlet].clone())

        return outlet_info

class Outlet():

    def __init__(self, oid, powered):
        self.oid = oid
        self.powered = powered

    def getId(self):
        return self.oid

    def isPowered(self):
        return self.powered

    def clone(self):
        return Outlet(self.oid, self.powered)

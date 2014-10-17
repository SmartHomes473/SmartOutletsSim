#!/usr/bin/env python3

import copy

class Simulator():

    def __init__(self):
        self.outlets = { }

    def outletInfo(self, outlets=[]):
        outlet_info = []

        if len(outlets) == 0:
            outlets = self.outlets

        for outlet in outlets:
            # check if we know about the outlet
            if outlet in self.outlets:
                # clone the outlet into the output
                outlet_info.append(self.outlets[outlet].clone())

        return outlet_info

    def registerOutlets(self, outlets_ids):
        """Add outlets to the simulator."""
        for oid in outlets_ids:
            self.outlets[oid] = Outlet(oid, False, 0)

    def setOutletPower(self, outlets):
        """Sets the power state for a list of outlets."""
        for oid, powered in outlets:
            self.outlets[oid].setPowered(powered)

    def listOutlets(self):
        """Return a list of IDs for each outlet"""
        return [self.outlets[outlet].getId() for outlet in self.outlets]

class Outlet():

    def __init__(self, oid, powered, power):
        self.oid = oid
        self.powered = powered
        self.power = power

    def getId(self):
        return self.oid

    def isPowered(self):
        return self.powered

    def setPowered(self, powered):
        self.powered = True if powered else False

    def getPower(self):
        msb = (self.power >> 8) & 0xFF
        lsb = self.power & 0xFF
        return msb, lsb

    def clone(self):
        return Outlet(self.oid, self.powered, self.power)

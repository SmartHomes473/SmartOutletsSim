#!/usr/bin/env python3

import copy

class Simulator():

    def __init__(self):
        self.outlets = { }

    def outletInfo(self, outlets=None):
        outlet_info = []

        if outlets == None:
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
            self.outlets[oid] = Outlet(oid, False)

    def setOutletPower(self, outlets):
        """Sets the power state for a list of outlets."""
        for oid, powered in outlets:
            self.outlets[oid].setPowered(powered)

    def listOutlets(self):
        """Return a list of IDs for each outlet"""
        return [self.outlets[outlet].getId() for outlet in self.outlets]

class Outlet():

    def __init__(self, oid, powered):
        self.oid = oid
        self.powered = powered

    def getId(self):
        return self.oid

    def isPowered(self):
        return self.powered

    def setPowered(self, powered):
        self.powered = True if powered else False

    def clone(self):
        return Outlet(self.oid, self.powered)

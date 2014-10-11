#!/usr/bin/env python3

import unittest
from sim.coordinator import Simulator as CoordinatorSim

class TestOutletFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_adding_outlets(self):
        sim = CoordinatorSim()
        outlets = range(0, 10)

        # add a set of outlets
        sim.registerOutlets(outlets)
        self.assertCountEqual(outlets, sim.listOutlets())

        # add a second set of outlets
        sim.registerOutlets(range(10, 20))
        outlets = range(0, 20)
        self.assertCountEqual(outlets, sim.listOutlets())


    def test_fetch_all_outlet_info(self):
        sim = CoordinatorSim()
        outlets = range(0, 10)

        # add a set of outlets
        sim.registerOutlets(outlets)

        # all outlets should be powered off
        info = sim.outletInfo()

        # check we returned ALL outlets
        info_ids = [outlet.getId() for outlet in info]
        self.assertCountEqual(outlets, info_ids)

        # verify all outlets are powered off
        for outlet in info:
            self.assertEqual(outlet.isPowered(), False)

    def test_set_single_outlet_power(self):
        sim = CoordinatorSim()
        outlets = range(0, 10)

        # register outlets with simulator
        sim.registerOutlets(outlets)

        # fetch info for outlet 5
        oid = 5
        info = sim.outletInfo([oid])

        # excpect one result
        self.assertEqual(len(info), 1)

        outlet = info[0]
        self.assertEqual(outlet.getId(), oid)
        self.assertEqual(outlet.isPowered(), False)

        # set power state to ON
        update_state = (oid, True)
        sim.setOutletPower([update_state])

        # fetch updated info for outlet 5
        info = sim.outletInfo([oid])

        # excpect one result
        self.assertEqual(len(info), 1)

        outlet = info[0]
        self.assertEqual(outlet.getId(), oid)
        self.assertEqual(outlet.isPowered(), True)

    def test_set_multiple_outlet_power(self):
        sim = CoordinatorSim()
        on_outlets = range(0, 10)
        off_outlets = range(10, 20)

        # register outlets with simulator
        sim.registerOutlets(on_outlets)
        sim.registerOutlets(off_outlets)

        # fetch info for on outlets
        info = sim.outletInfo(on_outlets)

        # expect 10 results
        self.assertEqual(len(info), len(on_outlets))

        # set power states to on
        update_state = [(outlet, True) for outlet in on_outlets]
        sim.setOutletPower(update_state)

        # fetch updated infor for on outlets
        info = sim.outletInfo(on_outlets)

        # expect 10 results
        self.assertEqual(len(info), len(on_outlets))

        # verify they are all on
        for outlet in info:
            self.assertEqual(outlet.isPowered(), True)

        # fetch info for the off outlets to make sure none were
        # turned on.
        info = sim.outletInfo(off_outlets)
        self.assertEqual(len(info), len(off_outlets))
        for outlet in info:
            self.assertEqual(outlet.isPowered(), False)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3

import unittest
import random
from sim.coordinator import Outlet as Outlet

class TestOutletFunctions(unittest.TestCase):

    def setUp(self):
        self.outlet_id = random.getrandbits(8)

    def test_outlet_id(self):
        outlet = Outlet(self.outlet_id, False)
        self.assertEqual(self.outlet_id, outlet.getId())

    def test_outlet_initial_state(self):
        outlet = Outlet(self.outlet_id, False)
        self.assertEqual(outlet.isPowered(), False)

        outlet = Outlet(self.outlet_id, True)
        self.assertEqual(outlet.isPowered(), True)

    def test_outlet_set_power(self):
        outlet = Outlet(self.outlet_id, False)

        outlet.setPowered(True)
        self.assertEqual(outlet.isPowered(), True)

        outlet.setPowered(False)
        self.assertEqual(outlet.isPowered(), False)

if __name__ == '__main__':
    unittest.main()

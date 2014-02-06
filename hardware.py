#!/usr/bin/env python
from datetime import date

# Simple class to represent a piece of hardware
class hw:
    def __init__(self, name, d, hashes, price, power):
        self.name = name
        self.date = d
        self.hashes = hashes
        self.price = price
        self.power = power

        self.hash_efficiency = hashes / price
        self.power_efficiency = hashes / power
        self.total_units = 0
        self.embodied_energy = 0
        self.on = True

    def new_cap(self, capacity, embodied_energy_per_rig):
        new_units = capacity / self.hashes
        self.total_units += new_units
        self.embodied_energy += embodied_energy_per_rig * new_units


    def running(self, start, end, network_hashrate, usd_prices, electricity_price):
        # Assume that a rig is turned off it fails to cover its power costs for
        # an entire generation of hardware.  This assumes miners are slightly
        # bullish about the future price of BTC, which fits their psychology
        # and is rational given BTC's deflationary monetary policy algorithm

        proportion = self.hashes / network_hashrate
        for (d,btc_price) in usd_prices:
            if d >= start and d <= end:
                payoff = 144. * 25 * btc_price
                unit_payoff = proportion * btc_price
                on = (unit_payoff / self.power) > electricity_price
                #print self.name, "pays", unit_payoff * 3600 * 24, "/day and is", on ,
                #print (unit_payoff / self.power), "dollars per joule"
                if on:
                    # The rig paid or its electicity this period, so it will
                    # keep running until new hardware is out
                    if not self.on:
                        print self.name, "HAS TURNED BACK ON"
                        self.on = True
                    return True
        if self.on: 
            print self.name, "now off (%f%% of network)" % (proportion * self.total_units * 100), "unit payoff", unit_payoff *3600* 24, "/day"
            self.on = False
        return False

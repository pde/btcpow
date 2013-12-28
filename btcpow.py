#!/usr/bin/env python
from datetime import date
import json

print date.fromtimestamp(0)

# Unit conversions
MH = MW = 1000000
GH = GW = 1000 * MH
TH = TW = 1000 * GH
PH = PW = 1000 * TH

# Read in historical data on BTC price and network hash rate
# Latest data can be fetched from https://blockchain.info/stats 

capacities, usd_prices = {}, {}
with open('data/hash_rate.json', 'r') as f:
  capacities = [(date.fromtimestamp(x['x']),
                   x['y'] * GH)
                   for x in json.load(f)['values']]

with open('data/price.json', 'r') as f:
  usd_prices = [(date.fromtimestamp(x['x']),
                   x['y'])
                   for x in json.load(f)['values']]

#Electricity prices, converted from quoted USD per kWh to USD per J
conversion_factor = 1.0/(1000*60*60)
ind_electricity_price = 0.06 * conversion_factor #USD per J
res_electricity_price = 0.10 * conversion_factor #USD per J

# Epochs of best mining hardware

# List of:
# (name, date introduced, hashes / sec, power consumption)
# picking some of the more popular entries from https://en.bitcoin.it/wiki/Mining_hardware_comparison
# Taking best-case hashrates but excluding strong outliers (probably a more accurate model would
# track the optimisation of use of a particular piece of hardware over time
# Radeon intoduction dates from Wikipedia;
# FPGA introduction dates from 
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
        self.on = True

    def new_cap(self, capacity):
        new_units = capacity / self.hashes
        self.total_units += new_units

    def running(self, start, end, network_hashrate):
        # Assume that a rig is turned off it fails to cover its power costs for
        # an entire generation of hardware.  This assumes miners are slightly
        # bullish about the future price of BTC, which fits their psychology
        # and is rational given BTC's deflationary monetary policy algorithm

        proportion = self.hashes / network_hashrate
        for (d,price) in usd_prices:
            if d >= start and d <= end:
                payoff = 144. * 25 * price
                unit_payoff = proportion * price
                on = (unit_payoff / self.power) > ind_electricity_price
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
        
hardware = [
  hw("Radeon 4350", date(2008,9,30), 10.7 * MH, 20, 40),
  hw("Radeon 4870", date(2008,6,25), 112 * MH, 140, 135),
  hw("Radeon 5770", date(2009,10,13), 244 * MH, 108, 160),
  hw("Radeon 6870", date(2010,10,22), 330 * MH, 170, 240),
  hw("Bitcoin Dominator X5000", date(2011,8,18), 100 * MH, 6.8, 440),
  hw("Radeon 7970", date(2012,1,9), 710 * MH, 250, 420),
  hw("Butterfly Labs mini-rig FPGA", date(2012,4,8), 25.2 * GH, 1250, 15300),
  hw("Avalon ASIC #1", date(2013, 2,1), 66.3 *GH, 620, 1300),
  hw("Block Erupter blade", date(2013,4,1),10.7 * GH, 83, 350),
  hw("KNC Saturn", date(2013,10,3), 200 * GH, 320, 3000)
]

def standard_model():
    h_available = []
    for pos, h in enumerate(hardware):
        h_available.append(h)
        print h.name, "available", h.date
        best = max([gen.hash_efficiency for gen in h_available])
        print "best", best
        # MODEL: anything that's not more than ten times worse than the best hardware (hash/$)
        # will still be getting some deployment, but at a fraction proportional only to its "quality"
        for gen in h_available:
            gen.quality = gen.hash_efficiency / best
        plausible = [gen for gen in h_available if gen.hash_efficiency > (best / 10.)]
        total_q = sum([gen.quality for gen in plausible])

        prev_hashrate = 0
        for pos2, (when, hashrate) in enumerate(capacities):
            
            # iterate from the start of this hardware epoch
            if when < h.date: 
                prev_hashate = hashrate
                continue
            # until the end
            try: 
                if when > hardware[pos+1].date: break
            except: 
                pass  # fencepost
            
            
            new_hashing = hashrate - prev_hashrate
            if new_hashing < 0:
                # SIMPLIFY: skip forward in time until there is actual growth
                continue

            #print "incremental hashrate", new_hashing, "(%d plausible rigs)" % len(plausible)
            
            for gen in plausible:
                # each piece of plausible hardware is turned on with a capacity
                # equal to its proportion of the total quality
                gen.new_cap(new_hashing * (gen.quality / total_q))
            
         
            # without turning anything off yet...
            try: when_next = capacities[pos2 + 1][0]
            except: when_next = when # end of series
            burn_rate = sum([gen.total_units * gen.power for gen in h_available if gen.running(when, when_next, hashrate)])
            print when, burn_rate / MW, "MW"
        
            prev_hashrate = hashrate

standard_model()

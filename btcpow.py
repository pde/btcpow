#!/usr/bin/env python
from datetime import date
import json

print date.fromtimestamp(0)

# TIME SERIES INPUTS
MH = MW = 1000000
GH = GW = 1000 * MH
TH = TW = 1000 * GH
PH = PW = 1000 * TH

capacities, usd_prices = {}

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
res_electricity_price = 0.10 #USD per J

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
  def new_cap(self, capacity):
    new_units = capacity / self.hashes
    self.total_units += new_units
        
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
<<<<<<< HEAD
  h_available = []
  for pos, h in enumerate(hardware):
    h_available.append(h)
    best = max([gen.hash_efficiency for gen in h_available])
    print "best", best
    # MODEL: anything that's not more than ten times worse than the best hardware (hash/$)
    # will still be getting some deployment, but at a fraction proportional only to its "quality"
    for gen in h_available:
      gen.quality = gen.hash_efficiency / best
    plausible = [gen for gen in h_available if gen.hash_efficiency > (best / 10.)]
    total_q = sum([gen.quality for gen in plausible])

    prev_hashrate = 0
    for when, hashrate in capacities:
      
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

    print "incremental hashrate", new_hashing, "(%d plausible rigs)" % len(plausible)
      
      for gen in plausible:
        # each piece of plausible hardware is turned on with a capacity
        # equal to its proportion of the total quality
        gen.new_cap(new_hashing * (gen.quality / total_q))
      
     
      # without turning anything off yet...
      burn_rate = sum([gen.total_units * gen.power for gen in h_available])
      print when, burn_rate / MW, "MW"

standard_model()

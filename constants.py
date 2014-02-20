#!/usr/bin/env python

from hardware import hw
from datetime import date
import json

# Unit conversions
MJ = MH = MW = 1000000
GJ = GH = GW = 1000 * MH
TJ = TH = TW = 1000 * GH
PJ = PH = PW = 1000 * TH

# Electricity prices, converted from quoted USD per kWh to USD per J
# We could later replace this with changes over time, though variance in location
# is far greater than variance over time
conversion_factor = 1.0/(1000*60*60)
ind_electricity_price = 0.06 * conversion_factor # USD per J
res_electricity_price = 0.10 * conversion_factor # USD per J

# Embodied energy estimate from:
# http://www.aceee.org/files/proceedings/2012/data/papers/0193-000301.pdf
# Rigs vary in their character from large desktop-PC style devices to
# much smaller units; we pick a laptop emobdied energy minus an LCD as
# a representative estimate
embodied_energy_per_rig = (4790 - 1233) * MJ

#Read in data from JSON, smooth it by averaging data in bins, and apply a transformation func
def read_data(filename, func=lambda x,y: (x, y), bin_size=1):
  new_data = []
  with open(filename, 'r') as f:
    data = json.load(f)['values']
    while len(data) > 0:
      next_bin_size = min(bin_size, len(data))
      new_data.append(func(sum([x['x'] for x in data[:bin_size]]) / float(next_bin_size),
                           sum([x['y'] for x in data[:bin_size]]) / float(next_bin_size)))
      data = data[bin_size:]
  return new_data

# Read in historical data on BTC price and network hash rate
bin_size = 10
capacities = read_data('data/hash_rate.json', lambda x,y: (date.fromtimestamp(x), y * GH), bin_size)
usd_prices = read_data('data/price.json', lambda x,y: (date.fromtimestamp(x), y), bin_size)

# List of:
# (name, date introduced, hashes / sec, power consumption)
# picking some of the more popular entries from https://en.bitcoin.it/wiki/Mining_hardware_comparison
# Taking best-case hashrates but excluding strong outliers (probably a more accurate model would
# track the optimisation of use of a particular piece of hardware over time
# Radeon intoduction dates from Wikipedia;
# FPGA introduction dates from 
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

# This could be extended for all future rewards
block_rewards = [
  (date(2009,01,01), 50.0),
  (date(2012,01,01), 25.0),
  (date(2017,01,01), 12.5),
]

genesis_date = date(2009,01,01)


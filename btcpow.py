#!/usr/bin/env python
from datetime import date

print date.fromtimestamp(0)

# TIME SERIES INPUTS
MH = MW = 1000000
GH = GW = 1000 * MH
TH = TW = 1000 * GH
PH = PW = 1000 * TH

#HISTORICAL NETWORK HASH RATE (blockchain.info)
data = [
     (1357107305, 22958.37364207791),
    (1357971305, 21696.36194810485),
    (1358835305, 21662.447876690152),
    (1359699305, 24228.992664876263),
    (1360563305, 25286.602571202566),
    (1361427305, 31133.761880168673),
    (1362291305, 33463.367148424295),
    (1363155305, 38510.37733654069),
    (1364019305, 50559.4545672301),
    (1364883305, 58998.98230185833),
    (1365747305, 64270.43179056337),
    (1366611305, 71422.95940925334),
    (1367475305, 75312.19284197057),
    (1368365225, 86544.25801956786),
    (1369289705, 90403.83802229879),
    (1370153705, 120463.78349218788),
    (1371017705, 138085.31708232762),
    (1371881705, 151125.75162434127),
    (1372745705, 174758.09293056282),
    (1373609705, 209850.27834491036),
    (1374473705, 239381.35399752203),
    (1375389545, 301823.5877760969),
    (1376391785, 412783.2605573256),
    (1377324905, 521157.07305177033),
    (1378344425, 716929.8311090792),
    (1379225705, 931116.0573862279),
    (1380089705, 1230164.417991475),
    (1380953705, 1488956.2104355616),
    (1381817705, 2278372.956066019),
    (1382681705, 3148414.510056981),
    (1383545705, 3818282.206791638),
    (1384409705, 4662804.636600295),
    (1385273705, 5023333.516734963),
    (1386137705, 6410662.717894249),
    (1387001705, 8221990.13533961),
    (1387823145, 9800440.160946507)]

capacities = [(date.fromtimestamp(ts), rate * GH) for (ts,rate) in data]

#HISTORICAL EXCHANGE RATE DATA (blockchain.info)
data = [   
    (1357107305, 13.547272999999999),
    (1357971305, 14.199774999999999),
    (1358835305, 17.091099),
    (1359699305, 20.229999),
    (1360563305, 23.827327999999998),
    (1361427305, 28.676488),
    (1362291305, 35.654864999999994),
    (1363155305, 45.972775),
    (1364019305, 66.291985),
    (1364883305, 109.784688),
    (1365747305, 144.83650599999999),
    (1366611305, 122.197318),
    (1367475305, 121.999054),
    (1368365225, 114.402251),
    (1369289705, 126.485916),
    (1370153705, 125.088434),
    (1371017705, 105.180854),
    (1371881705, 106.490308),
    (1372745705, 88.817518),
    (1373609705, 86.37360000000001),
    (1374473705, 93.32941100000001),
    (1375389545, 102.50322700000001),
    (1376391785, 107.836195),
    (1377324905, 122.20741299999997),
    (1378344425, 135.74866100000003),
    (1379225705, 138.481626),
    (1380089705, 136.253562),
    (1380953705, 135.751742),
    (1381817705, 151.702516),
    (1382681705, 197.99597899999998),
    (1383545705, 241.02648100000002),
    (1384409705, 418.986333),
    (1385273705, 802.8146669999999),
    (1386137705, 1044.352163),
    (1387001705, 858.2592950000001),
    (1387823145, 697.1547822222224)]

usd_prices = [(date.fromtimestamp(ts), price) for (ts,price) in data]

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
        
        prev_hashrate = hashrate

standard_model()

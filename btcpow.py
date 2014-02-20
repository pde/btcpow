#!/usr/bin/env python
from datetime import date

# local files
from constants import *

def standard_model():
    h_available = []
    # Iterate over the epochs when new hardware becomes available
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
        prev_embodied = 0
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
                gen.new_cap(new_hashing * (gen.quality / total_q), embodied_energy_per_rig)
            
         
            # without turning anything off yet...
            try: when_next = capacities[pos2 + 1][0]
            except: when_next = when # end of series
            burn_rate = sum([gen.total_units * gen.power for gen in h_available if gen.running(when, when_next, hashrate, usd_prices, ind_electricity_price)])
            print when, burn_rate / MW, "MW consumed",

            # Include embodied energy in the calculation
            embodied = sum([gen.embodied_energy for gen in h_available])
            elapsed = (when_next - when).total_seconds() # timedelta objects
            if elapsed:
              newly_embodied = ((embodied - prev_embodied) / elapsed) 
              print newly_embodied / MW, "MW embodied in new hardware"
              burn_rate += newly_embodied
            else:
              # use the previous estimate 
              print "~", newly_embodied / MW, "MW newly embodied"
              burn_rate += newly_embodied 

            print "Total energy consumption rate:", burn_rate / MW,  "MW"

            prev_hashrate = hashrate
            prev_embodied = embodied

standard_model()

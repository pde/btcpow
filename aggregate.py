#!/usr/bin/env python
from datetime import date
import math

# local files
from constants import *

total_work = 0
total_reward = 0

start_date = genesis_date
end_date = date.today()

for i in xrange(len(capacities) - 1):
  t1, r1 = capacities[i]
  t2, r2 = capacities[i + 1]

  t = (t2 - t1).total_seconds()
  r = (r1 + r2) / 2 #trapezoidal interpolation

  total_work += t * r

reward_index = 0
for i in xrange(len(usd_prices) - 1):
  t1, r1 = usd_prices[i]
  t2, r2 = usd_prices[i + 1]

  reward = block_rewards[reward_index][1]
  if t2 > block_rewards[reward_index + 1][0]:
    reward_index += 1
    d1 = (block_rewards[reward_index][0] - t1).total_seconds()
    d2 = (t2 - block_rewards[reward_index][0]).total_seconds()
    reward = (block_rewards[reward_index - 1][1] * d1)/(d1 + d2) + (block_rewards[reward_index ][1] * d2)/(d1 + d2)

  t = (t2 - t1).total_seconds() / (60 * 10)
  r = (r1 + r2) / 2 #trapezoidal interpolation
  
 
  total_reward += r * t * reward

start_date = max(start_date, genesis_date)
end_date = min(end_date, capacities[-1][0])

print "Aggregate Bitcoin network from %s to %s:" % (start_date, end_date)
print "\t2^%2f hashes computed" % (math.log(total_work, 2))
print "\t%.1f M US$ earned" % (total_reward / MH)

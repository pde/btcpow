#!/usr/bin/env python
from datetime import date, timedelta
import math

# local files
from constants import *

def compute_total_work(start_date, end_date):
  total_work = 0
  for i in xrange(len(capacities) - 1):
    t1, r1 = capacities[i]
    t2, r2 = capacities[i + 1]

    t1 = max(start_date, t1)
    t2 = min(end_date, t2)
    if t1 > t2: continue

    t = (t2 - t1).total_seconds()
    r = (r1 + r2) / 2 #trapezoidal interpolation

    total_work += t * r

  return total_work

def compute_total_reward(start_date, end_date):
  total_reward = 0
  reward_index = 0
  for i in xrange(len(usd_prices) - 1):
    t1, r1 = usd_prices[i]
    t2, r2 = usd_prices[i + 1]

    t1 = max(start_date, t1)
    t2 = min(end_date, t2)
    if t1 > t2: continue

    while t1 > block_rewards[reward_index + 1][0]:
      reward_index += 1

    reward = block_rewards[reward_index][1]
    if t2 > block_rewards[reward_index + 1][0]:
      reward_index += 1
      d1 = (block_rewards[reward_index][0] - t1).total_seconds()
      d2 = (t2 - block_rewards[reward_index][0]).total_seconds()
      reward = (block_rewards[reward_index - 1][1] * d1)/(d1 + d2) + (block_rewards[reward_index ][1] * d2)/(d1 + d2)

    t = (t2 - t1).total_seconds() / (60 * 10) #block frequency
    r = (r1 + r2) / 2 #trapezoidal interpolation
    
    total_reward += r * t * reward

  return total_reward


date_ranges = [(genesis_date, date.today())]

extended_ranges = []
d = date(2013, 01, 01)
while d < date.today():
  extended_ranges.append((d, date.today()))
  d += timedelta(days = 30)
  
#date_ranges += extended_ranges

date_ranges += [(date(2013,01,01), date(2013,12,31))]
date_ranges += [(date(2014,01,01), date(2014,07,01))]

for (s, e) in date_ranges:

  s = max(s, genesis_date)
  e = min(e, capacities[-1][0])

  print "Aggregate Bitcoin network from %s to %s:" % (s, e)
  print "\t2^%.3f hashes computed" % (math.log(compute_total_work(s, e), 2))
  print "\t%.1f M US$ earned" % (compute_total_reward(s, e) / MH)

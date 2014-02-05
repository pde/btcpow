#!/bin/sh

curl 'http://blockchain.info/charts/hash-rate?showDataPoints=false&timespan=all&show_header=true&daysAverageString=1&scale=0&format=json&address=' -o 'hash_rate.json'
curl 'http://blockchain.info/charts/market-price?showDataPoints=false&timespan=all&show_header=true&daysAverageString=1&scale=0&format=json&address=' -o 'price.json'


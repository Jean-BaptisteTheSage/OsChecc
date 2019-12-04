import nmap
import netifaces as ni
from os import system as sys
from collections import defaultdict
import requests as r
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-v', action='store_true', help='get information verbose')
parser.add_argument('-d', action='store_true', help='debug nmap call')
parser.add_argument('--targ', action='append', help='run on only targeted IP address')
parser.add_argument('--vuln', action='store_true', help='checks for vulnerabilities on device')
args = parser.parse_args()



inet_addr_fam = ni.AF_INET
aflink = ni.AF_LINK
interface = []

separator = lambda: print('################\n')


def getNetworkInterfaces():
    ifs = []
    for i in ni.interfaces():
        tmp = ni.ifaddresses(i)
        # second check is to clear out localhost information
        if inet_addr_fam in tmp and tmp[aflink][0]['addr'] != '':
            ifs.append(tmp)

    return ifs

interface = getNetworkInterfaces()

###############################################################################

verbose = '-v '
debug = '-d '
vuln = '-sC '
writer = '-oN ip.txt '
ps4 = "10.68.234.0"
laptop = "10.66.79.2"
iphone = "10.66.243.234"

# form the subnet mask modify ip addresses to search for a class C network
buildNetwork = lambda x: x + '/24'
targ = args.targ[0] if args.targ else buildNetwork(interface[-1][inet_addr_fam][0]['addr'])

query = '-O '
if args.d:
    query += debug

if args.vuln:
    query += vuln

if args.v:
    query += verbose

###############################################################################

nm = nmap.PortScanner()
nm.scan(targ, arguments='-O ' + writer)
print(nm.csv())

osGuess = defaultdict(list)
cons = 'Running'
aggy = 'Aggressive OS guesses'
detected = False

with open('ip.txt') as f:
    for line in f:
        if cons in line:
            detected = True
            osGuess['conservative'] = line.rstrip()[line.find(':') + 2: ].split(', ')

        if aggy in line:
            detected = True
            osGuess['aggressive'] = line.rstrip()[len(aggy) + 2:].split(', ')

def printer(line):
    for i in line:
        print(i, '\n')
        separator()


def checkLatest():
    isOld = 'asdf'

    print('General guesses: \n\n')
    print('================\n')
    printer(osGuess['conservative'])
    print('================\n\n')

    print('Detailed guess: \n\n')
    print('================\n')
    printer(osGuess['aggressive'])
    print('================\n\n')
    
    return isOld

def handleFailure():
    print('OS detection failed')

separator()
checkLatest() if detected else handleFailure()

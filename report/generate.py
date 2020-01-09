#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Simple and trivial program generating lines in stdout
        each lines contain :
            an incremental id (int)
            a key1 in tabkey1 (int)
            a key2 in tabkey2 (int)
            a key3 in tabkey3 (int)
            an amount in range -10000. +10000 (double)
            separator is blank

    standalone program
    ------------------

    parameters
    ---------
    num: int
        number of line in stdout (a positive integer)
'''

import sys
import random
import argparse

_key1s = ['000',
          '001',
          '002',
          '050',
          '060',
          '070',
          '075',
          '080',
          '125',
          '354',
          '452',
          '552'
         ]

_key2s = ['010',
          '020',
          '030',
          '040',
          '050',
          '060',
          '070',
          '080',
          '090',
          '100',
          '110',
          '120'
         ]

_key3s = ['050',
          '075',
          '100',
          '125',
          '150',
          '175',
          '200',
          '225',
          '250',
          '275',
          '300',
          '325',
          '350',
          '375',
          '400'
         ]

def main(num=5000):

    '''
        Trivial program generating randomly an incremental Id, 3 keys and an amount
    '''

    random.seed()

    for i in range(num):

        key1 = _key1s[random.randint(0, len(_key1s)-1)]
        key2 = _key2s[random.randint(0, len(_key2s)-1)]
        key3 = _key3s[random.randint(0, len(_key3s)-1)]

        mnt = random.uniform(-10000., 10000.)

        print(i, key1, key2, key3, mnt)

    return 0

if __name__ == '__main__':

    # argparse: standard command line parser
    parser = argparse.ArgumentParser(description='Generate randomly in stdout\
        an incremental Id, 3 keys and a float NUM times')
    parser.add_argument('--num', default=5000, type=int, help='num must be a positive integer')
    args = parser.parse_args()

    status = 1
    if args.num > 0:
        status = main(args.num)
    else:
        print('num args null or negative')
        print('program stopped')

    sys.exit(status)

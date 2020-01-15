#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Demonstration program split a file in one path in multiple file

    standalone program
    ------------------
    output produces :
        files gem-key1-key2-key3.txt

    parameters
    ---------
    gem: header for the name of ouput files,
    file: a file or stdin
        each lines of file contain :
            an incremental id
            a key1 in tabkey1
            a key2 in tabkey2
            a key3 in tabkey3
            an amount in range -10000. +10000
            separator : blank
    example : 0 050 050 075 8532.45398608017
'''

import sys
import argparse
from datetime import datetime

def main(gem, streamin):

    """
        reporting program
    """

    # init global var
    # datas from stream
    newid = ''
    newkey1 = ''
    newkey2 = ''
    newkey3 = ''
    newmnt = ''
    # datas from stream
    oldid = ''
    oldkey1 = ''
    oldkey2 = ''
    oldkey3 = ''
    oldmnt = ''

    # last mouvement for key init at True
    lmvkey = True
    # first mouvement for key, first mouvement is the previous last mouvement
    fmvkey = True

    # end of file
    feof = False

    # we maintain a record counter per key and a total record counter
    nbenrread = 0
    nbenrwrite = 0
    nbenrkey = 0
    nbfiles = 0

    # first read
    l_in = streamin.readline()
    if not l_in:
        print('**************')
        print('* Empty File *')
        print('**************')
        return 1
    #fi

    newid, newkey1, newkey2, newkey3, newmnt = l_in.split()
    nbenrread += 1

    # loop
    while feof is False:

        # datas save
        oldid = newid
        oldkey1 = newkey1
        oldkey2 = newkey2
        oldkey3 = newkey3
        oldmnt = newmnt

        # second read
        l_in = streamin.readline()
        if not l_in:
            feof = True
        else:
            newid, newkey1, newkey2, newkey3, newmnt = l_in.split()
            nbenrread += 1
        #fi

        # at this point, we have two lines for the stream old one and new one

        # check good sort, useless
        # check sort key1
        if newkey1 < oldkey1:
            print('**************************')
            print('* Sorting error for key1 *')
            print('**************************')
            print('at record number :', nbenrread)
            print('newkey1 :', newkey1, 'oldkey1 :', oldkey1)
            return 1
        #fi

        # check sort key2
        if (newkey1 == oldkey1) and (newkey2 < oldkey2):
            print('**************************')
            print('* Sorting error for key2 *')
            print('**************************')
            print('at record number :', nbenrread)
            print('newkey1 :', newkey1, 'oldkey1 :', oldkey1)
            print('newkey2 :', newkey2, 'oldkey2 :', oldkey2)
            return 1
        #fi

        # check sort key3
        if (newkey1 == oldkey1) and (newkey2 == oldkey2) and (newkey3 < oldkey3):
            print('**************************')
            print('* Sorting error for key3 *')
            print('**************************')
            print('at record number :', nbenrread)
            print('newkey1 :', newkey1, 'oldkey1 :', oldkey1)
            print('newkey2 :', newkey2, 'oldkey2 :', oldkey2)
            print('newkey3 :', newkey3, 'oldkey3 :', oldkey3)
            return 1
        #fi

        # now we checked last mouvement for each key
        # a last mouvement is when key change
        # a last mouvement mean a first mouvement for the next round !!!
        #---------------------------------------------------------------

        # rupt permutation
        fmvkey = lmvkey
        lmvkey = False

        # rupt calc one key created with concatenation key1+key2+key3
        if (oldkey1+oldkey2+oldkey3 != newkey1+newkey2+newkey3) or feof:
            lmvkey = True
        #fi

        # on first mouvement in key create file using PREVIOUS record
        if fmvkey:
            try:
                fileout = open(gem+oldkey1+oldkey2+oldkey3+'.txt', 'w')
            except IOError:
                fileout.close()
                sys.exit(status)
            #endtry
            nbfiles += 1
        #fi

        # print PREVIOUS record not current for detail line
        fileout.write(oldid+' '+oldkey1+' '+oldkey2+' '+oldkey3+' '+oldmnt+'\n')

        # accumulate
        nbenrwrite += 1
        nbenrkey += 1

        # on last mouvement in key close file using PREVIOUS record
        if lmvkey:
            fileout.close()
            print('records written            : {0:>15d} in file {1:s}'\
                  .format(nbenrkey, gem+oldkey1+oldkey2+oldkey3+'.txt'))
            nbenrkey = 0
        #fi
    #endloop

    print()
    print('Number of records read     : {0:>15d}'.format(nbenrread))
    print('Number of files created    : {0:>15d}'.format(nbfiles))
    print('Number of records written  : {0:>15d}'.format(nbenrwrite))
    return 0

if __name__ == '__main__':

    # argparse: standard command line parser
    parser = argparse.ArgumentParser(description='Split input sorted with 3 keys')
    parser.add_argument('--file', default='ficin.txt')
    parser.add_argument('--gem', default='gem')
    args = parser.parse_args()

    status = 1

    print('Program started')
    nowstart = datetime.now()
    print('Start Date                 : ', nowstart.today())
    print()

    # selection of input stream stdin or file
    filein = sys.stdin
    if args.file == '-':
        status = main(gem=args.gem, streamin=filein)
    else:
        try:
            filein = open(args.file, 'r')
            status = main(gem=args.gem, streamin=filein)
            filein.close()
        except IOError:
            filein.close()
            print(args.file, ': No such file')
            print('program aborted')
            sys.exit(status)
        #endtry
    #fi

    nowend = datetime.now()
    print()
    print('End Date                   : ', nowend.today())
    print('Duration                   : ', nowend - nowstart)
    print('Job terminated')
    sys.exit(status)
#fi

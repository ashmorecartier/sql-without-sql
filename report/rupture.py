#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Demonstration program generating a report for stdout

    standalone program
    ------------------
    output produces :
        Header key1
            Header key2
                Header key3
                    current record
                    ...
                Foot key3
                ...
            Header key2
            ...
        Foot key1
        ...
    with subtotal and number of records

    parameters
    ---------
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

_nblinespage = 80
_nbcarligne = 100

_pagebreak = '<PAGE_BREAK>'

def main(dttrt, streamin):

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
    lmvkey1 = True
    lmvkey2 = True
    lmvkey3 = True
    # first mouvement for key, first mouvement is the previous last mouvement
    fmvkey1 = True
    fmvkey2 = True
    fmvkey3 = True

    # end of file
    feof = False

    # we maintain a record counter per key and a total record counter
    nbenrtotl = 0
    nbenrkey1 = 0
    nbenrkey2 = 0
    nbenrkey3 = 0

    # we maintain a sum of mnt per key and a total sum for mnt
    cpttotl = 0.0
    cptkey1 = 0.0
    cptkey2 = 0.0
    cptkey3 = 0.0

    # number of lines printed
    nblines_printed = 0

    # page counter
    npage = 0

    # number of lines printed in one page
    nbl = 999

    # line to print
    ltp = 0

    # flag for a header needed
    needheader = True

    # first read
    l_in = streamin.readline()
    if not l_in:
        print('**************')
        print('* Empty File *')
        print('**************')
        return 1
    #fi

    newid, newkey1, newkey2, newkey3, newmnt = l_in.split()

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
        #fi

        # at this point, we have two lines for the stream old one and new one

        # check good sort, useless
        # check sort key1
        if newkey1 < oldkey1:
            print('**************************')
            print('* Sorting error for key1 *')
            print('**************************')
            print('at record number :', nbenrtotl)
            print('newkey1 :', newkey1, 'oldkey1 :', oldkey1)
            return 1
        #fi

        # check sort key2
        if (newkey1 == oldkey1) and (newkey2 < oldkey2):
            print('**************************')
            print('* Sorting error for key2 *')
            print('**************************')
            print('at record number :', nbenrtotl)
            print('newkey1 :', newkey1, 'oldkey1 :', oldkey1)
            print('newkey2 :', newkey2, 'oldkey2 :', oldkey2)
            return 1
        #fi

        # check sort key3
        if (newkey1 == oldkey1) and (newkey2 == oldkey2) and (newkey3 < oldkey3):
            print('**************************')
            print('* Sorting error for key3 *')
            print('**************************')
            print('at record number :', nbenrtotl)
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
        fmvkey1 = lmvkey1
        fmvkey2 = lmvkey2
        fmvkey3 = lmvkey3
        lmvkey1 = False
        lmvkey2 = False
        lmvkey3 = False

        # rupt calc key1 ==> key2 ==> key3
        if (oldkey1 != newkey1) or feof:
            lmvkey1 = True
            lmvkey2 = True
            lmvkey3 = True
        #fi

        # rupt calc key2 ==> key3
        if (oldkey1 == newkey1) and (oldkey2 != newkey2):
            lmvkey2 = True
            lmvkey3 = True
        #fi

        # rupt calc key3
        if (oldkey1 == newkey1) and (oldkey2 == newkey2) and (oldkey3 != newkey3):
            lmvkey3 = True
        #fi

        # calc of number of lines to print in this iteration
        ltp = 0
        if fmvkey1:
            ltp += 2
        #fi
        if fmvkey2:
            ltp += 1
        #fi
        if fmvkey3:
            ltp += 1
        #fi
        ltp += 1
        if lmvkey3:
            ltp += 3
        #fi
        if lmvkey2:
            ltp += 2
        #fi
        if lmvkey1:
            ltp += 2
        #fi

        # if lines to print in this iteration make a page break before
        if nbl + ltp >= _nblinespage:
            npage += 1
            print(_pagebreak)
            s_d = '{0:%A, %B %d, %Y}'.format(dttrt)
            s_p = 'page : {0:>8d}'.format(npage)
            print(s_d + ' '*(_nbcarligne-len(s_d)-len(s_p)) + s_p)
            nblines_printed += 1
            nbl = 0
            needheader = True
        #fi

        # on first mouvement in key1 print header key1 on 1 page using PREVIOUS record
        if fmvkey1:
            print()
            print('header key1 : {0:>8s}'\
                  .format(oldkey1))
            nblines_printed += 2
            nbl += 2
        #fi

        # on first mouvement in key2 print header key2 on 1 page using PREVIOUS record
        if fmvkey2:
            print('\theader key2 : {0:>8s} in key1 : {1:>8s}'\
                  .format(oldkey2, oldkey1))
            nblines_printed += 1
            nbl += 1
        #fi

        # on first mouvement in key3 print header key3 using PREVIOUS record
        if fmvkey3:
            print('\t\theader key3 : {0:>8s} in key2 : {1:>8s} in key1 : {2:>8s}'\
                  .format(oldkey3, oldkey2, oldkey1))
            nblines_printed += 1
            nbl += 1
        #fi

        # new header needed if new page
        if needheader:
            print()
            print('\t\t\t    key1     key2     key3       id               debit           credit')
            print('\t\t\t------------------------------------------------------------------------')
            nblines_printed += 3
            nbl += 3
            needheader = False
        #fi

        # print PREVIOUS record not current for detail line
        s_d = '\t\t\t{0:>8s}'.format(oldkey1) + ' '
        s_d += '{0:>8s}'.format(oldkey2) + ' '
        s_d += '{0:>8s}'.format(oldkey3) + ' '
        s_d += '{0:>8s}'.format(oldid) + ' '
        f_mnt = float(oldmnt)
        if f_mnt < 0:
            s_d += '({0:>18,.2f})'.format(-f_mnt) + ' '*18
        else:
            s_d += ' '*18 + '{0:>18,.2f}'.format(f_mnt)
        print(s_d)

        # accumulate
        nbenrtotl += 1
        nbenrkey1 += 1
        nbenrkey2 += 1
        nbenrkey3 += 1
        cpttotl += float(oldmnt)
        cptkey1 += float(oldmnt)
        cptkey2 += float(oldmnt)
        cptkey3 += float(oldmnt)

        nblines_printed += 1
        nbl += 1

        # on last mouvement in key3 print footer key3 using PREVIOUS record
        if lmvkey3:
            print()
            print('\t\tfooter key3 : {0:>8s} in key2 : {1:>8s} in key1 : {2:>8s}'\
                  .format(oldkey3, oldkey2, oldkey1))
            print('\t\tnb. records = {0:>8d} total amount = {1:>18,.2f}'\
                  .format(nbenrkey3, cptkey3))
            nbenrkey3 = 0
            cptkey3 = 0.0
            nblines_printed += 3
            nbl += 3
        #fi

        # on last mouvement in key2 print footer key2 using PREVIOUS record
        if lmvkey2:
            print('\tfooter key2 : {0:>8s} in key1 : {1:>8s}'\
                  .format(oldkey2, oldkey1))
            print('\tnb. records = {0:>8d} total amount = {1:>18,.2f}'\
                  .format(nbenrkey2, cptkey2))
            nbenrkey2 = 0
            cptkey2 = 0.0
            nblines_printed += 2
            nbl += 2
        #fi

        # on last mouvement in key1 print footer key1 using PREVIOUS record
        if lmvkey1:
            print('footer key1 : {0:>8s}'.format(oldkey1))
            print('nb. records = {0:>8d} total amount = {1:>18,.2f}'\
                  .format(nbenrkey1, cptkey1))
            nbenrkey1 = 0
            cptkey1 = 0.0
            nblines_printed += 2
            nbl += 2
        #fi
    #endloop

    print()
    print('Number of records       : {0:>15d}'.format(nbenrtotl))
    print('Total amount            : {0:>18,.2f}'.format(cpttotl))
    print('Number of pages printed : {0:>15d}'.format(npage))
    print('Number of lines printed : {0:>15d}'.format(nblines_printed))
    return 0

if __name__ == '__main__':

    # argparse: standard command line parser
    parser = argparse.ArgumentParser(description='Edit input sorted with 3 keys')
    parser.add_argument('--file', default='ficin.txt')
    args = parser.parse_args()

    status = 1

    print('Program started')
    nowstart = datetime.now()
    print('Start Date                 : ', nowstart.today())
    print()

    # selection of input stream stdin or file
    filein = sys.stdin
    if args.file == '-':
        status = main(dttrt=nowstart, streamin=filein)
    else:
        try:
            filein = open(args.file, 'r')
            status = main(dttrt=nowstart, streamin=filein)
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

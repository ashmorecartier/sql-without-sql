#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Demonstration program generating daily, weekly,
    monthly and yearly barchart from a daily barchart

    standalone program
    ------------------
    output produces :
        Type : D, W, M, Y
        Datedeb : Start date for period
        Dateend : End date for period
        Open : Value for open
        High : Value for high
        Low : Value for low
        Close : Value for close
        Separator : blank

    parameters
    ---------
    file: a file 'cote.txt'
        each lines of file contain :
            Date : format JJ/MM/AAAA
            Open : Value for open
            High : Value for high
            Low : Value for low
            Close : Value for close
            separator : blank
'''

import sys
import argparse
from datetime import datetime, date, MINYEAR

def main(streamin):

    """
        Calculate barchart
    """

    # init global var
    # datas from stream
    newdate = ''
    newopen = ''
    newhigh = ''
    newlow = ''
    newclose = ''
    # datas from stream
    olddate = '' # marked unused variable OK
    oldopen = ''
    oldhigh = ''
    oldlow = ''
    oldclose = ''

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

    # counter record read
    nbread = 0

    # we maintain a record counter written per key and a total record counter
    nbenrtot = 0
    nbenry = 0
    nbenrm = 0
    nbenrw = 0
    nbenrd = 0

    # var for weekly
    datedebw = date(MINYEAR, 1, 1)
    dateendw = date(MINYEAR, 1, 1)
    openw = ''
    highw = ''
    loww = ''
    closew = ''

    # var for monthly
    datedebm = date(MINYEAR, 1, 1)
    dateendm = date(MINYEAR, 1, 1)
    openm = ''
    highm = ''
    lowm = ''
    closem = ''

    # var for yearly
    datedeby = date(MINYEAR, 1, 1)
    dateendy = date(MINYEAR, 1, 1)
    openy = ''
    highy = ''
    lowy = ''
    closey = ''

    # first read
    l_in = streamin.readline()
    if not l_in:
        print('**************')
        print('* Empty File *')
        print('**************')
        return 1
    #fi

    newdate, newopen, newhigh, newlow, newclose = l_in.split()
    newd = date(int(newdate[6:10]), int(newdate[3:5]), int(newdate[0:2]))
    nbread += 1

    # loop
    while feof is False:

        # datas save
        olddate = newdate
        oldopen = newopen
        oldhigh = newhigh
        oldlow = newlow
        oldclose = newclose
        oldd = newd

        # second read
        l_in = streamin.readline()
        if not l_in:
            feof = True
        else:
            newdate, newopen, newhigh, newlow, newclose = l_in.split()
            newd = date(int(newdate[6:10]), int(newdate[3:5]), int(newdate[0:2]))
            nbread += 1
        #fi

        # at this point, we have two lines for the stream old one and new one

        # check good sort, useless
        # check sort date
        if newd < oldd:
            print('**************************')
            print('* Sorting error for date *')
            print('**************************')
            print('at record number :', nbenrtot)
            print('newd :', newd, 'oldd :', oldd)
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

        # rupt calc key1 yearly
        if (oldd.year != newd.year) or feof:
            lmvkey1 = True
        #fi

        # rupt calc key2 monthly
        if (oldd.month != newd.month) or feof:
            lmvkey2 = True
        #fi

        # rupt calc key3 weekly, weak if market is closed more than 1 week
        if (oldd.weekday() > newd.weekday()) or feof:
            lmvkey3 = True
        #fi

        # on first mouvement in key1 keep trace of datas using PREVIOUS record
        if fmvkey1:
            datedeby = oldd
            openy = oldopen
            highy = oldhigh
            lowy = oldlow
        #fi

        # on first mouvement in key2 keep trace of datas using PREVIOUS record
        if fmvkey2:
            datedebm = oldd
            openm = oldopen
            highm = oldhigh
            lowm = oldlow
        #fi

        # on first mouvement in key3 keep trace of datas using PREVIOUS record
        if fmvkey3:
            datedebw = oldd
            openw = oldopen
            highw = oldhigh
            loww = oldlow
        #fi

        # print PREVIOUS record not current for detail line
        s_d = 'D' + ' '
        s_d += '{0:}'.format(oldd) + ' '
        s_d += '{0:}'.format(oldd) + ' '
        s_d += '{0:>6.4f}'.format(float(oldopen)) + ' '
        s_d += '{0:>6.4f}'.format(float(oldhigh)) + ' '
        s_d += '{0:>6.4f}'.format(float(oldlow)) + ' '
        s_d += '{0:>6.4f}'.format(float(oldclose)) + ' '
        print(s_d)
        nbenrtot += 1
        nbenrd += 1

        # accumulate or calculate
        # for yearly
        if float(oldhigh) > float(highy):
            highy = oldhigh
        #fi
        if float(oldlow) < float(lowy):
            lowy = oldlow
        #fi

        # for monthly
        if float(oldhigh) > float(highm):
            highm = oldhigh
        #fi
        if float(oldlow) < float(lowm):
            lowm = oldlow
        #fi

        # for weekly
        if float(oldhigh) > float(highw):
            highw = oldhigh
        #fi
        if float(oldlow) < float(loww):
            loww = oldlow
        #fi

        # on last mouvement in key3 print footer key3 using PREVIOUS record
        if lmvkey3:
            dateendw = oldd
            closew = oldclose
            s_d = 'W' + ' '
            s_d += '{0:}'.format(datedebw) + ' '
            s_d += '{0:}'.format(dateendw) + ' '
            s_d += '{0:>6.4f}'.format(float(openw)) + ' '
            s_d += '{0:>6.4f}'.format(float(highw)) + ' '
            s_d += '{0:>6.4f}'.format(float(loww)) + ' '
            s_d += '{0:>6.4f}'.format(float(closew)) + ' '
            print(s_d)
            nbenrtot += 1
            nbenrw += 1
        #fi

        # on last mouvement in key2 print footer key2 using PREVIOUS record
        if lmvkey2:
            dateendm = oldd
            closem = oldclose
            s_d = 'M' + ' '
            s_d += '{0:}'.format(datedebm) + ' '
            s_d += '{0:}'.format(dateendm) + ' '
            s_d += '{0:>6.4f}'.format(float(openm)) + ' '
            s_d += '{0:>6.4f}'.format(float(highm)) + ' '
            s_d += '{0:>6.4f}'.format(float(lowm)) + ' '
            s_d += '{0:>6.4f}'.format(float(closem)) + ' '
            print(s_d)
            nbenrtot += 1
            nbenrm += 1
        #fi

        # on last mouvement in key1 print footer key1 using PREVIOUS record
        if lmvkey1:
            dateendy = oldd
            closey = oldclose
            s_d = 'Y' + ' '
            s_d += '{0:}'.format(datedeby) + ' '
            s_d += '{0:}'.format(dateendy) + ' '
            s_d += '{0:>6.4f}'.format(float(openy)) + ' '
            s_d += '{0:>6.4f}'.format(float(highy)) + ' '
            s_d += '{0:>6.4f}'.format(float(lowy)) + ' '
            s_d += '{0:>6.4f}'.format(float(closey)) + ' '
            print(s_d)
            nbenrtot += 1
            nbenry += 1
        #fi
    #endloop

    print()
    print('Number of records read     : {0:>15d}'.format(nbread))
    print()
    print('Number of recordsY         : {0:>15d}'.format(nbenry))
    print('Number of recordsM         : {0:>15d}'.format(nbenrm))
    print('Number of recordsW         : {0:>15d}'.format(nbenrw))
    print('Number of recordsD         : {0:>15d}'.format(nbenrd))
    print('Number of records          : {0:>15d}'.format(nbenrtot))
    return 0

if __name__ == '__main__':

    # argparse: standard command line parser
    parser = argparse.ArgumentParser(description='Make barcharts')
    parser.add_argument('--file', default='cote.txt')
    args = parser.parse_args()

    status = 1

    print('Program started')
    nowstart = datetime.now()
    print('Start Date                 : ', nowstart.today())
    print()

    # selection of input stream stdin or file
    try:
        filein = open(args.file, 'r')
        status = main(streamin=filein)
        filein.close()
    except IOError:
        filein.close()
        print(args.file, ': No such file')
        print('program aborted')
        sys.exit(status)
    #endtry

    nowend = datetime.now()
    print()
    print('End Date                   : ', nowend.today())
    print('Duration                   : ', nowend - nowstart)
    print('Job terminated')
    sys.exit(status)
#fi

#!/home/pmccrone/anaconda3/bin/python
# -*- coding: utf-8 -*-
#==============================================================
#
#==============================================================
#
#==-ROC/FRB PYTHON PROGRAM DEFINITION-==========================================
#
#/home/pmccrone/python/src/runrpg
#
# NAME:
# :::::::::::::::::::::::::::::::::::::::::::::::
# process_level3_NST_v1.py
# :::::::::::::::::::::::::::::::::::::::::::::::
#
#  PROGRAM OVERVIEW:
#       (0) The PYTHON CODE reads WSR88D L3 information from a file. 
#       (1) The information is used to decode NEXRAD data for further post analysis.
#
#--------------------------------------------------------------------------------------------------
# PARAMETER TABLE:
#--------------------------------------------------------------------------------------------------
#
# I/O           NAME                               TYPE            FUNCTION
#--------------------------------------------------------------------------------------------------
#  I            Level III           input          INPUT           DATA FROM ROC/FRB
#  O            Formatted table of data            output          formatted information
#_________________________________________________________________________________________________
#=================================================================================================
#
#=================================================================================================
#-
#
# Programmer: Mr. Paul McCrone     07 Nov 2023
# Modification  :  BELOW
#========================================================================================
#  Version 1.0   , Dated 2032-Nov-07
#                  Initial Build.
#========================================================================================
#  NOTE: THIS PROGRAM ASSUMES THE USE OF Python version 3.8.8+ for RHEL.
#---------------------------------------------------------------
#
#  PYTHON MODULES USED: numpy, scipy, matplotlib, datetime, 
##
# Decode STI product 

import datetime
import time
import os

# Variables I will use in all functions:
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

DADASH='-----------------------------------------------------'
dadash='-----------------------------------------------------'
dadashes='-----------------------------------------------------'
#
DAEQUALS='==--==--==--==--==--==--==--==--==--==--==--==--==--'
#
DADASHES='----------------------------------------------------'

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ALL_call_signs= \
["PGUA","RKSG","RKJK","RODN","KABR","KENX","KABX","KFDR","KAMA","PAHG", \
"KEWX","KBBX","PABC","KBLX","KBGM","KBMX","KBIS","KCBX","KBOX","KBRO", \
"KBUF","KCXX","KFDX","KICX","KCLX","KRLX","KCYS","KLOT","KILN","KCLE", \
"KCAE","KGWX","KCRP","KFWS","KDVN","KFTG","KDMX","KDTX","KDDC","KDOX", \
"KDLH","KDYX","KEYX","KEVX","KEPZ","KLRX","KBHX","PAPD","KFSX","KHPX", \
"KGRK","KPOE","KEOX","KSRX","KIWX","KAPX","KGGW","KGLD","KMVX","KGJX", \
"KGRR","KTFX","KGRB","KGSP","KRMX","KUEX","KHDX","KCBW","KHGX","KHTX", \
"KIND","KJKL","KDGX","KJAX","PHKN","KEAX","KBYX","PAKC","KMRX","KARX", \
"LPLA","KLCH","KESX","KDFX","KILX","KLZK","KVTX","KLVX","KLBB","KMQT", \
"KMXX","KMAX","KMLB","KNQA","KAMX","PAIH","KMAF","KMKX","KMPX","KMBX", \
"KMSX","KMOB","PHMO","KVAX","KMHX","KOHX","KLIX","KOKX","PAEC","KAKQ", \
"KLNX","KTLX","KOAX","KPAH","KPDT","KDIX","KIWA","KPBZ","KSFX","KGYX", \
"KRTX","KPUX","KRAX","KUDX","KRGX","KRIW","KFCX","KJGX","KDAX","KLSX", \
"KMTX","KSJT","KNKX","KMUX","KHNX","TJUA","KSOX","KATX","KSHV","KFSD", \
"PACG","PHKI","PHWA","KOTX","KSGF","KCCX","KLWX","KTLH","KTBW","KTWX", \
"KEMX","KINX","KVNX","KVBX","KICT","KLTX","KFFC","KYUX","KLGX"]
#

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
dict_call_signs={"KABR":"Aberdeen_SD", "KABX":"Albuquerque_NM", "KAKQ":"Norfolk-VA", \
"KAMA":"Amarillo_TX", "KBBX":"Beale-AFB_CA", \
"KAMX":"Miami-FL", "KAPX":"Gaylord_MI", "KARX":"La-Crosse_WI", "KATX":"Seattle-Tacoma_WA", \
"KBGM":"Binghamton_NY", "KBHX":"Eureka_CA", "KBIS":"Bismarck_ND", "KBLX":"Billings_MT", \
"KBMX":"Birmingham_AL", "KCAE":"Columbia_SC", \
"KBOX":"Boston-MA", "KBRO":"Brownsville-TX", "KBUF":"Buffalo_NY", "KBYX":"Key-West-FL", \
"KCBW":"Houlton-Maine", "KCBX":"Boise_ID", "KCCX":"State-College_PA", "KCLE":"Cleveland_OH", \
"KCLX":"Charleston-SC", "KDDC":"Dodge-City_KS", \
"KCRP":"Corpus-Christi-TX", "KCXX":"Burlington_VT", "KCYS":"Cheyenne_WY", "KDAX":"Sacramento_CA", \
"KDFX":"Laughlin-AFB_TX", "KDIX":"Philadelphia-PA", "KDLH":"Duluth_MN", "KDMX":"Des-Moines_IA", \
"KDOX":"Dover-AFB-DE", "KEMX":"Tucson_AZ", \
"KDTX":"Detroit_MI", "KDVN":"Davenport_IA", "KDYX":"Dyess-AFB_TX", "KEAX":"Kansas-City_MO", \
"KENX":"Albany_NY", "KEOX":"Fort-Rucker_AL", "KEPZ":"El-Paso_TX", "KESX":"Las-Vegas_NV", \
"KEVX":"Eglin-AFB-FL", "KFDX":"Cannon-AFB_NM", \
"KEWX":"Austin-San-Antonio_TX", "KEYX":"Edwards-AFB_CA", "KFCX":"Roanoke_VA", "KFDR":"Altus-AFB_OK", \
"KFFC":"Atlanta_GA", "KFSD":"Sioux-Falls_SD", "KFSX":"Flagstaff_AZ","KFTG":"Denver_CO", \
"KFWS":"Dallas-Ft.Worth_TX", "KGRK":"Fort-Hood_TX", \
"KGGW":"Glasgow_MT", "KGJX":"Grand-Junction_Co", "KGLD":"Goodland_KS", "KGRB":"Green-Bay_WI", \
"KGRR":"Grand-Rapids_MI", "KGSP":"Greer_SC", "KGWX":"Columbus-AFB,_ MS", "KGYX":"Portland-Maine", \
"KHDX":"Holloman-AFB_NM", "KHTX":"Huntsville_AL",  \
"KHGX":"Houston-Galveston-TX", "KHNX":"San-Joaquin-Valley_CA", "KHPX":"Fort-Campbell_KY", \
"KICT":"Wichita_KS", "KICX":"Cedar-City_UT", "KILN":"Cincinnati_OH", "KILX":"Lincoln_IL", \
"KIND":"Indianapolis_IN", "KJAX":"Jacksonville-FL", \
"KINX":"Tulsa_OK", "KIWA":"Phoenix_AZ", "KIWX":"Fort-Wayne_IN", "KDGX":"Jackson_MS", \
"KJGX":"Robins-AFB_GA", "KJKL":"Jackson_KY", "KLBB":"Lubbock_TX", "KLCH":"Lake-Charles-LA", \
"KLIX":"New-Orleans-LA", "KLTX":"Wilmington-NC", \
"KLNX":"North-Platte_NE", "KLOT":"Chicago_IL", "KLRX":"Elko_NV", "KLSX":"Saint-Louis_ MO", \
"KLVX":"Louisville_KY", "KLWX":"Sterling-VA", "KLZK":"Little-Rock_AR", "KMAF":"Midland-Odessa_TX", \
"KMAX":"Medford_OR", "KMOB":"Mobile-AL", \
"KMBX":"Minot-AFB_ND", "KMHX":"Morehead-City-NC", "KMKX":"Milwaukee_WI", "KMLB":"Melbourne-FL", \
"KMPX":"Minneapolis-St.Paul_MN", "KMQT":"Marquette_MI", "KMRX":"Knoxville-Tri-Cities_TN", \
"KMSX":"Missoula_MT", "KNKX":"San-Diego-CA", \
"KMTX":"Salt-Lake-City_UT", "KMUX":"San-Francisco_CA", "KMVX":"Grand-Forks_ND", "KMXX":"Maxwell-AFB_AL", \
"KNQA":"Memphis_TN", "KOAX":"Omaha_NE", "KOHX":"Nashville_TN", "KOKX":"New-York-City-NY", \
"KOTX":"Spokane_WA", "KPAH":"Paducah_KY", \
"KPBZ":"Pittsburgh_PA", "KPDT":"Pendleton_OR", "KPOE":"Fort-Polk_LA", "KPUX":"Pueblo_CO", \
"KRAX":"Raleigh-Durham_NC", "KRGX":"Reno-NV", "KSFX":"Pocatello-Idaho-Falls_ID", \
"KRIW":"Riverton_WY", "KRLX":"Charleston_WV", "KRMX":"Griffiss-AFB_NY", "KRTX":"Portland_OR", \
"KSGF":"Springfield_MO", "KSHV":"Shreveport_LA", "KSJT":"San-Angelo_TX", \
"KSOX":"Santa-Ana_Mountains_CA", "KTLX":"Oklahoma-City_OK", \
"KSRX":"Fort-Smith_AR", "KTBW":"Tampa-FL", "KTFX":"Great-Falls_MT", "KTLH":"Tallahassee-FL", \
"KTWX":"Topeka_KS", "KUDX":"Rapid-City_SD", "KUEX":"Hastings_NE", "KVAX":"Moody-AFB_GA", \
"KVBX":"Vandenberg-AFB_CA", "PABC":"Bethel_AK", \
"KVNX":"Vance-AFB_OK", "KVTX":"Los_Angeles_CA", "KYUX":"Yuma_AZ", "LPLA":"Lajes-AB_Azores", \
"PACG":"Sitka_AK", "PAEC":"Nome_AK", "PAHG":"Anchorage_AK", "PAIH":"Middleton-Island_AK",
"PAKC":"King-Salmon_AK", "PHKM":'Kamuela-Kohala-HI', \
"PAPD":"Fairbanks_AK", "PGUA":"Anderson-AFB-Guam", "PHKI":"South-Kauai-HI", \
"PHKN":"Kamuela_HI", "PHMO":"Molokai-HI", "PHWA":"South-Shore-HI", "RKJK":"Kunsan-AB-Korea", \
"RKSG":"Camp-Humphreys-Korea", "RODN":"Kadena_Okinawa", "TJUA":"San-Juan-Puerto-Rico", \
"KLGX":"Langley-Hill_WA"}
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# run the following linux command to turn the Nexrad
# level III product into ascii data.

# xxd -s 0 -l 218450 -c 30  KFDR_SDUS84_NSTFDR_202205050336 >> KFDR_SDUS84_NSTFDR_202205050336.hex

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Print_Current_Time
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Print_Current_Time(now):
    #-----
    ###import datetime
    #-----
    now = datetime.datetime.now()
    #-----
    print ()
    print( "Current date and time using str method of datetime object:")
    print( str(now))
    #-----
    print( " \n")
    print( "Current date and time using instance attributes:")
    print( "Current year: %d" % now.year)
    print( "Current month: %d" % now.month)
    print( "Current day: %d" % now.day)
    print( "Current hour: %d" % now.hour)
    print( "Current minute: %d" % now.minute)
    print( "Current second: %d" % now.second)
    print( "Current microsecond: %d" % now.microsecond)
    #-----
    print( " \n")
    print( "Current date and time using strftime:")
    #print now.strftime("%Y-%m-%d %H:%M")
    print( now.strftime("%Y-%m-%d...%H:%M"))
    #-----
    print( " \n")
    print( "Current date and time using isoformat:")
    print( now.isoformat())
    return( now.strftime("%Y-%m-%d...%H:%M"))
    #return now
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Print_Current_Time FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#determine_date_since_1970
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

def determine_date_since_1970(days):
    t2=(days-1)*24*60*60
    mytime=time.gmtime(t2)
    #time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=4, tm_min=56, tm_sec=4, tm_wday=3, tm_yday=1, tm_isdst=0)
    year=mytime.tm_year
    month=mytime.tm_mon
    strmonth=str(month)
    day=mytime.tm_mday
    strday=str(day)
    if len(strmonth) == 1:
        oldmonth=month
        strmonth="0"+str(oldmonth)
    if len(strday) == 1:
        oldday=day
        strday='0'+str(oldday)

    date=str(year)+":"+strmonth+":"+strday
    #
    return(date)
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #END OF determine_date_since_1970
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----


#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function determine_time_since_midnight
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

def determine_time_since_midnight(seconds):
    #This function will assume you input the number of seconds since mignight
    #The output will be a string in HH:MM:SS assuming a 24 hour clock like 
    #23:59:50

    hours=int(seconds/(60*60))
    waterfall=seconds-(hours*60*60)
    minutes=int(waterfall/60)
    remsec=waterfall-(minutes*60)
    strhours=str(hours)
    if hours < 10:
        strhours='0'+str(hours)
    strminutes=str(minutes)
    if minutes < 10:
        strminutes='0'+str(minutes)
    strremsec=str(remsec)
    if remsec < 10:
        strremsec='0'+str(remsec)
    time_string=strhours+":"+strminutes+":"+strremsec
    #
    return(time_string)
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    # END OF determine_time_since_midnight
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----


def printbn():
    #
    print('\n')
    #END OF Function

def printds():
    #
    print('--------------------------------------------')
    #END

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
####### Begin decode_halfword
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#

def decode_halfword(halfwrd):
    # Decode a four char string in hexadecimal to a number.
    value=int(halfwrd, 16)
    return(value)

    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF decode_halfword FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
####### Begin decode_twohalfwords
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#

def decode_twohalfwords(halfwrds):

    # Decode a string with nine characters and a space in the middle in hexadecimal to number
    halfwrd1=halfwrds[0:4]
    halfwrd2=halfwrds[5:]
    wholewrd=halfwrd1+halfwrd2
    printds()
    print('We will convert the hex value to decimal: '+wholewrd)
    value=int(wholewrd, 16)
    print('The converted value is:'+str(value))
    print(DADASHES)
    return(value)

    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF decode_halfword FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

########
# MAIN part of program
########

now=0
Print_Current_Time(now)

datadirectry='/home/pmccrone/test/'
file='KFDR_SDUS84_NSTFDR_202205050336.txt'
l3file='KFDR_SDUS84_NSTFDR_202205050336'
pdbfile='KFDR_SDUS84_NSTFDR_202205050336.pdb.ascii'

thefile=datadirectry+file

if os.path.isfile(thefile):
    os.system('rm -rf '+thefile)
    os.system('rm -rf *.ascii')
    print("removed file")
else:
    print("The file has not bee made")

#xxd -s 0 -l 218450 -c 30  KFDR_SDUS84_NSTFDR_202205050336 >> KFDR_SDUS84_NSTFDR_202205050336.hex
os.system('xxd -s 0 -l 218450 -c 30 '+datadirectry+l3file+' >> '+datadirectry+file)

# making the PRODUCT DESCRIPTION BLOCK
os.system('xxd -s 48 -l 120 -c 30 '+datadirectry+l3file+' >> '+datadirectry+pdbfile)

# lines contains the entire file.
print("This is the entire file")
with open(thefile) as f:
    lines =  f.readlines()

f.close()

count=len(lines[0])

awips_top=lines[0]

awips_header=awips_top[count-31:-1]

##### GET the Product Description block read in separately.

# 
print("This is the Product Description Block")
printds()
#
with open(datadirectry+pdbfile) as ff:
    plines=  ff.readlines()

ff.close()
#

for pli in plines:
    print(pli)

    

##### BEGIN DECODING

printbn()
printds()
print("HERE IS THE AWIPS HEADER:")
printds()
print(awips_header)
printbn()


###
### DECODE MESSAGE HEADER
printbn()
printds()
print("Print the MESSAGE HEADER INFO")
printds()


MSG_HEADER_RAW=lines[1]

# HALFWORD 01

MSG_HEADER_HEX=MSG_HEADER_RAW[10:54]
MSG_CODE=MSG_HEADER_HEX[0:4]
real_msg_code=decode_halfword(MSG_CODE)

print('MSG_CODE (Hx) =                      '+MSG_CODE)
print('real_msg_code =                      '+str(real_msg_code))

printbn()

# HALFWORD 02

DATE_OF_MSG=MSG_HEADER_HEX[5:9]
real_date_msg=decode_halfword(DATE_OF_MSG)

print('DATE OF MSG (Hx) =                   '+DATE_OF_MSG)
print('real date of mesg in Julian Dt =     '+str(real_date_msg))

Current_date_of_msg=determine_date_since_1970(real_date_msg)
print('The date of the data is:             '+Current_date_of_msg)

printbn()

# HALFWORDS 03-04

TIME_OF_MSG=MSG_HEADER_HEX[10:19]
real_time_msg=decode_twohalfwords(TIME_OF_MSG)

print('TIME OF MSG (Hx) =                   '+TIME_OF_MSG)
print('time of msg num secs after midnight: '+str(real_time_msg))
printbn()

Current_time_of_msg=determine_time_since_midnight(real_time_msg)
print('The system time since midnight is:   '+Current_time_of_msg)
printbn()

# HALFWORDS 05-06 : LENGTH OF MESSAGE

#LENGTH_OF_MSG=
LENGTH_OF_MSG=MSG_HEADER_HEX[20:29]
real_length_msg=decode_twohalfwords(LENGTH_OF_MSG)

print('LENGTH_OF_MSG =                      '+LENGTH_OF_MSG)
print('length of message in bytes =         '+str(real_length_msg))
printbn()

# HALFWORD 07 : SOURCE ID

SOURCEID=MSG_HEADER_HEX[30:34]
real_sourceid=decode_halfword(SOURCEID)

print('SOURCEID =                           '+SOURCEID)
print('real sourceid =                      '+str(real_sourceid))

# HALFWORD 08 : DESTINATON ID
DESTINATION_ID=MSG_HEADER_HEX[35:39]
real_destination_id=decode_halfword(DESTINATION_ID)
print('DESTINATION_ID =                     '+DESTINATION_ID)
print('real destination id =                '+str(real_destination_id))

# HALFWORD 09 : Number of blocks
NUM_BLOCKS=MSG_HEADER_HEX[40:44]
real_num_blocks=decode_halfword(NUM_BLOCKS)
print('NUM_BLOCKS =                         '+NUM_BLOCKS)
print('real_num_blocks =                    '+str(real_num_blocks))


#
# ISOLATE THE PRODUCT DECRIPTION BLCK
#

# type this at the linux prompt: 
# xxd -s 48 -l 120 -c 30 filename

# This was done ealier and is now in the string array plines

# the first halfword of the PDB is HALFWORD 10 is the ffff (a block divider)
# We do not read this block.

printbn()
printds()
print("Print the PRODUCT DESCRIPTION BLOCK")
printds()


# We get the first line of the PDB

PDBLINE1=plines[1]
PDBLINE2=plines[2]
PDBLINE3=plines[3]
PDBLINE0=plines[0]

LAT_RADAR=PDBLINE0[15:24]
real_latx1000=decode_twohalfwords(LAT_RADAR)
real_lat_radar=real_latx1000/1000.0

print('LAT_RADAR =                          '+ LAT_RADAR)
print('real_latx1000 =                      '+ str(real_latx1000))
print('real_lat_radar=                      '+ str(real_lat_radar))

printds()
LONG_RADAR=PDBLINE0[25:34]
real_lonx1000=decode_twohalfwords(LONG_RADAR)

print('LONG_RADAR =                         '+ LONG_RADAR)
print('real_lonx1000 =                      '+ str(real_lonx1000))

##### Need to convert to binary, then flip bits, then determine value. 
#binary_str=bin(int(dec_num))

#strip_bin_str=binary_str[2:len(binary_str)]

#flipped=''.join('1' if x=='0' else '0' for x in strip_bin_str)

#info=int(flipped,2)

binary_str=bin(int(real_lonx1000))
strip_bin_str=binary_str[2:len(binary_str)]
flipped=''.join('1' if x=='0' else '0' for x in strip_bin_str)
longinfo=int(flipped,2)
print('converted real_lon_radar=            '+ str(longinfo))
real_lon_radar= longinfo/1000.0
print('real_lon_radar=                      '+ str(real_lon_radar))




# HALFWORD 15 : Radar Height in ft above Sea Level

printds()
HEIGHT_RADAR=PDBLINE0[35:39]
real_height_radar=decode_halfword(HEIGHT_RADAR)

print('HEIGHT_RADAR =                       '+HEIGHT_RADAR)
print('Height of Radar in ft above sea lvl ='+str(real_height_radar))

# HALFWORD 16: PRODUCT CODE

PRODUCT_CODE=PDBLINE0[40:44]
real_product_code=decode_halfword(PRODUCT_CODE)

print('PRODUCT_CODE =                       '+PRODUCT_CODE)
print('real_product_code =                  '+str(real_product_code))

# HALFWORD 17 : Operational Mode

OPER_MODE=PDBLINE0[45:49]
real_oper_mode=decode_halfword(OPER_MODE)
print('OPER_MODE =                          '+OPER_MODE)
print('real_oper_mode =                     '+str(real_oper_mode))

# HALFWORD 18 : VCP 

VCP=PDBLINE0[50:54]
real_vcp=decode_halfword(VCP)
print('VCP =                                '+VCP)
print('real_vcp =                           '+str(real_vcp))

printds()

# HALFWORD 19: SEQUENCE NUMBER

SEQ_NUM=PDBLINE0[55:59]
real_seq_num=decode_halfword(SEQ_NUM)
print('SEQ_NUM =                            '+SEQ_NUM)
print('real_seq_num =                       '+str(real_seq_num))

#-HALFWORD20: VOLUME SCAN Number
VSN=PDBLINE0[60:64]
real_vsn=decode_halfword(VSN)
print('VSN =                                '+VSN)
print('real_vsn =                           '+str(real_vsn))

# HALFWORD 21: Volume Scan Date
#
printds()
#
VOL_SCAN_DATE=PDBLINE0[65:69]
real_vol_scan_date=decode_halfword(VOL_SCAN_DATE)
Real_date_of_Volscan=determine_date_since_1970(real_vol_scan_date)

print('VOL_SCAN_DATE=                       '+VOL_SCAN_DATE)
print('real_vol_scan_date =                 '+str(real_vol_scan_date))
print('The ACTUAL date of the data is:      '+Real_date_of_Volscan)
printds()

# HALFWORD 22: Volume Scan time
#
VOL_SCAN_TIME=PDBLINE0[70:79]
#
real_vol_scan_time=decode_twohalfwords(VOL_SCAN_TIME)
Real_time_of_Volscan=determine_time_since_midnight(real_vol_scan_time)
print('VOL_SCAN_TIME=                       '+VOL_SCAN_TIME)
print('real_vol_scan_time =                 '+str(real_vol_scan_time))
print('The ACTUAL time of the data is:      '+Real_time_of_Volscan)





#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# END OF PYTHON

#>>> PDBLINE0='00000030: ffff 0000 863a fffe 7d5f 0523 003a 0002 00d4 0173 0009 4aae 0000 32cb 4abc  .....:..}_.#.:.....s..J...2.J.'
#>>> PDBLINE0[25:34]
#'fffe 7d5f'
#>>> string='fffe7d5f'
#>>> int(string,16)
#4294868319
#>>> string='fffe72b3'
#>>> int(string,16)
#4294865587
#>>> table = {'0': 0, '1': 1, '2': 2, '3': 3,
#...          '4': 4, '5': 5, '6': 6, '7': 7,
#...          '8': 8, '9': 9, 'A': 10, 'B': 11,
#...          'C': 12, 'D': 13, 'E': 14, 'F': 15}
#...
#>>> import math
#>>> dec_num = sum(int(x, 16) * math.pow(16, len(string)-i-1) for i, x in enumerate(string))
#>>> print(dec_num)
#4294865587.0
#>>> string2='72b3'
#>>>
#>>> dec_num = sum(int(x, 16) * math.pow(16, len(string2)-i-1) for i, x in enumerate(string2))
#>>> print(dec_num)
#29363.0
#>>> string
#'fffe72b3'
#>>> import ctypes
#>>> x=0xfffe72b3
#>>> 15*(16**7)
#4026531840
#>>> binary_str=bin(int(dec_num))
#>>> binary_str
#'0b111001010110011'
#>>> strip_bin_str=binary_str[2:len(binary_str)]
#>>> strip_bin_str
#'111001010110011'
#>>> flipped=''.join('1' if x=='0' else '0' for x in strip_bin_str)
#>>> flipped
#'000110101001100'
#>>> strip_bin_str
#'111001010110011'
#>>> int(flipped)
#110101001100
#>>> flipped
#'000110101001100'
#>>> int(flipped,2)
#3404
#>>> int('0b'+flipped,2)
#3404


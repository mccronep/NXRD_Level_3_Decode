#!/home/pmccrone/anaconda3/bin/python
# -*- coding: utf-8 -*-
#==============================================================
#
#==============================================================
#
#==-ROC/FRB PYTHON PROGRAM DEFINITION-==========================================
#
#
# NAME:
# :::::::::::::::::::::::::::::::::::::::::::::::
# read_and_process_Exclusion_data_v06.py
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
# Programmer: Mr. Paul McCrone     19 Dec 2023
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

try:
    import datetime
    import time
    #
    import os
    import sys
    import csv
    import metpy
    import pandas as pd
    import cartopy.crs as ccrs
    import matplotlib.gridspec as gridspec
    import matplotlib.pyplot as plt
    import numpy as np
    #
    from math import asin, atan2, cos, degrees, radians, sin
    #
    import metpy
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    #
    from metpy.calc import azimuth_range_to_lat_lon
    from metpy.io import Level3File
    from metpy.plots import add_metpy_logo, add_timestamp, colortables, USCOUNTIES
    from metpy.units import units  
    print('Was able to successfully Load Modules')
    #
except:
    print('There was a problem loading modules.')
#######################################################
#######################################################

degtorad=np.pi/180.0

myargv=sys.argv

print('-------- ')
print(str(len(myargv)))


#
# Get the first argument from the command line.
#
if len(myargv) >=2:
#
    inputfile=sys.argv[1]
    
    print('read in the filename')
else:

    inputfile='Not_defined'
# Variables I will use in all functions:
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DADASH='-----------------------------------------------------'
dadash='-----------------------------------------------------'
dadashes='-----------------------------------------------------'
#
DAEQUALS='==--==--==--==--==--==--==--==--==--==--==--==--==--'
#
DADASHES='----------------------------------------------------'
PRTERR="--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--"
PRTOK='--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--'


 
def printbn():
    #
    print('\n')
    #END OF Function

def printok():
    #
    print(PRTOK)
    #END OF Function

def printerr():
    #
    print(PRTERR)
    #END OF Function

def printds():
    #
    print('--------------------------------------------')
    #END
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}km from initial, in degrees
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    a = radians(bearing)
    lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
    lon2 = lon1 + atan2(
        sin(a) * sin(d/R) * cos(lat1),
        cos(d/R) - sin(lat1) * sin(lat2)
    )
    return (degrees(lat2), degrees(lon2),)
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----




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


print('Input filename is:'+str(inputfile))

fileexists=os.path.isfile(inputfile)
useinputfile=0


if fileexists:
    print("The input file "+str(inputfile)+" exists.")
    useinputfile=1
#            
else:
    print("The input file "+str(inputfile)+" does not exist.")
    useinputfile=0
    
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

thezones=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"," 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9"]

thezonesn=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]





#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
call_signs_3list= \
["GUA","KSG","KJK","ODN","ABR","ENX","ABX","FDR","AMA","AHG", \
"EWX","BBX","ABC","BLX","BGM","BMX","BIS","CBX","BOX","BRO", \
"BUF","CXX","FDX","ICX","CLX","RLX","CYS","LOT","ILN","CLE", \
"CAE","GWX","CRP","FWS","DVN","FTG","DMX","DTX","DDC","DOX", \
"DLH","DYX","EYX","EVX","EPZ","LRX","BHX","APD","FSX","HPX", \
"GRK","POE","EOX","SRX","IWX","APX","GGW","GLD","MVX","GJX", \
"GRR","TFX","GRB","GSP","RMX","UEX","HDX","CBW","HGX","HTX", \
"IND","JKL","DGX","JAX","HKN","EAX","BYX","AKC","MRX","ARX", \
"PLA","LCH","ESX","DFX","ILX","LZK","VTX","LVX","LBB","MQT", \
"MXX","MAX","MLB","NQA","AMX","AIH","MAF","MKX","MPX","MBX", \
"MSX","MOB","HMO","VAX","MHX","OHX","LIX","OKX","AEC","AKQ", \
"LNX","TLX","OAX","PAH","PDT","DIX","IWA","PBZ","SFX","GYX", \
"RTX","PUX","RAX","UDX","RGX","RIW","FCX","JGX","DAX","LSX", \
"MTX","SJT","NKX","MUX","HNX","JUA","SOX","ATX","SHV","FSD", \
"ACG","HKI","HWA","OTX","SGF","CCX","LWX","TLH","TBW","TWX", \
"EMX","INX","VNX","VBX","ICT","LTX","FFC","YUX","LGX"]

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
dict_icao_3ltr= \
        {"GUA":"PGUA","KSG":"RKSG","KJK":"RKJK","ODN":"RODN", \
        "ABR":"KABR","ENX":"KENX","ABX":"KABX","FDR":"KFDR", \
        "AMA":"KAMA","AHG":"PAHG", \
        "EWX":"KEWX","BBX":"KBBX","ABC":"PABC","BLX":"KBLX", \
        "BGM":"KBGM","BMX":"KBMX","BIS":"KBIS","CBX":"KCBX", \
        "BOX":"KBOX","BRO":"KBRO", \
        "BUF":"KBUF","CXX":"KCXX","FDX":"KFDX","ICX":"KICX", \
        "CLX":"KCLX","RLX":"KRLX","CYS":"KCYS","LOT":"KLOT", \
        "ILN":"KILN","CLE":"KCLE", \
        "CAE":"KCAE","GWX":"KGWX","CRP":"KCRP","FWS":"KFWS", \
        "DVN":"KDVN","FTG":"KFTG","DMX":"KDMX","DTX":"KDTX", \
        "DDC":"KDDC","DOX":"KDOX", \
        "DLH":"KDLH","DYX":"KDYX","EYX":"KEYX","EVX":"KEVX", \
        "EPZ":"KEPZ","LRX":"KLRX","BHX":"KBHX","APD":"PAPD", \
        "FSX":"KFSX","HPX":"KHPX", \
        "GRK":"KGRK","POE":"KPOE","EOX":"KEOX","SRX":"KSRX", \
        "IWX":"KIWX","APX":"KAPX","GGW":"KGGW","GLD":"KGLD", \
        "MVX":"KMVX","GJX":"KGJX", \
        "GRR":"KGRR","TFX":"KTFX","GRB":"KGRB","GSP":"KGSP", \
        "RMX":"KRMX","UEX":"KUEX","HDX":"KHDX","CBW":"KCBW", \
        "HGX":"KHGX","HTX":"KHTX", \
        "IND":"KIND","JKL":"KJKL","DGX":"KDGX","JAX":"KJAX", \
        "HKN":"PHKN","EAX":"KEAX","BYX":"KBYX","AKC":"PAKC", \
        "MRX":"KMRX","ARX":"KARX", \
        "PLA":"LPLA","LCH":"KLCH","ESX":"KESX","DFX":"KDFX", \
        "ILX":"KILX","LZK":"KLZK","VTX":"KVTX","LVX":"KLVX", \
        "LBB":"KLBB","MQT":"KMQT", \
        "MXX":"KMXX","MAX":"KMAX","MLB":"KMLB","NQA":"KNQA", \
        "AMX":"KAMX","AIH":"PAIH","MAF":"KMAF","MKX":"KMKX", \
        "MPX":"KMPX","MBX":"KMBX", \
        "MSX":"KMSX","MOB":"KMOB","HMO":"PHMO","VAX":"KVAX", \
        "MHX":"KMHX","OHX":"KOHX","LIX":"KLIX","OKX":"KOKX", \
        "AEX":"PAEC","AKQ":"KAKQ", \
        "LNX":"KLNX","TLX":"KTLX","OAX":"KOAX","PAH":"KPAH", \
        "PDT":"KPDT","DIX":"KDIX","IWA":"KIWA","PBZ":"KPBZ", \
        "SFX":"KSFX","GYX":"KGYX", \
        "RTX":"KRTX","PUX":"KPUX","RAX":"KRAX","UDX":"KUDX", \
        "RGX":"KRGX","RIW":"KRIW","FCX":"KFCX","JGX":"KJGX", \
        "DAX":"KDAX","LSX":"KLSX", \
        "MTX":"KMTX","SJT":"KSJT","NKX":"KNKX","MUX":"KMUX", \
        "HNX":"KHNX","JUA":"TJUA","SOX":"KSOX","ATX":"KATX", \
        "SHV":"KSHV","FSD":"KFSD", \
        "ACG":"PACG","HKI":"PHKI","HWA":"PHWA","OTX":"KOTX", \
        "SGF":"KSGF","CCX":"KCCX","LWX":"KLWX","TLH":"KTLH", \
        "TBW":"KTBW","TWX":"KTWX", \
        "EMX":"KEMX","INX":"KINX","VNX":"KVNX","VBX":"KVBX", \
        "ICT":"KICT","LTX":"KLTX","FFC":"KFFC","YUX":"KYUX", \
        "LGX":"KLGX"}

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

CWD_PATH='/home/pmccrone/test/'

NEX_file=CWD_PATH+'NEXRAD_Data_LL_Data.csv'

#
this_return_value = 0
#
# Check thisfile
#
valid_thisfile=os.path.isfile(NEX_file)
#
if valid_thisfile:
    print(dadash)
    print("This file is VALID and EXISTS:: "+NEX_file)
    this_return_value = 1
    print(dadash)
    WARNING_INIT_ERROR=1
    #
else:
    #
    print("---CAUTION---")
    print("---The indicated file is INVALID! NEED TO CHECK THIS!: "+NEX_file)
    this_return_value = 0
    WARNING_INIT_ERROR=0
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
try:
    nexrad_dataframe = pd.read_csv(CWD_PATH+'NEXRAD_Data_LL_Data.csv')
except:
    WARNING_INIT_ERROR=0
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

print (DADASHES)

#try:
#    nexrad_dataframe.set_index("STATION_ID")
#except:
#    WARNING_INIT_ERROR=0
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

print(DADASHES)
print( "The nexrad_dataframe")
print(DADASHES)
#
try:
    print(nexrad_dataframe)
except:
    WARNING_INIT_ERROR=0
#============================================================

#----------------------------------------------------
#We will print the column names:
#['WBAN' 'STATION_ID' 'STATION_NAME' 'LATN/LONGW(deg,min,sec)' 'ELEV(ft)'
# 'TOWER_HEIGHT(m)' 'TROPICAL' 'COASTAL' 'INLAND' 'LAT_N(deg,min,sec)'
# 'LONG_W(deg,min,sec)' 'STATION_CALLSIGN' 'LONG' 'LAT']
#----------------------------------------------------
#This is the last column - This is its name:
#LAT
#----------------------------------------------------
#

col_wban        =       'WBAN' 
#
col_icao        =       'STATION_ID' 	             # KEY - col_icao
col_sname       =       'STATION_NAME'               # KEY - col_sname
col_ll0         =       'LATN/LONGW(deg,min,sec)' 
#
col_elev        =       'ELEV(ft)'                   # KEY - col_elev
col_thgt        =       'TOWER_HEIGHT(m)' 
col_trop        =       'TROPICAL' 
col_cost        =       'COASTAL' 
col_inla        =       'INLAND' 
col_lata        =       'LAT_N(deg,min,sec)'
col_lona        =       'LONG_W(deg,min,sec)' 
col_call        =       'STATION_CALLSIGN' 
#
col_lon         =       'LONG'                       # Key - col_lon
col_lat         =       'LAT'                        # Key - col_lat


# pandas Get Column Names
# You can get the column names from pandas DataFrame using df.columns.values, 
# and pass this to python list() function to get it as list, once you have the data you can print it using print() statement.
print (DADASHES)
print("We will print the column names:")
print(nexrad_dataframe.columns.values)

# You can also use df.columns.values.tolist() to get the DataFrame column names.
colmn_list=nexrad_dataframe.columns.values.tolist()
num_cols=len(colmn_list)

print (DADASHES)
print("This is the last column - This is its name:")
last_col=colmn_list[num_cols-1]
print(colmn_list[num_cols-1])


## Print all the STATION_ID
#print (DADASHES)
#print("These are the Station Ids:")
#for x in nexrad_dataframe.index:
#    my_station_icao = nexrad_dataframe.loc[x,col_icao]
#    #print(my_station_icao)
#    if "KGSP" in my_station_icao:
#        my_x=x
#        print("WE have KGSP at my_x="+str(x))

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

####..............####
# MAIN part of program
####..............####


now=0
Print_Current_Time(now)

datadirectry='/home/pmccrone/test/'
file='KGSP_SDUS82_DTAGSP_202202271757_SUPPLDATA.txt'

thefile=datadirectry+file

if useinputfile == 1:
    printds()
    print('Attempt to use the file from the command line.')
    printds()
    thefile=inputfile


if os.path.isfile(thefile):
    print(DADASH)
    print('The file is valid- it exists.KGSP_SDUS82_DTAGSP_202202271757_SUPPLDATA.txt.raw.csv ')
    printok()
    fileisvalid=1
else:
    fileisvalid=0
    print("The file does not exist")
    print("We cant process.")
    printerr()


#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# 
# lines contains the entire file.
print("This is the entire file")

if fileisvalid ==1:
    with open(thefile) as f:
        lines =  f.readlines()
    #
    f.close()
    count=len(lines[0])

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# 

lenlines=len(lines)

printok()
print('length of lines or number of lines in the file are: '+str(lenlines))



start=[]
dpl=[]
ii=0

radar_list=[]
excl_zonesl=[]

find_zone='ZONE BEG AZM END AZM'
radarposition="RADAR ID:"
dp='DUAL POL EXCLUSION'
num_excl_zone='NUMBER OF EXCLUSION ZONES'


for line in lines:
    ii=ii+1    
    if find_zone in line:
        start.append(ii)
    
    if dp in line:
        dpl.append(ii)

    if radarposition in line:
        radar_list.append(ii)

    if num_excl_zone in line:
       excl_zonesl.append(ii) 

 
#----- End of the for loop

# We will get the radar 4 letter identifer, with the 
# date and time of the file.

lenstart=len(start)

len_dpl=len(dpl)

radar1=radar_list[0]
radara=lines[radar1-1]

print(DADASH)
print('Radar line')
print(radara)
print(DADASH)

#00000000001111111111222222222233333333334444444444
#01234567890123456789012345678901234567890123456789
#RADAR ID: KGSP     DATE: 02/27/22     TIME: 17:57                               

radar_icao=radara[10:14]
radar_date=radara[25:33]
radar_time=radara[44:49]

printok()
printbn()
print("Radar Site: "+str(radar_icao))
print("Event Date: "+str(radar_date))
print("Event Time: "+str(radar_time))

printok()

#nexrad_dataframe['STATION_ID']
#nexrad_dataframe.loc[[radar_icao]]


# Print all the STATION_ID
print (DADASHES)
print("Looking for data connected with our NEXRAD :")
print (DADASHES)

for x in nexrad_dataframe.index:
    my_station_icao = nexrad_dataframe.loc[x,col_icao]
    #print(my_station_icao)
    if radar_icao in my_station_icao:
        my_x=x
        print("WE have "+str(radar_icao)+" at my_x="+str(x))

#
# Get radar lat lon
#
radar_lon=nexrad_dataframe.loc[my_x,col_lon]

radar_lat=nexrad_dataframe.loc[my_x,col_lat]


radar_name=nexrad_dataframe.loc[my_x,col_sname]


print('Latitude of  '+radar_icao+' is '+str(radar_lat))
print('Longitude of '+radar_icao+' is '+str(radar_lon))

print(DADASH+"\n"+"Radar ICAO "+str(radar_icao)+" is located at "+str(radar_name)+'\n'+str(DADASH))     


# Next we need to get the number of exclusion zones

numberofexzones=0

loc_zones=excl_zonesl[0]
line_zones=lines[loc_zones-1]

print(DADASH)
print('Exclusion Zone line')
print(line_zones)
print(DADASH)

#00000000001111111111222222222233333333334444444444555555555566666666667777777777
#01234567890123456789012345678901234567890123456789012345678901234567890123456789
#MAX RATE                    200.00 MM/HR NUMBER OF EXCLUSION ZONES    17

str_numberofexzones=line_zones[70:72]

numberofexzones=int(str_numberofexzones)

printok()
printbn()

print('Number of Exclusion Zones: '+str(str_numberofexzones)) 

printok()

# I am assuming there is exclusion zone data at this point.
# Now the start of the data is the first list item in start.
# I will keep going until we get a space or blank in my_zone.

blank=''
space=' '
spaces2='  '
spaces3='   '

my_start1=start[0]
if len_dpl > 1:
    my_stop1=dpl[1]
else:
    my_stop1=lenlines

indx=my_start1
first_line=lines[indx]

#
#             ZONE BEG AZM END AZM BEG RNG (NM) END RNG (NM) ELEV ANG            
#               1  229.0   233.0        4            6          1.0     
#00000000001111111111222222222233333333334444444444555555555566666666667         
#01234567890123456789012345678901234567890123456789012345678901234567890
#
my_zone=first_line[14:16] #2
beg_az =first_line[18:23] #5
end_az =first_line[26:31] #5
beg_rng=first_line[38:40] #2
end_rng=first_line[51:53] #2
ele_ang=first_line[62:66] #4

print(".......................................................")
print("my_zone - beg_az - end_az - beg_rng - end_rng - ele_ang")
print(".......................................................")

largestring=my_zone +"      - "+beg_az+"  - "+end_az+"  -   "+beg_rng+"   -    "+end_rng+"      - "+ele_ang
print(largestring)

zone_list=[]
baz_list=[]
eaz_list=[]
brng_list=[]
erng_list=[]
eang_list=[]

zone_list.append(my_zone)
baz_list.append(beg_az)
eaz_list.append(end_az)
brng_list.append(beg_rng)
erng_list.append(end_rng)
eang_list.append(ele_ang)

looper=1

while(looper == 1):
    indx=indx+1
    first_line=lines[indx]
    #
    my_zone=first_line[14:16]
    beg_az =first_line[18:23]
    end_az =first_line[26:31]
    beg_rng=first_line[38:40]
    end_rng=first_line[51:53]
    ele_ang=first_line[62:66]
    largestring=my_zone +"      - "+beg_az+"  - "+end_az+"  -   "+beg_rng+"   -    "+end_rng+"      - "+ele_ang
    print(largestring)
    #
    if (my_zone == blank) or (my_zone == space) or (my_zone == spaces2):
        print("End of first group: look for next group") 
        looper=0
    else:
         #
         zone_list.append(my_zone)
         baz_list.append(beg_az)
         eaz_list.append(end_az)
         brng_list.append(beg_rng)
         erng_list.append(end_rng)
         eang_list.append(ele_ang)
    #
    if (indx == my_stop1):
        print("End of first group: look for next group") 
        looper=0

# End of first while loop.

## We will read the second group
#if numberofexzones >= 14:
if lenstart > 1:
    # Only  go to the next group if there is another group. 
    
    my_start2=start[1]
    #my_stop1=dpl[2]
    indx=my_start2
    first_line=lines[indx]


print(".......................................................")
print("my_zone - beg_az - end_az - beg_rng - end_rng - ele_ang")
print(".......................................................")


# This is the second while loop
looper=1

while(looper == 1):
    #
    my_zone=first_line[14:16]
    beg_az =first_line[18:23]
    end_az =first_line[26:31]
    beg_rng=first_line[38:40]
    end_rng=first_line[51:53]
    ele_ang=first_line[62:66]
    #
    largestring=my_zone +"      - "+beg_az+"  - "+end_az+"  -   "+beg_rng+"   -    "+end_rng+"      - "+ele_ang
    print(largestring)
    #
    if (my_zone == blank) or (my_zone == space) or (my_zone == spaces2):
        print("End of last group: look for next group") 
        looper=0
    else:
         #
         zone_list.append(my_zone)
         baz_list.append(beg_az)
         eaz_list.append(end_az)
         brng_list.append(beg_rng)
         erng_list.append(end_rng)
         eang_list.append(ele_ang)
    #
    if (indx == my_stop1):
        print("End of last group: look for next group") 
        looper=0
    #
    if looper == 1:
      indx=indx+1
      first_line=lines[indx]
# End of final while loop.

# Make csv the file

csvfile=thefile+".raw.csv"

print(DADASH)
print("Making the raw CSV file without geo navigation, file name is:"+str(csvfile))
print(DADASH)

with open(csvfile, 'w', newline='') as filecsv:
    writer = csv.writer(filecsv)
    csvfield = ["my_zone","beg_az","end_az","beg_rng","end_rng","ele_ang"]
    writer.writerow(csvfield)
    ii=0
    for item in zone_list:
        stritem=str(item)
        if stritem in thezones:
            writer.writerow([zone_list[ii], baz_list[ii], eaz_list[ii], brng_list[ii], erng_list[ii], eang_list[ii] ]) 
            ii=ii+1
# End of writing csv file (raw) 


ii=0


# This part determines the max range for plotting. If there are cells over 100 km away, we include them.
# If there is a cell over 460 km away, we will not plot it, it is not in the range of the radar. 
# So 460 km is the greatest range allowed.
# Note we will at least plot 300 km.

mx_c_rng=float(max(erng_list))*1.852

print('maximum rng= '+str(mx_c_rng))

maxrange=100.0 # km

if mx_c_rng > maxrange:
    maxrange = mx_c_rng+20.0

if maxrange > 460.0:
    maxrange = 460.0

# This ends the max range part.


# Now we plot the data
#real_lat_radar 
#real_lon_radar

cent_lon = radar_lon
cent_lat = radar_lat

fig = plt.figure(figsize=(15, 15))
add_metpy_logo(fig, 190, 85, size='large')

ctables = (('NWSStormClearReflectivity', -20, 0.5),  # dBZ
           ('NWS8bitVel', -100, 1.0))  # m/s


### Plot the data
crs=ccrs.PlateCarree()
#crs=ccrs.LambertConformal(central_longitude=cent_lon, central_latitude=real_lat_radar)
ax = fig.add_subplot(1,1,1, projection=crs)

# Plot North, south, east and west points in red at a range of 150km.

xln, yln = azimuth_range_to_lat_lon(0, 150000, cent_lon, cent_lat)
xls, yls = azimuth_range_to_lat_lon(180, 150000, cent_lon, cent_lat)
xle, yle = azimuth_range_to_lat_lon(90, 150000, cent_lon, cent_lat)
xlw, ylw = azimuth_range_to_lat_lon(270, 150000, cent_lon, cent_lat)

ax.plot(xln,yln, color='red', marker= 'o', label='N',markersize=12)
ax.plot(xls,yls, color='red', marker= 'o', label='N',markersize=12)
ax.plot(xle,yle, color='red', marker= 'o', label='N',markersize=12)
ax.plot(xlw,ylw, color='red', marker= 'o', label='N',markersize=12)
ax.text(xln,yln, "N", color='black')
ax.text(xls,yls, "S", color='black')
ax.text(xle,yle, "E", color='black')
ax.text(xlw,ylw, "W", color='black')

plt.plot(xln,yln, xls,yls, color="black", linewidth=3)

# Plot North, south, east and west lines in black out to 150 km.

rrnngg=range(0,150000,1000)

for r in rrnngg:
    xlx, ylx = azimuth_range_to_lat_lon(0, r, cent_lon, cent_lat)
    ax.plot(xlx,ylx, color='black', marker= 'o', markersize=1)
    xlx, ylx = azimuth_range_to_lat_lon(180, r, cent_lon, cent_lat)
    ax.plot(xlx,ylx, color='black', marker= 'o', markersize=1)
    xlx, ylx = azimuth_range_to_lat_lon(90, r, cent_lon, cent_lat)
    ax.plot(xlx,ylx, color='black', marker= 'o', markersize=1)
    xlx, ylx = azimuth_range_to_lat_lon(270, r, cent_lon, cent_lat)
    ax.plot(xlx,ylx, color='black', marker= 'o', markersize=1)

# plot range rings (black) at 50 and 100 km

r50=50000
r100=100000

aannggllee=range(0,360)
for a in aannggllee:
    xlx, ylx = azimuth_range_to_lat_lon(a, r50, cent_lon, cent_lat)
    ax.plot(xlx,ylx, color='black', marker= 'o', markersize=1)
    xlx, ylx = azimuth_range_to_lat_lon(a, r100, cent_lon, cent_lat)
    ax.plot(xlx,ylx, color='black', marker= 'o', markersize=1)
     
# This is the radar location

xlr, ylr = azimuth_range_to_lat_lon(0, 0, cent_lon, cent_lat)

ax.plot(xlr,ylr, color='purple', marker= 'o', label=str(radar_icao), markersize=19)
ax.plot(xlr,ylr, color='white', marker= 'o', label=str(radar_icao), markersize=9)

# This places the radar ICAO in large letters on the map with an arrow pointing to the location.

ax.annotate(radar_icao, xy=(xlr, ylr),  xytext=(0.25, 0.25), textcoords='figure fraction', \
    arrowprops=dict(facecolor='purple', shrink=0.05), \
    horizontalalignment='left', \
    verticalalignment='bottom', fontsize=16)

R=6371.0
#
nm2km=1.852
#
ii=0
#
lat_a=[]
lat_b=[]
lat_c=[]
lat_d=[]
#
lon_a=[]
lon_b=[]
lon_c=[]
lon_d=[]
#
for item in zone_list:

    angl=float(baz_list[ii])#*degtorad
    rng=float(brng_list[ii])*nm2km
    xlo, ylo = azimuth_range_to_lat_lon(angl, rng, cent_lon, cent_lat)
    lat2, lon2 = get_point_at_distance(cent_lat, cent_lon, rng, angl)
    lat_a.append(lat2)
    lon_a.append(lon2)
    #
    angl2=float(eaz_list[ii])#*degtorad
    rng2=float(erng_list[ii])*nm2km
    xlob, ylob = azimuth_range_to_lat_lon(angl2, rng2, cent_lon, cent_lat)
    lat2b, lon2b = get_point_at_distance(cent_lat, cent_lon, rng2, angl2)
    lat_b.append(lat2b)
    lon_b.append(lon2b)
    #
    lat2c, lon2c = get_point_at_distance(cent_lat, cent_lon, rng, angl2)
    lat_c.append(lat2c)
    lon_c.append(lon2c)
    #
    lat2d, lon2d = get_point_at_distance(cent_lat, cent_lon, rng2, angl)
    lat_d.append(lat2d)
    lon_d.append(lon2d)
    #
    latlist=[lat2, lat2c, lat2b, lat2d, lat2]
    lonlist=[lon2, lon2c, lon2b, lon2d, lon2]

    ax.plot(lonlist, latlist, 'o-', color='black')

    ax.plot(xlo, ylo, 'o-', color='black')
    ax.plot(xlob, ylob, 'o-', color='black')

    ax.fill(lonlist, latlist, 'o-', color='orange')

    ax.plot(lon2c,lat2c,'o', label=item, color='black', transform=ccrs.Geodetic())

    #angl=float(curr_az[ii])
    #rng=float(curr_range[ii])*nm2km
    #xlo, ylo = azimuth_range_to_lat_lon(angl, rng, cent_lon, cent_lat)
    #lat2, lon2 = get_point_at_distance(cent_lat, cent_lon, rng, angl)
    ax.plot(lon2,lat2,'o', label=item, color='blue', transform=ccrs.Geodetic())
    #
    print('xlo='+str(xlo)+'  ylo='+str(ylo))
    #
    print('lon2='+str(lon2)+'  lat2='+str(lat2))
     
    print("The Zone  is:"+str(zone_list[ii]))   
    ax.text(lon2,lat2, item ,horizontalalignment='center', verticalalignment='bottom')
    ii=ii+1

#xlocs, ylocs = azimuth_range_to_lat_lon(az, rng, cent_lon, cent_lat)
ax.add_feature(USCOUNTIES, linewidth=0.5)
ax.set_extent([cent_lon-1.5, cent_lon+1.5, cent_lat-1.5, cent_lat+1.5])
ax.set_aspect('equal', 'datalim')
# Put a background image on for nice sea rendering.
ax.stock_img()

# Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')

SOURCE = 'Natural Earth'
LICENSE = 'public domain'
ax.add_feature(states_provinces, edgecolor='gray')
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.LAND)


# Make processed csv the file

pcsvfile=thefile+".proc.csv"

print(DADASH)
print("Making the updated CSV file With geo-navigation, file name is:"+str(pcsvfile))
print(DADASH)

with open(pcsvfile, 'w', newline='') as filecsv:
    writer = csv.writer(filecsv)
    csvfield = ["my_zone","beg_az","end_az","beg_rng","end_rng","ele_ang", "radar_lat", "radar_lon","lat","long","lat_b","lon_b","lat_c","lon_c","lat_d","lon_d"]
    writer.writerow(csvfield)
    ii=0
    for item in zone_list:
        stritem=str(item)
        if stritem in thezones:
            writer.writerow([zone_list[ii],baz_list[ii],eaz_list[ii],brng_list[ii],erng_list[ii], \
                eang_list[ii],cent_lat,cent_lon,lat_a[ii],lon_a[ii],lat_b[ii],lon_b[ii],lat_c[ii],lon_c[ii],lat_d[ii],lon_d[ii] ]) 
            ii=ii+1
# end of making the processed CSV.
#
printok()
print("The processed csv file was made. The file name is: "+str(pcsvfile))
printok()


#

# Make the kml file
makekml =1

kml_filemain=thefile+".proc_Exclusion.kml"


if makekml ==1:
    printok()
    #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Now we make the KML file.
    ff=open(kml_filemain, "w+")
    ff.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    ff.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    ff.write("  <Document>\n")
    ii=0
    for item in zone_list:
        stritem=str(item)
        if stritem in thezones: 
            ff.write("    <Placemark>\n")
            ff.write("      <name>" + str(zone_list[ii]) + "</name>\n")
            ff.write("      <description>" + str(zone_list[ii]) + "</description>\n")
            ff.write("      <Point>\n")
            ff.write("        <coordinates>"+str(lon_a[ii])+","+str(lat_a[ii])+"</coordinates>\n")
            ff.write("      </Point>\n")
            ff.write("    </Placemark>\n")
            #
            ff.write("    <Placemark>\n")
            ff.write("      <name>" + str(zone_list[ii])+'(b)'+ "</name>\n")
            ff.write("      <description>" + str(zone_list[ii])+'(b)'+ "</description>\n")
            ff.write("      <LineString>\n")
            ff.write("          <coordinates>\n")
            ff.write("          "+str(lon_a[ii])+","+str(lat_a[ii])+",0\n")
            ff.write("          "+str(lon_c[ii])+","+str(lat_c[ii])+",0\n")
            ff.write("          "+str(lon_b[ii])+","+str(lat_b[ii])+",0\n")
            ff.write("          "+str(lon_d[ii])+","+str(lat_d[ii])+",0\n")
            ff.write("          "+str(lon_a[ii])+","+str(lat_a[ii])+",0\n")
            ff.write("          </coordinates>\n") #  </coordinates>
            ff.write("      </LineString>\n")      #   </LineString>
            ff.write("    </Placemark>\n")
            #
            #ff.write("    <Style>\n") 
            #ff.write("      <LineStyle>\n")  
            #ff.write("        <color>#ff0000ff</color>\n")
            #ff.write("        <width>5</width>\n")
            #ff.write("      </LineStyle>\n") 
            #ff.write("    </Style>\n")
            ii=ii+1
        #
     # 
    ff.write("  </Document>\n")
    ff.write("</kml>\n")
    ff.close()

#plot the python map of the information.
plt.show()

###The KML code for the simple placemark looks like this:
#
#<?xml version="1.0" encoding="UTF-8"?>
#<kml xmlns="http://www.opengis.net/kml/2.2">
#  <Placemark>
#    <name>Simple placemark</name>
#    <description>Attached to the ground. Intelligently places itself 
#       at the height of the underlying terrain.</description>
#    <Point>
#      <coordinates>-122.0822035425683,37.42228990140251,0</coordinates>
#    </Point>
#  </Placemark>
#</kml>
#





#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# END
#
#......................
#                        STORM TOTAL ACCUMULATION                                
#                                                                                
#RADAR ID: KGSP     DATE: 02/27/22     TIME: 17:57                               
#VOLUME COVERAGE PATTERN: 215            MODE: Precip                            
#GAGE BIAS APPLIED                        -    NO                                
#     BIAS  ESTIMATE                      -      N/A                             
#     EFFECTIVE # G/R PAIRS               -      N/A                             
#     MEMORY SPAN (HOURS)                 -      N/A                             
#     DATE/TIME LAST BIAS UPDATE          -      N/A                             
#HYBRID RATE PERCENT BINS FILLED          -    99.53                             
#            HIGHEST ELEV. USED (DEG)     -     6.4                              
#            TOTAL PRECIP AREA (KM**2)    - 27698.3                              
#AWIPS SITE ID OF MOST RECENT BIAS SOURCE -   N/A                                
#R(A) STATUS                              - ON                                   
#R(A) MODE                                - STRATIFORM (0.035)                   
#R(A) ALPHA                               - 0.035                                
#NUMBER OF DATA BINS TO COMPUTE ALPHA     -    25145                             
#
#DEFAULT MELTING LAYER DEPTH   0.5 KM     MAX KDP BEAM BLOCKAGE        70 %      
#MELTING LAYER SOURCE     MODEL_ENHANCED  MIN KDP USAGE RATE           10.0 MM/HR
#KDP COEFFICIENT              44          WET SNOW R(Z) MULTIPLIER      0.6      
#KDP EXPONENT                  0.822      GRAUPEL R(Z) MULTIPLIER       0.8      
#KDP COEFF FOR RAIN/HAIL      27          RAIN/HAIL R(Z) MULTIPLIER     0.8      
#Z-R COEFFICIENT             300          DRY SNOW BELOW ML TOP MULT.   1.0      
#Z-R EXPONENT                  1.4        DRY SNOW R(Z) MULTIPLIER      2.8      
#RAIN RATE RELATIONSHIP TYPE CONTINENTAL  CRYSTALS R(Z) MULTIPLIER      2.8      
#ZDR/Z COEFFICIENT             0.0142     HVY RAIN REFL THRESH R(KDP)  45.0 dBZ  
#ZDR/Z EXPONENT FOR Z          0.770      % RATE GRID FILLED THRESH    99.9 %    
#ZDR/Z EXPONENT FOR ZDR       -1.67       PAIF PRECIP RATE THRESH       0.5 MM/HR
#MIN CORREL COEFF FOR PRECIP   0.8000     PAIF PRECIP AREA THRESH     200   KM**2
#MIN CORREL COEFF FOR KDP      0.9000     USE LOW SUPPLEMENTAL SCAN   YES        
#MAX REFLECTIVITY             53.0 dBZ    MAX VOLUMES PER HOUR         30        
#MAX RATE                    200.00 MM/HR NUMBER OF EXCLUSION ZONES    17        
#
#THRESHOLD ELAPSED TIME TO RESTART      60 MINUTES                               
#MAXIMUM TIME FOR INTERPOLATION         30 MINUTES                               
#MAXIMUM HOURLY ACCUMULATION VALUE     800 MM                                    
#TIME BIAS ESTIMATION                   50 MINUTES                               
#THRESHOLD NUMBER OF GAGE-RADAR PAIRS   10                                       
#RESET BIAS VALUE                        1.0                                     
#LONGEST ALLOWABLE LAG                 168 HOURS                                 
#BIAS FLAG APPLIED?                     NO                                       
#RPG ESTIMATED ISDP                     58 DEG                                   
#ISDP APPLIED TO DATA?                  NO                                       
#DATE OF ISDP ESTIMATE:           02/27/22                                       
#TIME OF ISDP ESTIMATE:              03:51                                       
#METSIGNAL PROCESSING:                  ON                                       
#METSIGNAL THRESHOLD:                   80.0                                     
#CAPPI PROCESSING:                      ON                                       
#CAPPI THRESHOLD:                       11.0 dBZ                                 
#CAPPI HEIGHT:                           3.0 KM                                  
#
#                            DUAL POL EXCLUSION ZONES                            
#                                                                                
#             ZONE BEG AZM END AZM BEG RNG (NM) END RNG (NM) ELEV ANG            
#               1  229.0   233.0        4            6          1.0              
#               2   13.0    14.0       75           76          1.0              
#               3   12.0    13.0       55           57          1.0              
#               4    5.0     6.0       14           15          1.0              
#               5    6.0     7.0       33           35          1.0              
#               6   25.0    26.0       16           18          1.0              
#               7   61.0    63.0       10           11          1.0              
#               8  114.0   116.0       11           12          1.0              
#               9  120.0   122.0       10           11          1.0              
#              10  129.0   130.0       17           18          1.0              
#              11  156.0   157.0       12           13          1.0              
#              12  193.0   194.0       18           19          1.0              
#              13  212.0   214.0        9           11          1.0              
#              14  234.0   236.0        7            8          1.0              
#
#                            DUAL POL EXCLUSION ZONES                            
#                                                                                
#             ZONE BEG AZM END AZM BEG RNG (NM) END RNG (NM) ELEV ANG            
#              15   63.0    65.0       21           24          1.0              
#              16  139.0   140.0       28           29          1.0              
#              17  157.0   159.0       22           23          1.0              
#
#
#

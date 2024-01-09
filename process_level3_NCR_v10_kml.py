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
# process_level3_NCR_v6_kml.py
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
    import csv
    #
    from metpy.calc import azimuth_range_to_lat_lon
    from metpy.io import Level3File
    from metpy.plots import add_metpy_logo, add_timestamp, colortables, USCOUNTIES
    from metpy.units import units
    from math import asin, atan2, cos, degrees, radians, sin
    #
    import cartopy.feature as cfeature
    #
    print('Was able to successfully Load Modules')
    #
except:
    print('There was a problem loading modules.')
#######################################################

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

degtorad=np.pi/180.0

DADASH='-----------------------------------------------------'
dadash='-----------------------------------------------------'
dadashes='-----------------------------------------------------'
#
DAEQUALS='==--==--==--==--==--==--==--==--==--==--==--==--==--'
#
DADASHES='----------------------------------------------------'
PRTERR="--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--"
PRTOK='--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--'

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
#
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

prod_sbn=["NCR","NVW","N0S","NVL","NST","APR","FTM","N1P","NTP","DPA", "NBU","N2U","N3U","DVL","EET", \
        "DSP","NMD","NXB","NYB","NZB","N0B","N1B","NBB","N2B","N3B","NXG","NYG","NZG","N0G","NAG","N1G", \
        "NXX","NYX","NZK","N0X","NAX","N1X","NBX","N2X","N3X","NXC","NYC","NZC","N0C","NAC","N1C","NBC", \
        "N2C","N3C","NXK","NYK","NZK","N0K","NAK","N1K","NBK","N2K","N3K","NXH","NYH","NZH","N0H","NAH", \
        "N1H","NBH","N2H","N3H","NXM","NYM","NZM","N0M","NAM","N1M","NBM","N2M","N3M","OHA","DAA","DTA", \
        "DU3","DU6","HHC","DPR","TZ0","TZ1","TZ2","TV0","TV1","TV2","TZL","NXQ","NYQ","NZQ","N0Q","NAQ", \
        "N1Q","NBQ","N2Q","N3Q","N0R","N1R","N2R","N3R","N0Z","NCZ","N0V","N1V","N2V","N3V","NXU","NYU", \
        "NZU","N0U","N1U","NBU","N2U","N3U","N0S","N1S","N2S","N3S" ]

dict_product_sbn={"NCR":"Short Range Composite Reflectivity 16 level/0.54 nm... 230km","NCZ":"Long Range Composite Reflectivity 16 level/0.54 nm... 460km", \
        "NVW":"Velocity Azimuth Display Wind Profile","N0S":"Storm-Relative Mean Radial Velocity ... 0.5 degrees", \
        "NVL":"Vertically Integrated Liquid","NST":"Storm Cell Identification (Storm Tracking Information)", \
        "APR":"Layer Composite Reflectivity APR 8 level-2.2 nm","FTM":"Free Text Message", \
        "N1P":"(Legacy) One-Hour Rainfall Accumulation","NTP":"Storm Total Rainfall Accumulation", \
        "DPA":"Legacy Hourly Digital Precipitation Array","NBU":"Reflectivity", \
        "N2U":"Reflectivity","N3U":"Reflectivity", \
        "DVL":"High Resolution Digital Vertically Integrated Liquid","EET":"High Resolution Enhanced Echo Tops", \
        "DSP":"Storm Total Rainfall Accumulation","NMD":"Mesocyclone Detection Product", \
        "NXB":"Base Reflectivity –248 nmi Range 256 level -0.13 nm","NYB":"Base Reflectivity –248 nmi Range 256 level -0.13 nm", \
        "NZB":"Base Reflectivity –248 nmi Range 256 level -0.13 nm","N0B":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 0.5 degrees", \
        "N1B":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 1.5 degree","NBB":"Base Reflectivity –248 nmi Range 256 level -0.13 nm", \
        "N2B":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 2.4 degrees","N3B":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 3.4 degrees", \
        "NXG":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm","NYG":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm", \
        "NZG":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm","N0G":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm... 0.5 degrees", \
        "NAG":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm... 0.9 degrees","N1G":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm... 1.5 degree", \
        "NXX":"Differential Reflectivity Data Array Product 256 level-0.13 nm","NYX":"Differential Reflectivity Data Array Product 256 level-0.13 nm", \
        "NZK":"Differential Reflectivity Data Array Product 256 level-0.13 nm","N0X":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 0.5 degrees", \
        "NAX":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 0.9 degrees","N1X":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 1.5 degrees", \
        "NBX":"Differential Reflectivity Data Array Product 256 level-0.13 nm","N2X":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 2.4 degrees", \
        "N3X":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 3.4 degrees","NXC":"Correlation Coefficient Data Array Product 256 level-0.13 nm", \
        "NYC":"Correlation Coefficient Data Array Product 256 level-0.13 nm","NZC":"Correlation Coefficient Data Array Product 256 level-0.13 nm", \
        "N0C":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 0.5 degrees","NAC":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 0.9 degrees", \
        "N1C":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 1.5 degrees","NBC":"Correlation Coefficient Data Array Product 256 level-0.13 nm", \
        "N2C":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 2.4 degrees","N3C":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 3.4 degrees", \
        "NXK":"Specific Differential Phase 256 level -0.13 nm","NYK":"Specific Differential Phase 256 level -0.13 nm", \
        "NZK":"Specific Differential Phase 256 level -0.13 nm","N0K":"Specific Differential Phase 256 level -0.13 nm... 0.5 degrees", \
        "NAK":"Specific Differential Phase 256 level -0.13 nm... 0.9 degrees","N1K":"Specific Differential Phase 256 level -0.13 nm... 1.5 degrees", \
        "NBK":"Specific Differential Phase 256 level -0.13 nm","N2K":"Specific Differential Phase 256 level -0.13 nm... 2.4 degrees", \
        "N3K":"Specific Differential Phase 256 level -0.13 nm... 3.4 degrees","NXH":"Digital Hydrometeor Classification 256 level-0.13 nm", \
        "NYH":"Digital Hydrometeor Classification 256 level-0.13 nm","NZH":"Digital Hydrometeor Classification 256 level-0.13 nm", \
        "N0H":"Digital Hydrometeor Classification 256 level-0.13 nm... 0.5 degrees","NAH":"Digital Hydrometeor Classification 256 level-0.13 nm... 0.9 degrees", \
        "N1H":"Digital Hydrometeor Classification 256 level-0.13 nm... 1.5 degrees","NBH":"Digital Hydrometeor Classification 256 level-0.13 nm", \
        "N2H":"Digital Hydrometeor Classification 256 level-0.13 nm... 2.4 degrees","N3H":"Digital Hydrometeor Classification 256 level-0.13 nm... 3.4 degrees", \
        "NXM":"Melting Layer Contour: 4 contour-0.13 nm","NYM":"Melting Layer Contour: 4 contour-0.13 nm", \
        "NZM":"Melting Layer Contour: 4 contour-0.13 nm","N0M":"Melting Layer Contour: 4 contour-0.13 nm... 0.5 degrees", \
        "NAM":"Melting Layer Contour: 4 contour-0.13 nm... 0.9 degrees","N1M":"Melting Layer Contour: 4 contour-0.13 nm... 1.5 degrees", \
        "NBM":"Melting Layer Contour: 4 contour-0.13 nm","N2M":"Melting Layer Contour: 4 contour-0.13 nm... 2.4 degrees", \
        "N3M":"Melting Layer Contour: 4 contour-0.13 nm... 3.4 degrees","OHA":"Dual Pol One-Hour Accumulation", \
        "DAA":"Digital Accumulation Array","DTA":"Dual Pol Storm Total Accumulation", \
        "DU3":"Digital User-Selectable Accumulation 3 hour","DU6":"Digital User-Selectable Accumulation 24 hour", \
        "HHC":"Hybrid Hydrometeor Classification 256 Level -0.13","DPR":"Digital Instantaneous Precipitation Rate 65536 Level -0.13 nm", \
        "TZ0":"TDWR Base Reflectivity – 48 nmi Range","TZ1":"TDWR Base Reflectivity – 48 nmi Range", \
        "TZ2":"TDWR Base Reflectivity – 48 nmi Range","TV0":"TDWR Base Radial Velocity - 48 nmi Range", \
        "TV1":"TDWR Base Radial Velocity - 48 nmi Range","TV2":"TDWR Base Radial Velocity - 48 nmi Range", \
        "TZL":"TDWR Long Range Reflectivity – 225 nmi Range 186-DR SDUS5i cccc", \
        "N0Q":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 0.5 degree ", \
        "N1Q":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 1.5 degree ","NBQ":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 1.8 degree ", \
        "N2Q":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 2.4 degree ","N3Q":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 3.4 degree ", \
        "NYQ":"Base Reflectivity –248 nmi Range 256 level -0.13 nm","NAQ":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 0.9 degree", \
        "NZQ":"Base Reflectivity –248 nmi Range 256 level -0.13 nm","NOZ":"Long Range Base Reflectivity (460 km)" , \
        "NOR":"Short Range Base Reflectivity (230 km) 0.5 degrees","N1R":"Short Range Base Reflectivity (230 km) 1.5 degrees", \
        "N2R":"Short Range Base Reflectivity (230 km) 2.4 degrees","N3R":"Short Range Base Reflectivity (230 km) 3.4 degrees", \
        "NOV":"Base Velocity (230 km) 0.5 degrees","N1V":"Base Velocity (230 km) 1.5 degrees", \
        "N2V":"Base Velocity (230 km) 2.4 degrees","N3V":"Base Velocity (230 km) 3.4 degrees", \
        "NOU":"Base Velocity (230 km) 0.5 degrees","NAU":"Base Velocity (230 km)... 0.9 degrees", \
        "N1U":"Base Velocity (230 km) 1.5 degrees","NBU":"Base Velocity (230 km) 1.8 degrees", \
        "N2U":"Base Velocity (230 km) 2.4 degrees","N3U":"Base Velocity (230 km) 3.4 degrees", \
        "NXU":"Base Velocity (230 km) -0.5 to-0.1 degrees","NYU":"Base Velocity (230 km) 0.0 to 0.2 degrees", \
        "NZU":"Base Velocity (230 km) 0.3 to 0.4 degrees", \
        "N1S":"Storm Relative Velocity (16 level 230 km)... 1.5 degrees", \
        "N2S":"Storm Relative Velocity (16 level 230 km)... 2.4 degrees", "N3S":"Storm Relative Velocity (16 level 230 km)... 3.4 degrees" }

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

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
####### Begin get_point_at_distance
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
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
    #### END OF get_point_at_distance FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----




########
# MAIN part of program
########

now=0
Print_Current_Time(now)

datadirectry='/home/pmccrone/test/'
file='KFDR_SDUS84_NCRFDR_202205050336.txt'
l3file='KFDR_SDUS84_NCRFDR_202205050336'
pdbfile='KFDR_SDUS84_NCRFDR_202205050336.pdb.ascii'
odfile='KFDR_SDUS84_NCRFDR_202205050336.odout.ascii'

thefile=datadirectry+file

if useinputfile == 1:
    printds()
    print('Attempt to use the file from the command line.')
    printds()
    l3file=inputfile
    pdbfile=inputfile+'.pdb.ascii'
    thefile=inputfile+'txt'
    odfile=inputfile+'.odout.ascii'

if os.path.isfile(thefile):
    os.system('rm -rf '+thefile)
    os.system('rm -rf *txt *.ascii')
    print("removed file")
    print('removed the txtfile and the ascii files')
    printok()

else:
    print("The file has not been made")

#Level3File We will ensure that l3file is Level 3. We are using the metpy Level3File reader to see if it is level 3.
#We are not otherwise using the metpy reader here, it is only to ensure that it is level 3. 
try:
    read_l3file=Level3File(l3file)
    print('This is a valid level 3')
    printok()
except:
    printds()
    print('ERROR: This is NOT a valid level 3 file!')
    printds()

#xxd -s 0 -l 218450 -c 30  KFDR_SDUS84_NSTFDR_202205050336 >> KFDR_SDUS84_NSTFDR_202205050336.hex
if useinputfile ==0:
    print('Make default files')
    os.system('xxd -s 0 -l 218450 -c 30 '+datadirectry+l3file+' >> '+datadirectry+file)
    # making the PRODUCT DESCRIPTION BLOCK
    os.system('xxd -s 48 -l 120 -c 30 '+datadirectry+l3file+' >> '+datadirectry+pdbfile)
    # making the tabular data for NST only
    os.system('od -S 0 '+datadirectry+l3file+' | grep / >> '+datadirectry+odfile)
    printok()
else:
    print('-------')
    print('Make ascii and text data')
    os.system('xxd -s 0 -l 218450 -c 30 '+l3file+' >> '+thefile   )
    # making the PRODUCT DESCRIPTION BLOCK
    os.system('xxd -s 48 -l 120 -c 30 '+l3file+' >> '+pdbfile  )
    # making the tabular data for NST only
    os.system('od -S 0 '+l3file+' | grep / >> '+odfile   )

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
mypdbfile=datadirectry+pdbfile
if useinputfile ==1:
    mypdbfile=pdbfile

with open(mypdbfile) as ff:
    plines=  ff.readlines()

ff.close()
#

for pli in plines:
    print(pli)

# Now we will get the ascii data (this is for NST only)
printds()
print("This is for the ascii tabular data for NST only")

myodfile=datadirectry+odfile
if useinputfile ==1:
    myodfile=odfile

with open(myodfile) as ff2:
    olines=  ff2.readlines()

ff2.close()
#

for oli in olines:
    print(oli)

##### BEGIN DECODING

printbn()
printds()
print("HERE IS THE AWIPS HEADER:")
printds()
print(awips_header)
printbn()

# 0123456789012345678901234567890
# SDUS84 KFDR 191928...NSTFDR...

ORIG_ICAO_ID_hdr=awips_header[7:11]

PRODUCT_ID_hdr=awips_header[21:24]

RADAR_3_LETTER=awips_header[24:27]

printds()
print('The ICAO ID Of the originator:       '+ORIG_ICAO_ID_hdr)
print('The three letter product id is:      '+PRODUCT_ID_hdr)
print('The three letter radar id:           '+RADAR_3_LETTER)

if "NCR" in PRODUCT_ID_hdr:
    printok()
    print('This is an NCR product. This code will only decode NCR data.')
    printok()
else:
    printerr()
    print('This is NOT an NCR product. This code will only decode NCR data.')
    printerr()

# Print plain description of Product ID
if PRODUCT_ID_hdr in prod_sbn:
    print('The Product ID is valid.')
    printds()
    print('The plain description of product id '+str(PRODUCT_ID_hdr)+' is:')
    #
    description_product=dict_product_sbn[PRODUCT_ID_hdr]
    print(description_product)
else:
    print('The product id is invalid.')

if RADAR_3_LETTER in call_signs_3list:
    fourletter=dict_icao_3ltr[RADAR_3_LETTER]
    printds()
    print('The three letter icao is '+RADAR_3_LETTER)
    print('The four letter  icao is '+fourletter)
    location_icao=dict_call_signs[fourletter]
    print('The location of '+ fourletter+' is '+location_icao)
else:
    printds()
    print('The 3 letter radar icao is invalid')

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

# HALFWORDS 22 and 23: Volume Scan time
#
VOL_SCAN_TIME=PDBLINE0[70:79]
#
real_vol_scan_time=decode_twohalfwords(VOL_SCAN_TIME)
Real_time_of_Volscan=determine_time_since_midnight(real_vol_scan_time)
print('VOL_SCAN_TIME=                       '+VOL_SCAN_TIME)
print('real_vol_scan_time =                 '+str(real_vol_scan_time))
print('The ACTUAL time of the data is:      '+Real_time_of_Volscan)

#
# HALFWORD 24:
#
PROD_GEN_DATE=PDBLINE0[80:84]
#
real_prod_generation_date = decode_halfword(PROD_GEN_DATE)
Real_date_prod_gen = determine_date_since_1970(real_prod_generation_date)

print('PROD_GEN_DATE=                       '+PROD_GEN_DATE)
print('real_prod_generation_date  =         '+str(real_prod_generation_date))
print('The ACTUAL date of prod generation = '+Real_date_prod_gen)

#
# HALFWORDS 25 and 26
#
PROD_GEN_time=PDBLINE1[10:19]
#
real_prod_generation_time = decode_twohalfwords(PROD_GEN_time)
Real_time_prod_gen=determine_time_since_midnight(real_prod_generation_time)

print('PROD_GEN_time=                       '+PROD_GEN_time)
print('real_prod_generation_time  =         '+str(real_prod_generation_time))
print('The ACTUAL time of prod generation = '+Real_time_prod_gen)

#
# HALFWORD 27
#
PRODUCT_DEP_PARAMETER_1=PDBLINE1[20:24]
#
real_prod_dep_param_1=decode_halfword(PRODUCT_DEP_PARAMETER_1)

print('PRODUCT_DEP_PARAMETER_1=             '+PRODUCT_DEP_PARAMETER_1)
print('real_prod_dep_param_1=               '+str(real_prod_dep_param_1))

#
# HALFWORD 28
#
PRODUCT_DEP_PARAMETER_2=PDBLINE1[25:29]
#
real_prod_dep_param_2=decode_halfword(PRODUCT_DEP_PARAMETER_2)

print('PRODUCT_DEP_PARAMETER_2=             '+PRODUCT_DEP_PARAMETER_2)
print('real_prod_dep_param_2=               '+str(real_prod_dep_param_2))

#
# HALFWORD 29
#
ELEVATION_NUMBER=PDBLINE1[30:34]
#
#
real_elevation_number = decode_halfword(ELEVATION_NUMBER)

print('ELEVATION_NUMBER=                    '+ELEVATION_NUMBER)
print('real_elevation_number =              '+str(real_elevation_number))

if real_elevation_number == 0:
    print("0 value means volume based prod") 

#
# HALFWORD 30
#
PRODUCT_DEP_PARAMETER_3=PDBLINE1[35:39]
#
real_prod_dep_param_3=decode_halfword(PRODUCT_DEP_PARAMETER_3)

print('PRODUCT_DEP_PARAMETER_3=             '+PRODUCT_DEP_PARAMETER_3)
print('real_prod_dep_param_3=               '+str(real_prod_dep_param_3))


#
# HALFWORD 31
# 
DATA_LEVEL_1_THRESH=PDBLINE1[40:44]
#
real_data_lvl_1_thresh=decode_halfword(DATA_LEVEL_1_THRESH)
print('DATA_LEVEL_1_THRESH=                 '+DATA_LEVEL_1_THRESH)

print('real_data_lvl_1_thresh=              '+str(real_data_lvl_1_thresh))

#
# HALFWORD 32
#
DATA_LEVEL_2_THRESH=PDBLINE1[45:49]
#
real_data_lvl_2_thresh=decode_halfword(DATA_LEVEL_2_THRESH)
print('DATA_LEVEL_2_THRESH=                 '+DATA_LEVEL_2_THRESH )
print('real_data_lvl_2_thresh=              '+str(real_data_lvl_2_thresh))

#
# HALFWORD 33
#
DATA_LEVEL_3_THRESH=PDBLINE1[50:54]
#
real_data_lvl_3_thresh=decode_halfword(DATA_LEVEL_3_THRESH)
print('DATA_LEVEL_3_THRESH=                 '+DATA_LEVEL_3_THRESH)
print('real_data_lvl_3_thresh=              '+str(real_data_lvl_3_thresh))

#
# HALFWORD 34-46
#
#DATA_LEVEL_4_THRES__THRU_SIXTEEN=PDBLINE0[125:189]
#
#real_data_lvl_4_thresh=decode_halfword(DATA_LEVEL_4_THRESH)
#print('DATA_LEVEL_4_THRESH=                 '+DATA_LEVEL_4_THESH)
#print('real_data_lvl_4_thresh=              '+str(real_data_lvl_4_thresh))
#zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
#
# HALFWORD 47
#
PRODUCT_DEP_PARAMETER_4=PDBLINE2[45:49]
#
real_prod_dep_param_4=decode_halfword(PRODUCT_DEP_PARAMETER_4)

print('PRODUCT_DEP_PARAMETER_4=             '+PRODUCT_DEP_PARAMETER_4)
print('real_prod_dep_param_4  =             '+str(real_prod_dep_param_4))


#
# HALF WORD 48 TO 50
# 50 to 64 
# NO MEANING#
# HALFWORD 30
#

#
# HALFWORD 51
#
PRODUCT_DEP_PARAMETER_8=PDBLINE2[65:69]
#
real_prod_dep_param_8=decode_halfword(PRODUCT_DEP_PARAMETER_8)

print('PRODUCT_DEP_PARAMETER_8=             '+PRODUCT_DEP_PARAMETER_8)
print('real_prod_dep_param_8=               '+str(real_prod_dep_param_8))

#
# HALFWORDS 52 and 53
#
PRODUCT_DEP_PARAMETER9n10=PDBLINE2[70:79]
#
Uncompress_Data_size=decode_twohalfwords(PRODUCT_DEP_PARAMETER9n10)

print('PRODUCT_DEP_PARAMETER9n10=           '+PRODUCT_DEP_PARAMETER9n10)
print('Uncompressed Data size   =           '+str(Uncompress_Data_size))

#
# HALFWORD 54
#
VERSION=PDBLINE2[80:82]

Version_decimal=decode_halfword(VERSION)
print('VERSION=                             '+VERSION)
print('Version_decimal=                     '+str(Version_decimal))

# The rest of Halfword 54 is the spot blank

#
# HALFWORDS 55-56


OFFSET_2_SYM_BLOCK=PDBLINE3[10:19]
real_offset_2_sym_block=decode_twohalfwords(OFFSET_2_SYM_BLOCK)

print('OFFSET_2_SYM_BLOCK=                  '+OFFSET_2_SYM_BLOCK)
print('real_offset_2_sym_block=             '+str(real_offset_2_sym_block))

#
# HALFWORDS 57-58
#
OFFSET_2_GRP_BLOCK=PDBLINE3[20:29]
real_offset_2_grp_block=decode_twohalfwords(OFFSET_2_GRP_BLOCK)

print('OFFSET_2_GRP_BLOCK=                  '+OFFSET_2_GRP_BLOCK)
print('real_offset_2_grp_block=             '+str(real_offset_2_grp_block))

#
# HALFWORDS 59-60
#

OFFSET_2_ALP_BLOCK=PDBLINE3[30:39]
real_offset_2_alp_block=decode_twohalfwords(OFFSET_2_ALP_BLOCK)

print('OFFSET_2_ALP_BLOCK=                  '+OFFSET_2_ALP_BLOCK)
print('real_offset_2_alp_block=             '+str(real_offset_2_alp_block))

#Process the tabular data from the Tabular alphanueric block. I grabbed this using the od command and it is the olines list.
#
iii=0            # This is the index to keep track of where on the list
start=[]         # This is the beginning 
endofblock=0     # The end of the block
averageline=0
dataliststm=[]
parnlist=[]
#
start_txt='STM ID'

end_txt=')'
for oli in olines:
    if start_txt in oli:
        start.append(iii)
    #   
    if end_txt in oli:
        parnlist.append(iii)
    #
    if not(start_txt in oli) and not(end_txt in oli):
        dataliststm.append(iii)
    #
    iii=iii+1
    #
printds()

print('Here are the lines that contain :'+str(start_txt))
print(start)

print('Here are the line numbers that contain :'+str(end_txt))
print(parnlist)

print('Here are the lines that contain storm data:')
print(dataliststm)


printds()
print('These are the lines we identifed:')
print('STORM Positions')
for item in dataliststm:
    print('Line :'+str(item)+':  '+olines[item])
print("Lines that contain "+end_txt)
for item in parnlist:
    print('Line :'+str(item)+':  '+olines[item])

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
# the following lists contian the line numbers that hold the data: 
# dataliststm and parnlist.
#
# The dataliststm contains normal data.
# The parnlist is normal data that adds a -)- in front.
#
# We will decode the storm info along those lines.
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#


print('Positions of Cell data')
for item in start:
    print('Line :'+str(item)+':  '+olines[item])


# Now decode the storm cells between each set of start elements
# We start at olines[start[0]] and go to olines[start[final],
# then we go to olines[parnlist[0] to olines[parnlist[final]]
index=1
stormdatalines=[]
print('Here we display only the storm data')
printds()
for x in dataliststm:
    print(olines[x])
    myitem=olines[x]
    stormdatalines.append(myitem[12:])
    #
for x in parnlist:
    print(olines[x])
    myitem=olines[x]
    stormdatalines.append(myitem[13:])
    index+=1
printds()
print('stormdatalines')
printds()
print(stormdatalines)

#    print(olines

#0020260  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0020402     Q2  237/ 37 TVS     7   70/100/ 1.50    66  64  8.4  37.4  240/ 16  
#0020524     Q3  304/ 53 TVS     6   80/100/ 1.75    67  65 12.4  38.5  271/ 29  
#0020646     W7  212/ 86 TVS     6   50/100/ 1.00    56  58 10.3  39.6  242/ 25  
#0020767 )    Q7   63/121 TVS  NONE   80/100/ 1.75    66  62 22.4  42.5  238/ 31  
#0027726  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0030050     B9  315/ 79 NONE    3    0/  0/ 0.00    17  53  8.9  20.3  222/ 35  
#0030172     T8  292/ 32 NONE NONE    0/  0/ 0.00    14  56  7.4  23.9  246/ 39  
#0030314     U9   29/144 NONE NONE     UNKNOWN       12  46 23.1  29.4  222/ 39  
#0030435 )    J9  277/ 68 NONE    1    0/  0/ 0.00    12  52  7.2  25.5  235/ 31  
#0025602  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0025724     H6  359/113 NONE    3    0/ 80/ 0.50    25  53 15.6  26.9  246/ 29  
#0026046     V2  332/ 83 NONE    3    0/ 70/ 0.50    29  55  9.6  27.4  249/ 25  
#0026170     P0  271/ 48 NONE    2    0/ 70/<0.50     6  47 22.1  27.4    NEW    
#0026311 )    M7  352/107 NONE    3    0/ 10/<0.50    17  51 14.3  28.4  239/ 23  
#...............................................................................
#000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#...............................................................................
#0026170     P0  271/ 48 NONE    2    0/ 70/<0.50     6  47 22.1  27.4    NEW    
#0026311 )    M7  352/107 NONE    3    0/ 10/<0.50    17  51 14.3  28.4  239/ 23  

print("Storm ID, Current AZRAN, Movement, 15min pos, 30 min pos, 45 min pos, 60 min pos")

storm_id=[]
curr_azran=[]
curr_az=[]
curr_range=[]

movement=[]
mov_az=[]
mov_spd=[]

poshpohmx=[]

posh=[]

poh=[]

mxsize=[]

tvs=[]

mda=[]

vil=[]

dbzm=[]

ht=[]

top=[]

paren=')'

none_data='NONE'
unkown_data='UNKNOWN'
new_data="NEW"
#...............................................................................
#000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#...............................................................................
#P0  271/ 48 NONE    2    0/ 70/<0.50     6  47 22.1  27.4    NEW
#T8  292/ 32 NONE NONE    0/  0/ 0.00    14  56  7.4  23.9  246/ 39
#ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT


#
# We are decoding the various parts of the data- we get the storm id, the current azumith and range, and the TVS, MDS and Hail probabilites. All stored in lists. 
#

for data in stormdatalines:
    storm_id_str      = data[0:2]
    storm_id.append(storm_id_str)
    #
    #
    current_azran_str = data[4:11]
    curr_azran.append(current_azran_str)
    splt_c_axr=current_azran_str.split('/')
    curr_az.append(splt_c_axr[0])
    curr_range.append(splt_c_axr[1])
    #
    #
    movement_str =      data[59:66]
    if new_data in movement_str:
        movement_str=' 999/999'
    movement.append(movement_str)
    splt_move=movement_str.split('/')
    if new_data in movement_str:
        mov_az.append(int('999'))
        mov_spd.append(int('999'))
    else:
        mov_az.append(int(splt_move[0]))
        mov_spd.append(int(splt_move[1]))
    #
    tvs_str =      data[12:16]
    #if none_data in pos15min_str:
    if none_data in tvs_str:
        tvs_str='999'
    tvs.append(tvs_str)
    #
    mda_str =      data[17:21]
    if none_data in mda_str:
        mda_str='999'
    mda.append(mda_str)
    #
    poshpohmx_str =      data[21:36]
    if unkown_data in poshpohmx_str:
        poshpohmx_str='999/999/9999'
    poshpohmx.append(poshpohmx_str)
    splt_poshpohmx=poshpohmx_str.split('/')
    posh.append(int(splt_poshpohmx[0]))
    poh.append(int(splt_poshpohmx[1]))
    mxsize.append(str(splt_poshpohmx[2]))

    vil_str= data[38:42]
    vil.append(vil_str)

    dbzm_str= data[42:46]
    dbzm.append(dbzm_str)

    ht_str= data[46:51]
    ht.append(ht_str)

    top_str= data[51:57]
    top.append(top_str)

    #
    #
    #print("Storm ID, Current AZRAN, Movement, 15min pos, 30 min pos, 45 min pos, 60 min pos")
    print(storm_id_str+" "+current_azran_str+" "+movement_str+" "+tvs_str+" "+mda_str+" "+poshpohmx_str+" "+vil_str+""+dbzm_str+""+ht_str+""+top_str+"")

#fig, ax = plt.subplots(projection=polar)
#fig=plt.figure(figsize=(10,10))
#ax=fig.add_subplot(projection="polar")

#ax.plot()
#ax.plot(0,0, 'ro',  markersize=19)
#ax.plot(0,0, 'wo',  markersize=10)
#ax.annotate(fourletter, xy=(0, 0),  xytext=(0.25, 0.25), textcoords='figure fraction', \
#    arrowprops=dict(facecolor='red', shrink=0.05), \
#    horizontalalignment='left', \
#    verticalalignment='bottom', fontsize=15)


# Now we plot the data
#real_lat_radar 
#real_lon_radar

cent_lon = real_lon_radar*(1.0-2.0)
cent_lat = real_lat_radar


fig = plt.figure(figsize=(15, 15))
add_metpy_logo(fig, 190, 85, size='large')


ctables = (('NWSStormClearReflectivity', -20, 0.5),  # dBZ
           ('NWS8bitVel', -100, 1.0))  # m/s


### Plot the data
crs=ccrs.PlateCarree()
#crs=ccrs.LambertConformal(central_longitude=cent_lon, central_latitude=real_lat_radar)
ax = fig.add_subplot(1,1,1, projection=crs)

xlr, ylr = azimuth_range_to_lat_lon(0, 0, cent_lon, cent_lat)

ax.plot(xlr,ylr, color='purple', marker= 'o', label=str(RADAR_3_LETTER), markersize=19)
ax.plot(xlr,ylr, color='white', marker= 'o', label=str(RADAR_3_LETTER), markersize=9)

ax.annotate(fourletter, xy=(xlr, ylr),  xytext=(0.25, 0.25), textcoords='figure fraction', \
    arrowprops=dict(facecolor='purple', shrink=0.05), \
    horizontalalignment='left', \
    verticalalignment='bottom', fontsize=16)

R=6371.0

nm2km=1.852


#
curr_lat=[]
curr_lon=[]
#
lat_mda1=[]
lon_mda1=[]
#
lat_mda3=[]
lon_mda3=[]
#
lat_mda5=[]
lon_mda5=[]
#
lat_tvs=[]
lon_tvs=[]
#
lat_hail1=[]
lon_hail1=[]
#
lat_cell=[]
lon_cell=[]
#


#
# In this section, we will plot TVS as a red triangle pointed down. Mesocyclones are green circles. All other cells are small blue squares.
#

ii=0
for item in storm_id:

    angl=float(curr_az[ii])#*degtorad
    rng=float(curr_range[ii])*1.852

    xlo, ylo = azimuth_range_to_lat_lon(angl, rng, cent_lon, cent_lat)
    lat2, lon2 = get_point_at_distance(cent_lat, cent_lon, rng, angl)
    curr_lat.append(lat2) 
    curr_lon.append(lon2) 
    
    mdain=mda[ii]
    mdanbr=float( mdain )
    #
    print('mdain is '+str(mdain))

    ax.plot(lon2,lat2,'o', label=storm_id[ii], color='blue', transform=ccrs.Geodetic())

    # This plots mesocyclone info. Mesocyclone strength of 1 or 2 is a small green circle with a smaller white center.
    # Strength 3 or 4 is a bigger green circle with a pink center. 5 and higher is a large green circle.     

    if '999' in mdain:
        print('No Meso detected in '+storm_id[ii])

    else:
        if mdanbr < 3:
            lat_mda1.append(lat2) 
            lon_mda1.append(lon2)
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='green',markersize=8, transform=ccrs.Geodetic())
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='white',markersize=4, transform=ccrs.Geodetic())
            #ax.plot(angl,rng,"o", label=storm_id[ii], color='green',markersize=8)
            #ax.plot(angl,rng,"o", label=storm_id[ii], color='white',markersize=4)
        if mdanbr >= 3:
            lat_mda3.append(lat2) 
            lon_mda3.append(lon2)
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='green',markersize=8, transform=ccrs.Geodetic())
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='pink',markersize=4, transform=ccrs.Geodetic())
            #ax.plot(angl,rng,"o", label=storm_id[ii], color='green',markersize=8)
            #ax.plot(angl,rng,"o", label=storm_id[ii], color='pink',markersize=4)
        if mdanbr >= 5:
            lat_mda5.append(lat2) 
            lon_mda5.append(lon2)
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='green',markersize=12, transform=ccrs.Geodetic())
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='black',markersize=2, transform=ccrs.Geodetic())
            #ax.plot(angl,rng,"o", label=storm_id[ii], color='green',markersize=12)
            #ax.plot(angl,rng,"o", label=storm_id[ii], color='black',markersize=2)

    tvsq=tvs[ii]
    if 'TVS' in tvsq:
        lat_tvs.append(lat2)
        lon_tvs.append(lon2)
        ax.plot(lon2,lat2,"v", label=storm_id[ii], color='red',markersize=18, transform=ccrs.Geodetic())
        #ax.plot(angl,rng,"v", label=storm_id[ii], color='red',markersize=18)

    #ax.plot(angl,rng,'s', label=storm_id[ii], color='blue' )
    
    print("The Storm ID is:"+str(storm_id[ii]))   
    ax.text(lon2,lat2, storm_id[ii] ,horizontalalignment='center', verticalalignment='bottom')
    #ax.text(angl,rng, storm_id[ii] ,horizontalalignment='center', verticalalignment='bottom')
    #ax.annotate('a polar annotation', xy=(angl, rng),  xytext=(0.05, 0.05), textcoords='figure fraction', \
    #    arrowprops=dict(facecolor='black', shrink=0.05), \
    #    horizontalalignment='left', \
    #    verticalalignment='bottom')
    #ax.plot(lon2,lat2,'o', label=storm_id[ii], color='blue', transform=ccrs.Geodetic())
    ii=ii+1

# This part determines the max range for plotting. If there are cells over 300 km away, we include them.
# If there is a cell over 460 km away, we will not plot it, it is not in the range of the radar. 
# So 460 km is the greatest range allowed.
# Note we will at least plot 300 km.

mx_c_rng=float(max(curr_range))*1.852

print('maximum rng= '+str(mx_c_rng))

maxrange=300.0 # km

if mx_c_rng > maxrange:
    maxrange = mx_c_rng+20.0

if maxrange > 460.0:
    maxrange = 460.0

# This ends the max range part.


#xlocs, ylocs = azimuth_range_to_lat_lon(az, rng, cent_lon, cent_lat)
ax.add_feature(USCOUNTIES, linewidth=0.5)
ax.set_extent([cent_lon-2.7, cent_lon+2.7, cent_lat-2.7, cent_lat+2.7])
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


#o
#ax.set_theta_zero_location("N")
#ax.set_theta_direction(-1)
#ax.set_rmax(maxrange)
#ax.set_rticks([10, 50, 100, 150, 200, 250,300])
#ax.set_rlabel_position(-22.5)
#ax.grid(True)
#ax.set_title("Plot: NST data "+str(awips_header))

##
##----
## First we will make a processed csv file, then a kml file
##

# csv comes first

# Make processed csv the file

pcsvfile=thefile+".NCR_proc.csv"

print(DADASH)
print("Making the updated CSV file With geo-navigation, file name is:"+str(pcsvfile))
print(DADASH)

with open(pcsvfile, 'w', newline='') as filecsv:
    writer = csv.writer(filecsv)
    csvfield = ["Storm_Id","begining_azimuth","beginning_range","radar_lat", "radar_lon","lat","long","tvs","mda","posh","poh","mxsize","vil","dbzm","ht", "top"]
    writer.writerow(csvfield)
    ii=0
    for item in storm_id:
        stritem=str(item)
        writer.writerow([item,curr_az[ii],curr_range[ii], \
            cent_lat,cent_lon,curr_lat[ii],curr_lon[ii],tvs[ii],mda[ii],posh[ii],poh[ii],mxsize[ii],vil[ii],dbzm[ii],ht[ii],top[ii] ]) 
        ii=ii+1
# end of making the processed CSV.
#
printok()
print("The processed csv file was made. The file name is: "+str(pcsvfile))
printok()



# Make the kml file
makekml =1

kml_filemain=thefile+".NCR_proc.kml"


if makekml ==1:
    printok()
    #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Now we make the KML file.
    ff=open(kml_filemain, "w+")
    ff.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    ff.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    ff.write("  <Document>\n")
    tvsflag=0
    #
    mda1flag=0
    mda3flag=0
    mda5flag=0
    #
    ii=0
    for item in storm_id:
        tvsflag=0
        #
        mda1flag=0
        mda3flag=0
        mda5flag=0
        #
        stritem=str(item)
        #
        mdain=mda[ii]
        # If there is a TVS, we only plot the TVS, not the MDA too.
        if tvsflag == 1:
            madin='999'
        mdanbr=float( mdain )
        if '999' in mdain:
            mda1flag=0
            mda3flag=0
            mda5flag=0
            mdanbr=999.0
            #
            print('No Meso detected in '+storm_id[ii])
        else:
            if mdanbr < 3:
                mda1flag=1
                ff.write("    <Placemark>\n")
                ff.write("     <Style>\n") 
                ff.write("      <IconStyle>\n")
                ff.write("      <scale>1.0</scale>\n") 
                ff.write("       <Icon>\n") 
                ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/road_shield3.png</href>\n")  ## road_shield3 is a white circle. MDA level 1 or 2.
                ff.write("       </Icon>\n")
                ff.write("     </IconStyle>\n")
                ff.write("     </Style>\n")
                ff.write("      <name>" + str(item) + "</name>\n")
                ff.write("      <description>" + str(item) + "</description>\n")
                ff.write("      <Point>\n")
                ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
                ff.write("      </Point>\n")
                ff.write("    </Placemark>\n")
                #
            if (mdanbr >= 3) and (mdanbr < 5):
                mda3flag=1
                mda1flag=0
                ff.write("    <Placemark>\n")
                ff.write("     <Style>\n") 
                ff.write("      <IconStyle>\n")
                ff.write("      <scale>2.1</scale>\n")  
                ff.write("       <Icon>\n") 
                ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/donut.png</href>\n")  ## donut is a large white circle with an inner circle. MDA level 3 or 4.
                ff.write("       </Icon>\n")
                ff.write("     </IconStyle>\n")
                ff.write("     </Style>\n")
                ff.write("      <name>" + str(item) + "</name>\n")
                ff.write("      <description>" + str(item) + "</description>\n")
                ff.write("      <Point>\n")
                ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
                ff.write("      </Point>\n")
                ff.write("    </Placemark>\n")
                #
            if (mdanbr >= 5) and (mdanbr < 900):
                mda5flag=1
                mda3flag=0
                mda1flag=0
                ff.write("    <Placemark>\n")
                ff.write("     <Style>\n") 
                ff.write("      <IconStyle>\n")
                ff.write("      <scale>2.5</scale>\n")                   
                ff.write("       <Icon>\n") 
                ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/target.png</href>\n")  ## Target is three concentric circles. MDA level 5 or up.
                ff.write("       </Icon>\n")
                ff.write("     </IconStyle>\n")
                ff.write("     </Style>\n")
                ff.write("      <name>" + str(item) + "</name>\n")
                ff.write("      <description>" + str(item) + "</description>\n")
                ff.write("      <Point>\n")
                ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
                ff.write("      </Point>\n")
                ff.write("    </Placemark>\n")
                #
        #
        allinone=tvsflag+mda1flag+mda3flag+mda5flag
        # This is the case where there in no TVS or MDA. Simply a normal cell.
        if allinone ==0:
            ff.write("    <Placemark>\n")
            ff.write("     <Style>\n") 
            ff.write("      <IconStyle>\n")
            ff.write("      <scale>1.5</scale>\n") 
            ff.write("       <Icon>\n") 
            ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>\n")  ## Placemark circle is a small white circle with black dot. Normal cell.
            ff.write("       </Icon>\n")
            ff.write("     </IconStyle>\n")
            ff.write("     </Style>\n")
            ff.write("      <name>" + str(item) + "</name>\n")
            ff.write("      <description>" + str(item) + "</description>\n")
            ff.write("      <Point>\n")
            ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
            ff.write("      </Point>\n")
            ff.write("    </Placemark>\n")
        #
        tvsq=tvs[ii]
        if 'TVS' in tvsq:
            tvsflag=1
            ff.write("    <Placemark>\n")
            ff.write("     <Style>\n") 
            ff.write("      <IconStyle>\n")
            ff.write("      <scale>2.5</scale>\n")
            ff.write("       <Icon>\n") 
            ff.write("       <href>http://maps.google.com/mapfiles/kml/paddle/red-stars.png</href>\n")  ## red-stars is a pin mark that is red and has a star in it. This is a TVS symbol
            ff.write("       </Icon>\n")
            ff.write("     </IconStyle>\n")
            ff.write("     </Style>\n")
            ff.write("      <name>" + str(item) + "</name>\n")
            ff.write("      <description>" + str(item) + "</description>\n")
            ff.write("      <Point>\n")
            ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
            ff.write("      </Point>\n")
            ff.write("    </Placemark>\n")
            # End of TVS
        # End of TVS

        #
        ii=ii+1
        #
    ff.write("    <Placemark>\n")
    ff.write("     <Style>\n") 
    ff.write("      <IconStyle>\n")
    ff.write("      <scale>3.0</scale>\n") 
    ff.write("       <Icon>\n") 
    ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/star.png</href>\n")  ## star is a white star. This is the Radar area.
    ff.write("       </Icon>\n")
    ff.write("     </IconStyle>\n")
    ff.write("     </Style>\n")
    ff.write("      <name>" + str(fourletter) + "</name>\n")
    ff.write("      <description>" + str("Radar-"+fourletter) + "</description>\n")
    ff.write("      <Point>\n")
    ff.write("        <coordinates>"+str(cent_lon)+","+str(cent_lat)+"</coordinates>\n")
    ff.write("      </Point>\n")
    ff.write("    </Placemark>\n")
    # 
    ff.write("  </Document>\n")
    ff.write("</kml>\n")
    ff.close()

#
printok()
print("The processed kml file was made. The file name is: "+str(kml_filemain))
printok()

plt.show()



#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# END of program



#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#od -S 0 KFDR_SDUS84_NCZFDR_202205050117 | grep /
#0020260  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0020402     Q2  237/ 37 TVS     7   70/100/ 1.50    66  64  8.4  37.4  240/ 16  
#0020524     Q3  304/ 53 TVS     6   80/100/ 1.75    67  65 12.4  38.5  271/ 29  
#0020646     W7  212/ 86 TVS     6   50/100/ 1.00    56  58 10.3  39.6  242/ 25  
#0020767 )    Q7   63/121 TVS  NONE   80/100/ 1.75    66  62 22.4  42.5  238/ 31  
#0021332  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0021454     A6   61/112 TVS     4   60/100/ 1.25    24  60 20.0  39.0  243/ 23  
#0021576     T2   62/154 NONE    8     UNKNOWN       69  60 25.7  47.2  228/ 17  
#0021720     F9  259/ 91 NONE    6   50/100/ 1.00    47  60 15.0  29.7  229/ 33  
#0022041 )    O9   56/112 NONE    6   20/ 90/ 0.50    31  53 15.5  30.7  221/ 29  
#0022404  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0022526     I9  213/ 95 NONE    5   60/100/ 1.25    61  61 16.0  46.5  246/ 37  
#0022650     S6  217/120 NONE NONE   80/100/ 2.00    65  65 17.2  40.7  233/ 17  
#0022772     U8  253/ 62 NONE    3   60/100/ 1.25    63  60 11.8  45.7  220/ 14  
#0023113 )    R7  249/ 52 NONE    4   60/100/ 1.25    56  61  7.0  35.6  246/ 17  
#0023456  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0023600     Y9   19/ 24 NONE NONE   30/100/ 0.75    24  55 16.2  32.6    NEW    
#0023722     H9    3/108 NONE    2   30/ 90/ 0.75    43  56 14.4  30.0  216/ 23  
#0024044     E9  315/ 71 NONE    1   20/100/ 0.75    39  56 17.6  33.2  216/ 39  
#0024165 )    S9  327/ 74 NONE    3   20/100/ 0.50    29  55 18.2  28.6  241/ 16  
#0024530  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0024652     K9  340/ 91 NONE NONE   20/100/ 0.50    23  52 23.6  29.5  224/ 25  
#0024774     W8   82/ 65 NONE NONE   20/ 90/ 0.75    31  58 15.7  31.6  237/ 21  
#0025116     Z8  208/ 76 NONE    2   10/100/ 0.50    33  54  8.5  35.8  232/ 25  
#0025237 )    M9  271/ 42 NONE    1   10/ 80/ 0.50    37  60  7.4  23.3  245/ 29  
#0025602  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0025724     H6  359/113 NONE    3    0/ 80/ 0.50    25  53 15.6  26.9  246/ 29  
#0026046     V2  332/ 83 NONE    3    0/ 70/ 0.50    29  55  9.6  27.4  249/ 25  
#0026170     P0  271/ 48 NONE    2    0/ 70/<0.50     6  47 22.1  27.4    NEW    
#0026311 )    M7  352/107 NONE    3    0/ 10/<0.50    17  51 14.3  28.4  239/ 23  
#0026654  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0026776     L7   47/126 NONE NONE     UNKNOWN       40  55 18.5  37.1  219/ 23  
#0027120     Z7  113/152 NONE NONE     UNKNOWN       31  52 25.2  38.9  204/ 35  
#0027242     Z9   40/134 NONE NONE     UNKNOWN       20  51 20.5  26.4    NEW    
#0027363 )    L0   60/130 NONE NONE     UNKNOWN       19  49 19.5  32.3    NEW    
#0027726  STM ID  AZ/RAN TVS  MDA  POSH/POH/MX SIZE VIL DBZM  HT  TOP  FCST MVMT 
#0030050     B9  315/ 79 NONE    3    0/  0/ 0.00    17  53  8.9  20.3  222/ 35  
#0030172     T8  292/ 32 NONE NONE    0/  0/ 0.00    14  56  7.4  23.9  246/ 39  
#0030314     U9   29/144 NONE NONE     UNKNOWN       12  46 23.1  29.4  222/ 39  
#0030435 )    J9  277/ 68 NONE    1    0/  0/ 0.00    12  52  7.2  25.5  235/ 31  
#[pmccrone@lnx064 test]$ 
##########

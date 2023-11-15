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

# 0123456789012345678901234567890
# SDUS84 KFDR 191928...NSTFDR...

ORIG_ICAO_ID_hdr=awips_header[7:11]

PRODUCT_ID_hdr=awips_header[21:24]

RADAR_3_LETTER=awips_header[24:27]

printds()
print('The ICAO ID Of the originator:       '+ORIG_ICAO_ID_hdr)
print('The three letter product id is:      '+PRODUCT_ID_hdr)
print('The three letter radar id:           '+RADAR_3_LETTER)

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
#
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


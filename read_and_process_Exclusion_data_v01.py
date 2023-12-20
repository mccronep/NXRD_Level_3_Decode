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
# read_and_process_Exclusion_data_v01.py
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
    import metpy
    import cartopy.crs as ccrs
    import matplotlib.gridspec as gridspec
    import matplotlib.pyplot as plt
    import numpy as np
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

thezones=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]

thezonesn=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]



#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

########
# MAIN part of program
########

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
    print('The file is valid- it exists. ')
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
my_stop1=dpl[1]

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

# PLot data on a polar plot

fig=plt.figure(figsize=(10,10))
ax=fig.add_subplot(projection="polar")

##ax.plot()
#ax.plot(0,0, 'ro',  markersize=29)
#ax.plot(0,0, 'wo',  markersize=19)
#ax.annotate(radar_icao, xy=(0, 0),  xytext=(0.25, 0.25), textcoords='figure fraction', \
#    arrowprops=dict(facecolor='red', shrink=0.05), \
#    horizontalalignment='left', \
#    verticalalignment='bottom', fontsize=15)

ii=0
for item in zone_list:
    #
    angl=float(baz_list[ii])*degtorad
    rng=float(brng_list[ii])*1.852
    ax.plot(angl,rng,'ro', label=item, markersize=5 )
    #ax.plot(angl,rng,'s', label=item, color='blue' )
    print("The zone number is:"+str(item))   
    ax.text(angl,rng, item ,horizontalalignment='center', verticalalignment='bottom')
    angl=float(eaz_list[ii])*degtorad
    rng=float(erng_list[ii])*1.852
    ax.plot(angl,rng,'ro', label=item, markersize=5 )
    #ax.plot(angl,rng,'s', label=item, color='blue' )
    ii=ii+1


#ax.plot()
ax.plot(0,0, 'ro',  markersize=29)
ax.plot(0,0, 'wo',  markersize=19)
ax.annotate(radar_icao, xy=(0, 0),  xytext=(0.25, 0.25), textcoords='figure fraction', \
    arrowprops=dict(facecolor='red', shrink=0.05), \
    horizontalalignment='left', \
    verticalalignment='bottom', fontsize=15)


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

#o
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

ax.set_rmax(maxrange)
ax.set_rticks([10, 50, 100, 150])
#ax.set_rticks([10, 50, 100, 150, 200, 250,300])
ax.set_rlabel_position(-22.5)
ax.grid(True)
ax.set_title("Plot: Exclusion Zone data "+str(radar_icao))
plt.show()

# Make the kml file
makekml =0

if makekml ==1:
    printok()
    #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Now we make the KML file.

#    KMLFile = open("KML.txt", "w")
#    f.write("<KML_File>\n")
#    f.write("<Document>\n")
#    for line in List2:
#        f.write("   <Placemark>")
#        f.write("       <decription>" + str(row[0]) + "</description>")
#        f.write("       <Point>")
#        f.write("          <coordinates>" + str(row[2]) + str(row[1])"</coordinates>")
#        f.write("       </Point>")
#        f.write("   </Placemark>")
#    f.write("</Document>\n")
#    f.write("</kml>\n")
#    KMLFile = close()



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

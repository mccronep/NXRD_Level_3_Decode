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
# process_level3_files_NCR_v11_tvso.py
# :::::::::::::::::::::::::::::::::::::::::::::::
#
#  PROGRAM OVERVIEW:
#       (0) The PYTHON CODE reads WSR88D L3 information from a file. 
#       (1) The information is used to decode NEXRAD data for further post analysis.
#
# This will run the v11 tvso program over all the files in a directory. It will only process NCR files.
# This is the same as process_level3_NCR_v11_kml.py 
# the diff is that it only plots TVS./
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

try:
    import datetime
    import time
    #
    import os
    import sys
    import csv
    #import metpy
    #import pandas as pd
    #import cartopy.crs as ccrs
    #import matplotlib.gridspec as gridspec
    #import matplotlib.pyplot as plt
    import numpy as np
    #import csv
    #
    #from metpy.calc import azimuth_range_to_lat_lon
    #from metpy.io import Level3File
    #from metpy.plots import add_metpy_logo, add_timestamp, colortables, USCOUNTIES
    #from metpy.units import units
    from math import asin, atan2, cos, degrees, radians, sin
    #
    #import cartopy.feature as cfeature
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
    inputdir=sys.argv[1]

    print('Read in the directory')
else:

    inputdir='Not_defined'
# Variables I will use in all functions:
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#outputdir='/home/pmccrone/Pictures/tvso/11KTLX01D'
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

print('Input directory is:'+str(inputdir))

fileexists=os.path.exists(inputdir)
useinputfile=0


if fileexists:
    print("The input directory "+str(inputdir)+" exists.")
    useinputfile=1
#
else:
    print("The input file "+str(inputdir)+" does not exist.")
    useinputfile=0

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

########
# MAIN part of program
########

datadirectry='/home/pmccrone/test/'
pythondir="/home/pmccrone/anaconda3/bin/python"

for x in os.listdir(inputdir):
    if 'NCR' in x:
        command=pythondir+' '+datadirectry+'process_level3_NCR_v11_tvso_kml.py'+' '+inputdir+'/'+str(x)
        #
        printds()
        print(command)
        printds()
        os.system(command)





#/home/pmccrone/anaconda3/bin/python ./process_level3_NCR_v11_tvso_kml.py /import/frb_archive/pmccrone/level_3/2024a/2024_Sulphur_Tornado_27Apr_01b_KFWS/Sulphur_FWS_01b/KFWD_SDUS84_NCRFWS_202404280602







#!/bin/bash

# This script is a "wrapper" shell script to facilitate running the est_comms_link.py
# Python script from the RPG scripts directory.
#
#
#
if grep -q "7.9" /etc/redhat-release ; then
        echo 'RHEL7'
        /home/pmccrone/anaconda3/bin/python /home/pmccrone/test/gui_runrpg_v001.py
else
        echo 'RHEL8 or higher'
        /home/pmccrone/anaconda3/bin/python /home/pmccrone/test/gui_runrpg_v001.py
fi

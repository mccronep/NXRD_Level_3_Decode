#!/home/pmccrone/anaconda3/bin
# -*- coding: utf-8 -*-
#==============================================================
#==-ROC/FRB PYTHON PROGRAM DEFINITION-==========================================
#
#/home/pmccrone/python/src/runrpg
#
# NAME:
# :::::::::::::::::::::::::::::::::::::::::::::::
# gui_runrpg_v004.py
# :::::::::::::::::::::::::::::::::::::::::::::::

'''
#  PROGRAM OVERVIEW:
#       (0) The PYTHON CODE reads case information from an FRB google sheet.
#           The Google sheet is NA23-00082_v2 for R(A) Mod -internal - for
#           allowing light precip , verifying the impact on alpha.
#       (1) The information is used to run NEXRAD RPG cases for further post analysis.
'''

#--------------------------------------------------------------------------------------------------
# PARAMETER TABLE:
#--------------------------------------------------------------------------------------------------
# I/O           NAME                               TYPE            FUNCTION
#--------------------------------------------------------------------------------------------------
#  I            FRB google sheet address           input           INPUT DATA FROM ROC/FRB
#  O            Formatted table of data            output          case information
#=================================================================================================
# Programmer: Mr. Paul McCrone     23 August 2023
# Modification  :  BELOW
#========================================================================================
#  Version 001   , Dated 2025-Jul-20
#                  Initial Build.
#  Version 002   , Dated 2025-Jul-23
#  Version 003   , Dated 2025-Jul-25 -PYLINT Compliant
#  Version 004   , Dated 2025-Jul-23 - 
#
#========================================================================================
#  NOTE: THIS PROGRAM ASSUMES THE USE OF Python version 3.8.8+ for RHEL.
#---------------------------------------------------------------
#  PYTHON MODULES USED: numpy, scipy, matplotlib, datetime,
#                       os, sys, math, warnings, json, socket, subprocess(commands)
#                       tkinter, pandas
#---------------------------------------------------------------#
#
try:
    import pandas as PD
    import os as OS
    import sys
    import math as MATH
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
    import datetime
except:  # pylint: disable=bare-except
    print("Error loading modules!")
    print("The program will end.")
    print("---------------------")
    sys.exit() ## The program ends.
#
WARNING_INIT_ERROR=1

BIGERRORLIST=[]

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
PROGRAM_NAME="gui_runrpg_v003.py"
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# The class ItemSelectorGUI
# I use this to make a gui
# to select an Excel tab.
#
class ItemSelectorGUI:
    """
    This class is used to support making a graphical user interface.
    """
    def __init__(self, master, items):
        self.master = master
        master.title("Select an Item")

        self.items = items
        self.selected_item = None

        # Create a Listbox to display items
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE)
        for item in self.items:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(pady=10)

        # Create a button to confirm selection and exit
        self.select_button = tk.Button(master, text="Select & Exit", command=self.select_and_exit)
        self.select_button.pack(pady=5)

    def select_and_exit(self):
        """
        Function for selecting item
        """
        selected_indices = self.listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            self.selected_item = self.items[index]
            messagebox.showinfo("Selection", f"You selected: {self.selected_item}")
            self.master.destroy()  # Close the GUI window
        else:
            messagebox.showwarning("No Selection", "Please select an item from the list.")
        root.quit()

#
DADASHES='-----------------------------------------------------'
DADASH='-----------------------------------------------------'
PRTERR="--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--"
PRTOK='--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--'
PRTWAR="--WARNING--WARNING--WARNING--WARNING--WARNING--WARNING--WARNING--"
#
DAEQUALS='==--==--==--==--==--==--==--==--==--==--==--==--==--'

#============================================================================================
# functions
#============================================================================================
#
# The printxx functions are just simple functions to make it easy to format prints.
#

def printbn():
    """
    This function is used for making printed output readable
    """
    #
    print('\n')
    #END OF Function

def printok():
    """
    This function is used for making printed output readable
    """
    #
    print(PRTOK)
    #END OF Function

def printerr():
    """
    This function is used for making printed output readable
    """
    #
    print(PRTERR)
    #END OF Function

def printwarn():
    """
    This function is used for making printed output readable
    """
    #
    print(PRTWAR)
    #END OF Function

def printds():
    """
    This function is used for making printed output readable
    """
    #
    print('--------------------------------------------')
    #END
#
# The functions select_directory, select_file are simple methods of having the user
# choose a directory or file. A GUI appears and allows the user to choose.
#

def select_directory():
    """
    This function makes a directory section graphic user interface.
    """
    rootf = tk.Tk()
    rootf.withdraw()  # Hide the main window
    directory_path = filedialog.askdirectory()
    if directory_path:
        print(f"Selected directory: {directory_path}")
    else:
        print("No directory selected.")
    return directory_path
    #END OF Function

def select_file():
    """
    This function selects a file with a graphical user interface
    """
    rootu = tk.Tk()
    rootu.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")
    return file_path
    #END OF Function

#
# The show_message_and_exitX functions are used to display a window that shows a message.
#

def show_message_and_exit1():
    """
    Displays an information message box and then destroys the main window.
    """
    messagebox.showinfo("Select the directory to store the ksh files.", \
                        "Select the directory to store the ksh files. Click OK to exit.")
    root.destroy()

def show_message_and_exit2():
    """
    Displays an information message box and then destroys the main window.
    """
    messagebox.showinfo("Select the Excel file to process.", \
                        "Select the Excel file to process. Click OK to exit.")
    root.destroy()

def show_message_and_exit3():
    """
    Displays an information message box and then destroys the main window.
    """
    messagebox.showinfo("Select the Excel tab or sheet to process.", \
                        "Select the Excel tab or sheet to process. Click OK to exit.")
    root.destroy()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function print_current_time
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def print_current_time(now):
    """
    Displays current date and time.
    """
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
    print( " \n")
    print( "Current date and time using strftime:")
    print( now.strftime("%Y-%m-%d...%H:%M"))
    print( " \n")
    print( "Current date and time using isoformat:")
    print( now.isoformat())
    return  now.strftime("%Y-%m-%d...%H:%M")
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF print_current_time FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#============================================================================================
# end of functions.
#============================================================================================

print_current_time(0)

CURRENT_WORKING_DIRECTORY='/home/pmccrone/python/src/runrpg'
#
CWD_PATH=CURRENT_WORKING_DIRECTORY+'/'
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
THIS_RETURN_VALUE = 0
VALID_THISPATH=OS.path.exists(CWD_PATH)
if VALID_THISPATH:
    print(DADASH)
    print("This path is VALID and EXISTS:: "+CWD_PATH)
    THIS_RETURN_VALUE = 1
    WARNING_INIT_ERROR=1
    print(DADASH)
    #
else:
    #
    print("--CAUTION--")
    MYERRTEXT="You are requesting the validity of this path: "+CWD_PATH
    print("You are requesting the validity of this path: "+CWD_PATH)
    BIGERRORLIST.append(MYERRTEXT)
    print("-------The indicated path is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
    MYERRTEXT="-------The indicated path is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------"
    BIGERRORLIST.append(MYERRTEXT)
    THIS_RETURN_VALUE = 0
    WARNING_INIT_ERROR=0
    print("The program will end.")
    print("---------------------")
    sys.exit() ## The program ends.
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# All Call signs are the ICAO identifiers for all NEXRAD (only NEXRAD) radars.
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
"KEMX","KINX","KVNX","KVBX","KICT","KLTX","KFFC","KYUX","KLGX","KHDC"]
#
#
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
"KEWX":"Austin-San-Antonio_TX", "KEYX":"Edwards-AFB_CA", \
"KFCX":"Roanoke_VA", "KFDR":"Altus-AFB_OK", \
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
"KMPX":"Minneapolis-St.Paul_MN", "KMQT":"Marquette_MI", \
"KMRX":"Knoxville-Tri-Cities_TN", \
"KMSX":"Missoula_MT", "KNKX":"San-Diego-CA", \
"KMTX":"Salt-Lake-City_UT", "KMUX":"San-Francisco_CA",\
"KMVX":"Grand-Forks_ND", "KMXX":"Maxwell-AFB_AL", \
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
"KLGX":"Langley-Hill_WA","KHDC":"Hammond_LA"}

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Check to make sure the directory for the korn shell scripts exists and is valid.
#
# -KSH_SCRIPTS- is the path where we will write out the korn shell scripts
#               for each job.
#
#/home/pmccrone/python/src/runrpg/KSH_SCRIPTS
# Suggest you change this for different runs.

# Make sure KSH_SCRIPTS ends with a /.
KSH_SCRIPTS='/import/frb_archive/pmccrone/Scripts/runrpg/KSH_SCRIPTS2025A/'
#### Make sure KSH_SCRIPTS ends with a /.
#KSH_SCRIPTS='/home/pmccrone/python/src/runrpg/KSH_SCRIPTS/'

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
##### Add gui to select runrpg output directory

#	root = tk.Tk()
#	root.title("Select the directory to store the ksh files.")
#	# Create a button that triggers the message box and exit
#	exit_button = tk.Button(root, text="Exit", command=show_message_and_exit1)
#	exit_button.pack(pady=20)
#
#	# Start the Tkinter event loop
#	root.mainloop()

printok()
print("Select the directory to store the ksh files.")
printok()

KSH_SCRIPTS=select_directory()

# End of gui to select output direcrtory
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Check thisfile
#
IS_VALID_PATH=OS.path.exists(KSH_SCRIPTS)
#
if IS_VALID_PATH:
    print(DADASH)
    print("This path for the ksh scripts is VALID and EXISTS: "+KSH_SCRIPTS)
    THIS_RETURN_VALUE = 1
    print(DADASH)
    WARNING_INIT_ERROR=1
    #
else:
    #
    print("---CAUTION---")
    print("---The indicated path for ksh is INVALID! NEED TO CHECK THIS!: "+KSH_SCRIPTS)
    MYERRTEXT="---The indicated path for ksh is INVALID! NEED TO CHECK THIS!: "+KSH_SCRIPTS
    BIGERRORLIST.append(MYERRTEXT)
    #
    THIS_RETURN_VALUE = 0
    WARNING_INIT_ERROR=0
    print("The program will end.")
    print("---------------------")
    sys.exit() ## The program ends.
    #
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------
#
THIS_RETURN_VALUE = 0

KSH_SCRIPTS=KSH_SCRIPTS+"/"
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#
file=CWD_PATH+'MetSignal_Testing_Cases.xlsx'

#	### This is the message box for the file selection.
#	root = tk.Tk()
#	root.title("Select the Excel file to process.")
#	# Create a button that triggers the message box and exit
#	exit_button = tk.Button(root, text="Exit", command=show_message_and_exit2)
#	exit_button.pack(pady=20)
#	# Start the Tkinter event loop
#	root.mainloop()

printok()
print("Select the Excel file to process.")
printok()
# Now select the file.
file=select_file()

#
# Check thisfile
#
valid_thisfile=OS.path.isfile(file)
#
if valid_thisfile:
    print(DADASH)
    print("This file is VALID and EXISTS:: "+file)
    THIS_RETURN_VALUE = 1
    print(DADASH)
    WARNING_INIT_ERROR=1
    #
else:
    #
    print("---CAUTION---")
    print("---The indicated file is INVALID! NEED TO CHECK THIS!: "+file)
    MYERRTEXT="---The indicated file is INVALID! NEED TO CHECK THIS!: "+file
    BIGERRORLIST.append(MYERRTEXT)
    #
    THIS_RETURN_VALUE = 0
    WARNING_INIT_ERROR=0
    print("The program will end.")
    print("---------------------")
    sys.exit() ## The program ends.
    #
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------

try:
    excel_file = PD.ExcelFile(file)
    # Replace 'path/to/your/excel_file.xlsx' with the actual path to your Excel file.
except:  # pylint: disable=bare-except
    #
    print("---CAUTION---")
    print("---The indicated file is NOT an EXCEL FILE! NEED TO CHECK THIS!: "+file)
    MYERRTEXT="---The indicated file is NOT an EXCEL FILE! NEED TO CHECK THIS!: "+file
    BIGERRORLIST.append(MYERRTEXT)
    THIS_RETURN_VALUE = 0
    WARNING_INIT_ERROR=0
    print("The program will end.")
    print("---------------------")
    sys.exit() ## The program ends.
    #
    #-----------------------------------------------------------
    # End of if block

sheet_names = excel_file.sheet_names

#	### This is the message box for the Excel sheet selection.
#	root = tk.Tk()
#	root.title("Select the Excel tab or sheet to process.")
#	# Create a button that triggers the message box and exit
#	exit_button = tk.Button(root, text="Exit", command=show_message_and_exit3)
#	exit_button.pack(pady=20)
#
#	# Start the Tkinter event loop
#	root.mainloop()

# Start the Interface to select the tab.
root = tk.Tk()
root.title("Select the Excel Tab")

printok()
print("Select the Excel tab or sheet to process.")
printok()

# New Gui to select the sheet.

app = ItemSelectorGUI(root, sheet_names)
root.mainloop()

# After the GUI closes, you can access the selected item
if app.selected_item:
    print(f"The final selected item was: {app.selected_item}")
    my_sheetname=app.selected_item
else:
    print("No item was selected.")
    print("The program will end.")
    print("---------------------")
    sys.exit() ## The program ends.

#
THIS_RETURN_VALUE = 0
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
try:
    #dataset=PD.read_excel(file, sheet_name="Stratiform Cool Season (F)")
    dataset=PD.read_excel(file, sheet_name=my_sheetname)
    #
    # NOTE: sheet_name is limited to 31 characters.
    #
    print('Read excel file. Successful!')
    # Alternatively, you can specify the sheet indices instead of the sheet names
    #df1 = pd.read_excel("file.xlsx", sheet_name=0)
except:  # pylint: disable=bare-except
    print("WARNING--- The file read was not successful\n\n")
    print("The program will end.")
    print("---------------------")
    sys.exit() ## The program ends.
    WARNING_INIT_ERROR=0
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

sp='==>'

print (DADASHES)
print("We print the dataset from Excel file then we print the first row, then one more.")

#
print(dataset)
##print(dataset.loc[0])
##print(dataset.loc[[0,1]])

#Get a quick overview by printing the first 10 rows of the DataFrame:
print (DADASHES)
print("Printing the first 10 rows -using the head option- of the DataFrame:")
print(dataset.head(10))

# There is also a tail() method for viewing the last rows of the DataFrame.
# The tail() method returns the headers and a specified number of rows, starting from the bottom.
print (DADASHES)

print("Printing the last 10 rows -using the tail method- of the Dataset:")
print(dataset.tail(10))

# Print information about the data:
print (DADASHES)
print("Print info about the data:")
print(dataset.info())

#### Keeping this code as it may be useful in the future.
#Return a new Data Frame with no empty cells
#new_df =dataset.dropna()

# If you want to change the original DataFrame, use the inplace = True argument
#dataset.dropna(inplace = True)

# Replace Empty Values
# Another way of dealing with empty cells is to insert a new value instead.
# This way you do not have to delete entire rows just because of some empty cells.
# The fillna() method allows us to replace empty cells with a value:
#dataset.fillna(130, inplace = True)

# Replace Only For Specified Columns
# The example above replaces all empty cells in the whole Data Frame.
# To only replace empty values for one column, specify the column name for the DataFrame
#df["Calories"].fillna(130, inplace = True)

# Replacing Values
# One way to fix wrong values is to replace them with something else.
# In our example, it is most likely a typo, and the value should be "45"
# instead of "450",  and we could just insert "45" in row 7'
#df.loc[7, 'Duration'] = 45

# Removing Rows
# Another way of handling wrong data is to remove the rows that contains wrong data.
# This way you do not have to find out what to replace them with, and there is a good
# chance you do not need them to do your analyses.
# Delete rows where "Duration" is higher than 120:
# for x in df.index:
#   if df.loc[x, "Duration"] > 120:
#     df.drop(x, inplace = True)


# pandas Get Column Names
# You can get the column names from pandas DataFrame using df.columns.values,
# and pass this to python list() function to get it as list,
# once you have the data you can print it using print() statement.
print (DADASHES)
print("We will print the column names:")
print(dataset.columns.values)

# You can also use df.columns.values.tolist() to get the DataFrame column names.
colmn_list=dataset.columns.values.tolist()
num_cols=len(colmn_list)

print (DADASHES)
print("This is the last column - This is its name:")
last_col=colmn_list[num_cols-1]
print(colmn_list[num_cols-1])

# Our dataset has 'Max Range for R(A) usage (km)' for the last column.
# How do we get the entry of this column from the 7th row?
#dataset.loc[7,last_col]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# THIS IS MEANT TO EXPLAIN HOW I GET THE DATA FROM THE FILE:
#
# Note, for our data set the following columns are important:
# I ASSUME THE EXCEL SHEET HAS THESE COLUMNS IN THIS ORDER!
# Note: In Python, The first column in column Zero (0).
# I leave column zeo for notes.
# Col
# No.  Name:
#  0 - 'Radar Site'                                                   (A)
#  1-  'File Location Level-II Data (Linux)'                          (B)
#  2 - 'File Location  Level-III Products (Linux)'                    (C)
#  3 - 'Est. ISDP pulled from ASP log, use with "show_isdp" command.' (D)
#  4 - 'Max Range for R(A) usage (km)'                                (E)
#  5 - 'Job Number' - This is the job number for scripts.             (F)
#  6 - 'Execute?'   - This tells the program if the scripts           (G)
#                     should actually be built. If 'no', the
#                     script won't be built, and will not run.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# If I do not specify a column, I do not use it.
# We do not care about the contents of columns 7 and higher, etc.
#

col_radar_site=colmn_list[0]
col_levelII=colmn_list[1]
col_level3=colmn_list[2]
col_ISDP=colmn_list[3]
col_maxrange=colmn_list[4]
#
col_Job_number=colmn_list[5]
col_execute=colmn_list[6]

# Print all the level II directories
print (DADASHES)
print("These are the level II directories:")
for x in dataset.index:
    print(dataset.loc[x,col_levelII])

# Print all the level 3 directories
print (DADASHES)
print("These are the level 3 directories:")
# Print all the level 3 directories
for x in dataset.index:
    print(dataset.loc[x,col_level3])

# Print all the Radar stations:
print (DADASHES)
print("These are the Radar stations")
for x in dataset.index:
    print(dataset.loc[x,col_radar_site])

#Print all the Estimated ISDP values
print (DADASHES)
print("These are the estimated ISDP vals:")
ISDPINDEX=1
#
for x in dataset.index:
    ISDPINDEX=ISDPINDEX+1
    if MATH.isnan(dataset.loc[x,col_ISDP]):
        print("ISDPINDEX= "+str(ISDPINDEX))
        MYERRTEXT="ISDPINDEX= "+str(ISDPINDEX)
        BIGERRORLIST.append(MYERRTEXT)
        print("This value is not a proper number. ISDP was reported as NaN. Please fix this.")
        MYERRTEXT="This value is not a proper number. ISDP was reported as NaN. Please fix this."
        BIGERRORLIST.append(MYERRTEXT)
    else:
        print(str(int(dataset.loc[x,col_ISDP])))

#Print the max range for each row:
print (DADASHES)
print("These are the maximum range values:")
RNGINDEX=1
for x in dataset.index:
    RNGINDEX=RNGINDEX+1
    if MATH.isnan(dataset.loc[x,col_maxrange]):
        MYERRTEXT="RNGINDEX= "+str(RNGINDEX)
        print(str(MYERRTEXT))
        BIGERRORLIST.append(MYERRTEXT)
        MYERRTEXT="This value is not a proper number. Please check this."
        print(str(MYERRTEXT))
        BIGERRORLIST.append(MYERRTEXT)
    else:
        print(dataset.loc[x,col_maxrange])

# Print the job number for each row:
print (DADASHES)
print("These are the Job number:")
JOBINDEX=1
for x in dataset.index:
    JOBINDEX=JOBINDEX+1
    if MATH.isnan(dataset.loc[x,col_Job_number]):
        print("JOBINDEX= "+str(JOBINDEX))
        print("This value is not a proper number. Please check this.")
    else:
        print(str(int(dataset.loc[x,col_Job_number])))

#Print the execute for each row:
print (DADASHES)
print("These are the execution setting values for each row:")
for x in dataset.index:
    print(dataset.loc[x,col_execute])

##
## Get example of data from row 5:
## This is for testing. Keep it.
#
ROWX=5
row5_radarsite = dataset.loc[ROWX,col_radar_site]
row5_levelII   = dataset.loc[ROWX,col_levelII]
row5_level3    = dataset.loc[ROWX,col_level3]
row5_ISDP      = dataset.loc[ROWX,col_ISDP]
row5_max_range = dataset.loc[ROWX,col_maxrange]
row5_Job_number = dataset.loc[ROWX,col_Job_number]
row5_execute = dataset.loc[ROWX,col_execute]

# This is for test runs.
#print('row5_radarsite= '+str(row5_radarsite))
#print('row5_levelII  = '+str(row5_levelII))
#print('row5_level3   = '+str(row5_level3))
#print('row5_ISDP     = '+str(row5_ISDP))
#print('row5_max_range= '+str(row5_max_range))
#
#print('row5_Job_number   = '+str(row5_Job_number))
#print('row5_execute   = '+str(row5_execute))
##
## - - - - - - - - - - - - - -
## Contruct KSH to run mrpg.
#

print(DADASHES)
print(DADASHES)
print(DADASHES)
#print("Example of playback instructions from row 5\n")
#print("mrpg cleanup\n")
#print("cad "+row5_radarsite.lower()+" 1\n")
#print("mrpg -p startup\n")RofA_ISDP_Interp_Fix
#print("show_isdp -i "+str(row5_ISDP)+"\n")
#print("hci &\n")

DADOTS=". . . . . . . . . . . . . . ."

# ***************************************************************************************
#### Begin main X loop
#### x represents the index value of every row. This is the python index,  not the Excel
#### index. They aren't the same.
#### Excel row 2 will be python row 0. Remember python starts with 0.
#### We are going through every row in the excel spreadsheet.  The for x loop is a big loop.

for x in dataset.index:
    print(DADASHES)
    print(DADASHES)
    print(DADASHES)
    #ROWX=x
    ROWX_radarsite = dataset.loc[   x,col_radar_site]
    ROWX_levelII   = dataset.loc[   x,col_levelII]
    ROWX_LEVEL3    = dataset.loc[   x,col_level3]
    ROWX_ISDP      = dataset.loc[   x,col_ISDP]
    ROWX_max_range = dataset.loc[   x,col_maxrange]
    rox_Job_number = dataset.loc[   x,col_Job_number]
    rwx_Job_number= str(int(rox_Job_number))
    ROWX_JOB_NUMBER=str(rwx_Job_number)

    if rox_Job_number < 100:
        ROWX_JOB_NUMBER="0"+rwx_Job_number
    if rox_Job_number < 10:
        ROWX_JOB_NUMBER="00"+rwx_Job_number

    ROWX_execute    = dataset.loc[   x,col_execute]

    EXECUTE_PERMIT=True

    #
    # - - - - - - - - - - - - - - -

    #======== Are the radar identifiers correct?
    #  Is the radarsite listed in:
    #  ALL_call_signs ?
    #  All_call_signs contains all the NEXRAD radars that we will process.
    # This identifier must be one of these.
    #
    RADAR_ID_CORRECT=1

    if ROWX_radarsite in ALL_call_signs:
        print('The radar identifer, '+str(ROWX_radarsite)+', is Valid. The program will continue.')
        #
        print("We are processing the radarsite at: "+str(dict_call_signs[ROWX_radarsite]) )
        EXECUTE_PERMIT=True
        RADAR_ID_CORRECT=1

    if ROWX_radarsite not in ALL_call_signs:
        print('WARNING: The radar ICAO,>'+str(ROWX_radarsite)+'<,is NOT Valid. Skip to next run.')
        EXECUTE_PERMIT=False
        RADAR_ID_CORRECT=0

    # Only perform the contruction of commands for cases with execute set to yes.
    # We will call this the execute test
    if "yes" in ROWX_execute:
        EXECUTE_PERMIT=True
    elif "YES" in ROWX_execute:
        EXECUTE_PERMIT=True
    elif "Yes" in ROWX_execute:
        EXECUTE_PERMIT=True
    elif "Y" in ROWX_execute:
        EXECUTE_PERMIT=True
    elif "y" in ROWX_execute:
        EXECUTE_PERMIT=True
    else:
        EXECUTE_PERMIT=False


    # End of radar identifer Check
    # - - - - - - - - - - - - - - -
    #
    #======== Are the directories valid?
    #xx LEVEL II xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    #
    LEVEL2_RETURN_VALUE = 0
    VALID_THISPATH=OS.path.exists(str(ROWX_levelII))
    if VALID_THISPATH:
        print(DADASH)
        print("The Level II path is VALID and EXISTS:: "+ROWX_levelII)
        LEVEL2_RETURN_VALUE = 1
        WARNING_INIT_ERROR=1
        EXECUTE_PERMIT=True
        print(DADASH)
        #
    else:
        #
        print("--CAUTION--")
        print("You are requesting the validity of this Lvl 2 path: "+str(ROWX_levelII))
        print("-------The indicated path is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        print("-------Level II directories are assumed to exist   -----------------")
        print("-------and have data! This is your responsibility! -----------------")
        LEVEL2_RETURN_VALUE = 0
        EXECUTE_PERMIT=False
        WARNING_INIT_ERROR=0
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------

    #======== Are the directories valid?
    #xx LEVEL 3 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # I made a big change here. What if we have a new project and need to make
    # new level 3 subdirectories? This will check for existing level 3, then try to
    # make the level  3 directories then make them writable.
    LVL3_RETURN_VALUE = 0
    VALID_THISPATH=OS.path.exists(str(ROWX_LEVEL3))
    #Level 3 if (top of loop)
    #
    if EXECUTE_PERMIT==False:
        EXECUTE_PERMIT==False
        continue
    elif VALID_THISPATH:
#    if VALID_THISPATH:
        print(DADASH)
        print("The Level 3 path is VALID and EXISTS:: "+ROWX_LEVEL3)
        LVL3_RETURN_VALUE = 1
        WARNING_INIT_ERROR=1
        EXECUTE_PERMIT=True
        print(DADASH)
        #
    else:
        #
        print("--CAUTION--")
        print("You are requesting the validity of this Level 3 path: "+str(ROWX_LEVEL3))
        print("-------The indicated path is INVALID!-----------------")
        print("-------We will try to make the path -----------------")
        # File was not made and is not valid
        LVL3_RETURN_VALUE = 0
        WARNING_INIT_ERROR=0
        EXECUTE_PERMIT=False
        # We will try to make the dir
        mode = 0o777  # Example: Owner rwx, Group rwx, Others rwx
        MAKETHISPATH = OS.makedirs(ROWX_LEVEL3,  mode=mode, exist_ok=True)
        VALID_MAKETHISPATH = OS.path.exists(str(ROWX_LEVEL3))
        # Nested -if- make sure the path is now valid after making it.
        if VALID_MAKETHISPATH:
            print(DADASH)
            print("The Level 3 path was made and EXISTS: "+ROWX_LEVEL3)
            print("Now to make it writeable.")
            # We must make the directory writeable. Make sure it is writable.
            valid_chmod777path=OS.system("chmod 777 "+str(ROWX_LEVEL3))
            #Another nested if
            if  valid_chmod777path == 0:  # Another nested if
                LVL3_RETURN_VALUE = 1
                WARNING_INIT_ERROR=1
                EXECUTE_PERMIT=True
                print(DADASH)
                #
            else:
                # File was not made and is not valid
                LVL3_RETURN_VALUE = 0
                WARNING_INIT_ERROR=0
                EXECUTE_PERMIT=False
                print("--CAUTION--")
                print("You are requesting the validity of this Level 3 path: "+str(ROWX_LEVEL3))
                printwarn()
                print("NOTE: We cannot go forward with this directory.")
                print("There is a PERMISSION problem in Linux.")
                printwarn()
                # End of second if block
                #
        else: #Nested -if-
            print("--CAUTION--")
            print("You are requesting the validity of this Level 3 path: "+str(ROWX_LEVEL3))
            printerr()
            print("-------The indicated path is INVALID! -----------------")
            print("-------We DID try to make the path, but still failed -----------------")
            printerr()
            # File was not made and is not valid
            LVL3_RETURN_VALUE = 0
            WARNING_INIT_ERROR=0
            EXECUTE_PERMIT=False
            # End of 1st nested if block
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
#       # #Level 3 if (bottom of loop)
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
    if (LEVEL2_RETURN_VALUE == 1 and LVL3_RETURN_VALUE ==1) and EXECUTE_PERMIT==True:
        EXECUTE_PERMIT=True
        print("Both directories are valid! Now make sure the execute col is set to yes!")
    else:
        EXECUTE_PERMIT=False

#    # Only perform the contruction of commands for cases with execute set to yes.
#    # We will call this the execute test
#    if "yes" in ROWX_execute:
#        EXECUTE_PERMIT=True
#    else:
#        EXECUTE_PERMIT=False

    # The first test only makes sure that both directories are valid.
    # What if a sole directory is not valid?
    # This is redundant,but I thought it is best to ensure.
    if (LEVEL2_RETURN_VALUE == 0 or LVL3_RETURN_VALUE ==0 or EXECUTE_PERMIT=False):
        EXECUTE_PERMIT=False
        #
        printerr()
        print("One of the data directories are not valid!")
        print("We will not make the scripts!")
        printerr()

    # We are testing to make sure that the radar identifier is a current NEXRAD ICAO.
    if RADAR_ID_CORRECT == 0:
        #
        EXECUTE_PERMIT=False
        printerr()
        print("One of the radar-sites has an invalid identifer!")
        print("Check this, we will not make scripts!")
        printerr()
    # Now we are going to make the ksh scripts and wite them out.
    # Make_the_KSH
    if EXECUTE_PERMIT:     # We spent effort to ensure EXECUTE_PERMIT
                           # is only set to true if there are no errors.
        #========
        #
        print("Screen 3:  playback instructions from row "+str(x))
        print("Will we execute? Setting:"+str(ROWX_execute)+"\n")
        print("Job Number: "+str(ROWX_JOB_NUMBER)+"\n\n")
        #
        FNAME_SC3="case"+str(ROWX_JOB_NUMBER)+"screen3.ksh"
        ksh_file_name=KSH_SCRIPTS+FNAME_SC3
        writefileobj = open(ksh_file_name, "w")
        print("File name: "+str(FNAME_SC3)+"\n")
        FIRST_LINE  ="#!/bin/ksh\n"
        SECOND_LINE ="#\n"
        THIRD_LINE  ="# Screen 3 playback instructions\n"
        FOURTH_LINE ="/export/home/${USER}/bin/lnux_x86/mrpg cleanup\n"
        FIFTH_LINE  ="/export/home/${USER}/bin/cad "+ROWX_radarsite.lower()+" 1\n"
        SIXTH_LINE  ="/export/home/${USER}/bin/lnux_x86/mrpg -p startup\n"
        ## The [:2] is to remove the decimal from the ISDP.
        ROWX_ISDP2  = str(ROWX_ISDP)[:2]
        SEVENTH_LINE="/export/home/${USER}/bin/lnux_x86/show_isdp -i "+str(ROWX_ISDP2)+"\n"
        EIGTH_LINE  ="/export/home/${USER}/bin/lnux_x86/hci &\n"
        NINTH_LINE  ="\n\n"
        script_list_set=[FIRST_LINE, SECOND_LINE, THIRD_LINE, FOURTH_LINE, FIFTH_LINE, \
                         SIXTH_LINE, SEVENTH_LINE, EIGTH_LINE, NINTH_LINE]
        for new_line in script_list_set:
            print(new_line)
            writefileobj.write(new_line)
            # End of loop
        # Close file.
        writefileobj.close()
        #
        print(DADOTS+" 2")
        print("Screen 2:  Playback instructions from row "+str(x))
        #
        FNAME_SC2="case"+str(ROWX_JOB_NUMBER)+"screen2.ksh"
        ksh_file_name=KSH_SCRIPTS+FNAME_SC2
        writefileobj = open(ksh_file_name, "w")
        print("File name: "+str(FNAME_SC2)+"\n")
        print("File name: case"+str(ROWX_JOB_NUMBER)+"screen2.ksh\n")
        # print("#!/bin/ksh") # Print FIRST_LINE
        ## FIRST_LINE and second line will be the same for all scripts.
        # print("#")          # Print SECOND_LINE
        #
        THIRD_LINE  ="# Screen 2 playback instructions\n"
        #FOURTH_LINE ="/export/home/orpg2/bin/ecl 1 "+str(ROWX_LEVEL3)
        FOURTH_LINE ="/home/pmccrone/python/src/ecl/ecl3sb2 1 "+str(ROWX_LEVEL3)
        FIFTH_LINE  ="\n"
        script_list_set=[FIRST_LINE, SECOND_LINE, THIRD_LINE, FOURTH_LINE, FIFTH_LINE]
        for new_line in script_list_set:
            print(new_line)
            writefileobj.write(new_line)
        # Close file.
        writefileobj.close()
        #
        print(DADOTS+" 0")
        print("Screen 0:  Playback instructions from row "+str(x))
        #
        FNAME_SC0="case"+str(ROWX_JOB_NUMBER)+"screen0.ksh"
        ksh_file_name=KSH_SCRIPTS+FNAME_SC0
        writefileobj = open(ksh_file_name, "w")
        print("File name: "+str(FNAME_SC0)+"\n")
        print("File name: case"+str(ROWX_JOB_NUMBER)+"screen0.ksh\n")
        # print("#!/bin/ksh")  # Print FIRST_LINE
        ## FIRST_LINE and second line will be the same for all scripts.
        # print("#")           # Print SECOND_LINE
        THIRD_LINE  ="# Screen 0 playback instructions\n\n"
        FOURTH_LINE ="cd "+str(ROWX_levelII)+"\n"
        #FIFTH_LINE  ="/export/home/${USER}/bin/lnux_x86/play_a2 -i\n" #Python 2 orignal
        FIFTH_LINE  ="/home/pmccrone/python/src/play_a2/play_a2.ksh\n" #PYTHON 3
        SIXTH_LINE  ="\n"
        #
        script_list_set=[FIRST_LINE, SECOND_LINE, THIRD_LINE, FOURTH_LINE, FIFTH_LINE, SIXTH_LINE]
        for new_line in script_list_set:
            print(new_line)
            writefileobj.write(new_line)
            # End of loop
        # Close file.
        writefileobj.close()
        #
        print(DADOTS+" 4")
        print("Screen 4:  Playback instructions from row "+str(x))
        #
        FNAME_SC4="case"+str(ROWX_JOB_NUMBER)+"screen4.ksh"
        ksh_file_name=KSH_SCRIPTS+FNAME_SC4
        writefileobj = open(ksh_file_name, "w")
        print("File name: "+str(FNAME_SC4)+"\n")
        print("File name: case"+str(ROWX_JOB_NUMBER)+"screen4.ksh\n")
        THIRD_LINE  ="# Screen 4 playback instructions\n"
        #FOURTH_LINE ="/usr/bin/script "+str(ROWX_LEVEL3)+"/lem_capture.txt\n"
        FOURTH_LINE ="/usr/bin/cd "+str(ROWX_LEVEL3)+"\n"
        FIFTH_LINE  ="#capture\n"
        SIXTH_LINE = "echo Type the COMMAND >capture< <PRESS RETURN> \n"
        script_list_set=[FIRST_LINE, SECOND_LINE, THIRD_LINE, FOURTH_LINE, FIFTH_LINE, SIXTH_LINE]
        for new_line in script_list_set:
            print(new_line)
            writefileobj.write(new_line)
            # End of loop
        # Close file.
        writefileobj.close()
        #
        # Screen 1 - Change 10/3/2023 PJM
        #
        print(DADOTS+" 1")
        print("Screen 1:  Playback instructions from row "+str(x))
        #
        FNAME_SC1="case"+str(ROWX_JOB_NUMBER)+"screen1.ksh"
        ksh_file_name=KSH_SCRIPTS+FNAME_SC1
        writefileobj = open(ksh_file_name, "w")
        print("File name: "+str(FNAME_SC1)+"\n")
        print("File name: case"+str(ROWX_JOB_NUMBER)+"screen1.ksh\n")
        # print("#!/bin/bash")  # Print FIRST_LINE
        ## FIRST_LINE and second line will be the same for all scripts.
        # print("#")           # Print SECOND_LINE
        THIRD_LINE  ="# Screen 1 playback instructions\n"
        FOURTH_LINE ="cd "+str(ROWX_LEVEL3)+"\n"
        FIFTH_LINE  ="/usr/bin/ls\n"
        SIXTH_LINE  ="echo cd "+str(ROWX_LEVEL3)+"\n"
        SEVENTH_LINE="echo If rerunning this- remove all files with  rm -rf star.star"
        script_list_set=[FIRST_LINE, SECOND_LINE, THIRD_LINE, FOURTH_LINE, \
                         FIFTH_LINE, SIXTH_LINE, SEVENTH_LINE]
        for new_line in script_list_set:
            print(new_line)
            writefileobj.write(new_line)
            # End of loop
        # Close file.
        writefileobj.close()
        #End loop
    else:
        print("\nCase Number: "+str(ROWX_JOB_NUMBER))
        print(" was set to no.\nWe will not make files for this case.")
        print("Check to make sure the paths to data files are correct.\n")
    #### End of the execute tst
#### This is the end of main X loop
### WE make the scripts rwx (777) to be executable.
try:
    OS.system("chmod 777 "+str(KSH_SCRIPTS)+"*.*")
    print("All scripts were set to -rwxrwxr-x\n")
except:  # pylint: disable=bare-except
    print("There was a problem with changing permissions.\n")

print(DADASH)
print("Here is the BIG ERROR LIST:")
printerr()
print(BIGERRORLIST)
printerr()

print("-------Program END EXECUTION - "+str(PROGRAM_NAME)+" -----------------")
print(DADASH)

##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--## END OF PYTHON CODE

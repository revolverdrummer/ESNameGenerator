# Only works in Python 3.6.7 32 Bit. Navigate to the directory of Python 3.6.7 and into the Scripts folder. Open a command prompt in that directory and run 'pip3.6.exe install pypyodbc' without the quotes. The program should then work from a Python 3.6.7 32 bit interpreter.
# This program was written in December 2018 by RevolverDrummer
# The only library that needs to be installed is pypyodbc. Once this is on a the system, this program will work.

import random
import pypyodbc
import os.path

# Get the absolute path of the working environment for the eventual SQL connection
pathVar = os.path.abspath("")
dbPathVar = os.path.abspath("es_names_real.mdb")

# Flip the backslashes to forward slashes in the abs path
for i in pathVar:
    pathVar = pathVar.replace("\\","/")

# Flip the backslashes to forward slashes in the abs path of the database
for i in dbPathVar:
    dbPathVar = dbPathVar.replace("\\","/")

# Main Menu for greeting the user and asking for the race of their character.
def main_menu():
    """Returns the corresponding number of the race that the user selected

    :param raceNum (string) the number the user selects for the corresponding race
    :return raceNum (string)
    """
    print(" _________________________________________________")
    print("/\\                                                \\")  
    print("\_|                                                |") 
    print("  |  Welcome to the Elder Scrolls Name Generator!  |")
    print("  |  Please select a race for your character:      |")
    print("  |                                                |")
    print("  |      1. Altmer           2. Argonian           |")
    print("  |      3. Bosmer           4. Breton             |")
    print("  |      5. Dunmer           6. Imperial           |")
    print("  |      7. Khajiit          8. Nord               |")
    print("  |      9. Orsimer          10. Redguard          |")
    print("  |                                                |")
    print("  |  ______________________________________________|_")
    print("  \_/_______________________________________________/")
    while True:
        raceNum = input()
        try:
            int(raceNum)
            if int(raceNum) < 1 or int(raceNum) > 10:
                print("Please input a valid option (Number 1 through 10.)")
            else:
                break    
        except:
            print("Please input a valid option (Number 1 through 10.)")
    return raceNum

# Funtion for races with only one name
def first_only(race, gender):
    """Returns a random name for a race with only one name

    :param namelist (list) The Python list that all the names for the selected race and gender. Will be populated from the backend database.
    :param con (string) The main variable set to handle the SQL functions
    :param name (string) The Python Variable to store names as they come in from the SQL database
    :param fstatement (string) The SQL statment to be executed
    :param firstname (string) The variable to represent the selected first name of the random choice
    :param race (string) The race the user inputted
    :param gender (string) The gender the user inputted
    :return name (string) the selected name for the user
    """
    # Altmer, Bosmer, Argonians, and Khajiit do not have traditional surnames.
    namelist = []
    # The connect statement to initialize the Python connection to the SQL server.
    con = pypyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL={MS Access};DriverId=25;DefaultDir='+pathVar+';DBQ='+dbPathVar+'')
    # I believe this 'selects' the first area in the SQL database, essentially prepping it for parsing.
    name = con.cursor()
    # Preparing the SQL statement outside of the execute function so that the Python variables can be passed in easily.
    fstatement = "SELECT first FROM Names WHERE race='"+race+"' AND gender='"+gender+"'"
    # Execute the SQL statement
    name.execute(fstatement)
    # Get all the names that match the SQL query and append them to the list within Python.
    for row in name.fetchall():
        namelist.append(str(row))
    # From the newly formed Python list, pick a random name.
    firstname = random.choice(namelist)
    # Normalize (take out the parenthesis and comma) the chose name.
    firstname = firstname[2:-3]
    # Capitalize the race to make the final output pretty.
    race = race.capitalize()
    # Print the final result to the user.
    return firstname

# Function for races with a first and last name
def first_last(race, gender):
    """Returns a random name for a race with a first name and last name

    :param fnamelist (list) The Python list that all the first names for the selected race and gender. Will be populated from the backend database.
    :param lnamelist (list) The Python list that all the last names for the selected race and gender. Will be populated from the backend database.
    :param con (string) The main variable set to handle the SQL functions
    :param fname (string) The Python Variable to store first names as they come in from the SQL database
    :param fstatment (string) The first name SQL statement to be executed
    :param lname (string) The Python Variable to store last names as they come in from the SQL database
    :param lstatement (string) The last name SQL statement to be executed
    :param firstname (string) The variable to represent the selected first name of the selection
    :param lastname (string) The variable to represent the selected last name of the selection
    :param race (string) The race the user inputted
    :return name (string) The selected name for the user
    """
    # Initialize the lists for both first names and last names.
    fnamelist = []
    lnamelist = []
    # The connect statement to initialize the Python connection to the SQL server. 
    con = pypyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL={MS Access};DriverId=25;DefaultDir='+pathVar+';DBQ='+dbPathVar+'')
    # I believe this 'selects' the first area in the SQL database, essentially prepping it for parsing. Only done for the first name side of things.
    fname = con.cursor()
    # Preparing the SQL statement outside of the execute function so that the Python variables can be passed in easily. This statement only applies to first names.
    fstatement = "SELECT first FROM Names WHERE race='"+race+"' AND gender='"+gender+"'"
    # Execute the SQL statement
    fname.execute(fstatement)
    lname = con.cursor()
    # Preparing the SQL statement outside of the execute function so that the Python variables can be passed in easily. This statement only applies to last names.
    lstatement = "SELECT last FROM Names WHERE race='"+race+"' AND last<>'None'"
    # Execute the SQL statement
    lname.execute(lstatement)
    # Get all the first names that match the SQL query and append them to the first name list within Python.
    for row in fname.fetchall():
        fnamelist.append(str(row))
    # Get all the last names that match the SQL query and append them to the last name list within Python.
    for row in lname.fetchall():
        lnamelist.append(str(row))
    # From the newly formed first name Python list, pick a random name.
    firstname = random.choice(fnamelist)
    # Normalize (take out the parenthesis and comma) the chose name.
    firstname = firstname[2:-3]
    # From the newly formed last name Python list, pick a random name.
    lastname = random.choice(lnamelist)
    # Normalize (take out the parenthesis and comma) the chose name.
    lastname = lastname[2:-3]
    # Capitalize the race to make the final output pretty.
    race = race.capitalize()
    # Print the final result to the user.
    name = firstname+" "+lastname
    return name

#Main
# Variable for repeating loop set to yes initially.
repeater = 'y'
# Sametype set to no so user can set initial values desired.
sametype = 'n'
race = ""
# Start the main loop.
while repeater == 'y':
    race = race.lower()
    # If the user does not want the same type (or is the first time) get their desired race and gender option.
    if sametype != 'y':
        # Call the main menu function to get the race.
        raceNum = main_menu()
        # Set the user's chosen number to the corresponding race.
        if raceNum == "1":
            race = "altmer"
        elif raceNum == "2":
            race = "argonian"
        elif raceNum == "3":
            race = "bosmer"
        elif raceNum == "4":
            race = "breton"
        elif raceNum == "5":
            race = "dunmer"
        elif raceNum == "6":
            race = "imperial"
        elif raceNum == "7":
            race = "khajiit"
        elif raceNum == "8":
            race = "nord"
        elif raceNum == "9":
            race = "orsimer"
        elif raceNum == "10":
            race = "redguard"
        # Ask for the gender of the character.
        while True:
            gender = input('What is the gender of the character you are creating? ')
            if gender == "male" or gender == "female":
                break
            else:
                print("Please input a compatible answer (male/female)")
        # Normalize the input to be lowercase.
        gender = gender.lower()
        

    # Single name races
    if race == 'altmer' or race == "argonian" or race == "bosmer" or race == "khajiit":
        # Call the first only function and pass in the race and gender variables. Get the name back.
        name = first_only(race, gender)
        # Print the user's generated name
        race = race.capitalize()
        print("Your "+race+"'s random name is "+name+".")
    # Two name races
    elif race == 'breton' or race == "dunmer" or race == "imperial" or race == "nord" or race == "orsimer" or race == "redguard":
        # Call the two name function and pass in the race and gender variables. Get the name back.
        name = first_last(race, gender)
        # Print the user's generated name
        race = race.capitalize()
        print("Your "+race+"'s random name is "+name+".")
    else:
        # If the user inputs something outside expected input then tell them it was invalid.
        print("Invalid Input")
    # Ask the user if they'd like to generate another name.
    repeater = input("Would you like to do another name? (y/n) ")
    # If they want to generate another name ask if they want it to be the same race and gender
    if repeater == 'y':
        sametype = input("Same race and gender? (y/n) ")
    # If they don't say yes to making another name, break the loop
    else:
        break
# Thank the user for their time and wait before exiting the program.
input("Thank you for using the Elder Scrolls Name Generator! [Press Enter to Exit]")

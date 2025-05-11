from secrets import randbelow
from datetime import datetime
from csv import reader
from sys import exit
import pyperclip

def get_name():
    # Defines a while loop that breaks once the user provides a valid first name
    while True:
        # Prompts user for first name of guest and saves it in a name variable
        first_name = input("Who's coming? First name: ")
        if not first_name.isalpha():
            print ("Invalid entry. Alphabetical characters only.")
        else:
            first_name = first_name.title().rstrip()
            break

    # Defines a while loop that breaks once the user provides a valid last name
    while True:
        # Prompts user for last name of guest and saves it in a name variable
        last_name = input("Last name: ")
        if not last_name.isalpha():
            print ("Invalid entry. Alphabetical characters only.")
        else:
            last_name = last_name.title().rstrip()
            break

    # Concatenates the first and last names, adding space between
    full_name = first_name + " " + last_name
    return full_name, first_name

def get_date():
    # Defines a while loop that breaks once the user provides a correct date
    while True:
        # Prompts user for date of arrival in MM/DD/YYYY format
        date_string = input("When do they arrive? MM/DD/YYYY: ")
        # Converts the string input to a datetime object
        # Catches incorrect entries and stops the script
        try:
            date_object = datetime.strptime(date_string, "%m/%d/%Y").date()
            break
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY.")
    return date_object

# Generates a list of eight random integers
def gen_door_code():
    random_ints = []
    for i in range(8):
        random_ints.append(randbelow(10))
    return random_ints

# Gets the list of random integers
# Reruns gen_door_code if the first digit is zero
# Lock does not support such codes
# Converts the list into an integer value
def get_door_code():
    result = gen_door_code()
    first_int = result[0]
    while first_int == 0:
        result = gen_door_code()
        first_int = result[0]
        print("Ooops! Got a leading zero. Generating a new code.")
    door_code = int(''.join(map(str, result)))
    return door_code

# Ensures door code was not used already
def ensure_unique(code):
    with open('door-codes.csv') as f:
        for num, row in enumerate(reader(f)):
            if code in row[1]:
                print(
                    "Collision! That door code was already issued! "
                    "Generating a new code. See {} {}.".format(num, row)
                )
                get_door_code()
            else:
                break

guest_long, guest_short = get_name()
print("long name {}, short name {}".format(guest_long, guest_short))
door_code = get_door_code()
ensure_unique(str(door_code))
arrival = get_date()

# Appends the guest's full name, code, and arrival date in local CSV file
def store_code():
    try:
        with open('door-codes.csv', 'a') as f:
            f.write("{},{},{}\n".format(guest_long, door_code, arrival))
            # Prints summary message
            print(
                "Added guest {} to door_codes.csv: using code {}, arriving {}".
                format(guest_long, door_code, arrival)
            )
    except FileNotFoundError as e:
        print(f"Error! Couldn't find the {e.filename} file. Please fix this, then rerun the script")
        exit(1)

def get_dropoff():
    # Defines a while loop that asks user if guest requested luggage drop off
    while True:
        dropoff = input('Did they request luggage drop off? Y or N: ').lower().strip()
        if dropoff == 'y':
            return True
        elif dropoff == 'n':
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

def get_baby():
    # Defines a while loop that asks user if guest is bringing infant
    while True:
        baby = input('Are they bringing an infant? Y or N: ').lower().strip()
        if baby == 'y':
            return True
        elif baby == 'n':
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

def gen_long_msg():
    dropoff = get_dropoff()
    baby = get_baby()
    if dropoff and not baby:
        file_name = 'welcome-dropoff.txt'
    elif baby and not dropoff:
        file_name = 'welcome-baby.txt'
    elif dropoff and baby:
        file_name = 'welcome-baby-dropoff.txt'
    else:
        file_name = 'welcome-regular.txt'
    try:
        with open(file_name, 'r') as f:
            welcome_long = f.read()
            welcome_long = welcome_long.replace('GUEST_NAME', guest_short)
            welcome_long = welcome_long.replace('DOOR_CODE', str(door_code))
            pyperclip.copy(welcome_long)
            print("Copied long message to clipboard! I'll wait for you to paste it.")
            input("Press Enter when you're ready for the short message.")
    except FileNotFoundError as e:
        print(f"Error! Couldn't find the {e.filename} file. Please fix this, then rerun the script.")
        exit(1)

def gen_short_msg():
    try:
        with open('welcome-short.txt', 'r') as f:
            welcome_short = f.read()
            welcome_short = welcome_short.replace('DOOR_CODE', str(door_code))
            pyperclip.copy(welcome_short)
            print("Copied short message to clipboard! I'll wait for you to paste it.")
            input("Press Enter when you're done.")
    except FileNotFoundError as e:
        print(f"Error! Couldn't find the {e.filename} file. Please fix this, then rerun the script")
        exit(1)

gen_long_msg()
gen_short_msg()
store_code()

print("Thank you for using this script. Have a great day.")


from secrets import randbelow
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from csv import reader, writer
from sys import exit
import pyperclip
import os
import re

env = Environment(
    loader=FileSystemLoader('.')
)

template_long = env.get_template("welcome_long.txt")
template_short = env.get_template("welcome_short.txt")
print(template_long, template_short)

def get_name():
    # Defines a while loop that breaks once the user provides a valid first name
    while True:
        # Prompts user for first name of guest and saves it in a name variable
        first_name = input("Who's coming? First name: ")
        if not all(x.isalpha() or x.isspace() for x in first_name) or first_name == "":
            print ("Invalid or empty entry. Alphabetical characters and spaces only.")
        else:
            first_name = first_name.title().rstrip()
            break

    # Defines a while loop that breaks once the user provides a valid last name
    while True:
        # Prompts user for last name of guest and saves it in a name variable
        last_name = input("Last name: ")
        if not all(x.isalpha() or x.isspace() for x in last_name) or last_name == "":
            print ("Invalid entry. Alphabetical characters and spaces only.")
        else:
            last_name = last_name.title().rstrip()
            break

    # Concatenates the first and last names, adding space between
    full_name = first_name + " " + last_name
    return full_name, first_name

guest_long, guest_short = get_name()
print(f"long name {guest_long}, short name {guest_short}")

def check_repeat():
    repeat = False
    stays = 1
    door_code = ""
    with open('door_codes.csv') as f:
        for row in reader(f):
            if row[0].strip().lower() == guest_long.strip().lower():
                print(f"Someone named '{row[0]}' stayed with you on {row[2]}.")
                confirmation = input(f"Could '{guest_long}' be a repeat visitor? ")
                if confirmation.lower() in ['yes', 'y']:
                    door_code = row[1]
                    stays = int(row[3]) + 1
                    repeat = True
                    print(
                        f"Congratulations! Using same door code {door_code}. "
                        f"and incrementing stay count to {stays}."
                    )
                else:
                    print(f"Treating {guest_long} as a new guest.")
                break
    return repeat, door_code, stays

def get_date():
    # Defines a while loop that breaks once the user provides a correct date
    while True:
        # Prompts user for date of arrival in MM/DD/YYYY format
        date_string = input("When do they arrive? MM/DD/YYYY: ")
        # Converts the string input to a datetime object
        # Catches incorrect entries and stops the script
        try:
            date_object = datetime.strptime(date_string, "%m/%d/%Y").date()
            return date_object
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY.")

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
    # Check if door code already exists and regenerate if needed.
    with open('door_codes.csv') as f:
        existing_codes = [row[1] for row in reader(f)]
    
    # Keep generating until we get a unique code
    while str(code) in existing_codes:
        print(f"Collision! Code {code} already exists. Generating new code.")
        code = get_door_code()
        print(code)
    
    return code

def finalize_door_code():
    repeat, door_code, stays = check_repeat()
    if repeat:
        print("Skipping new door code generation, repeat visitor.")
    else: 
        door_code = get_door_code()
        door_code = ensure_unique(door_code)
    return repeat, door_code, stays
        
repeat, door_code, stays = finalize_door_code()

arrival = get_date()

# Opens local door_codes.csv file and either:
# appends new guest's full name, door code, and arrival date
# or updates returning guest's arrival date and number of stays
def store_code():
    try:
        rows = []
        found = False

        # Read in existing rows if file exists
        if os.path.exists("door_codes.csv"):
            with open("door_codes.csv", newline="") as f:
                for row in reader(f):
                    if repeat and row[0] == guest_long:
                        # Update arrival and stays, set found var
                        row[2] = arrival
                        row[3] = str(stays)
                        found = True
                    rows.append(row)

        # If guest not found, append as new row
        if not found:
            rows.append([guest_long, door_code, arrival, str(stays)])
            print(
                f"Added guest {guest_long} to door_codes.csv: using code "
                f"{door_code}, arriving {arrival}, number of stays {stays}."
            )
        else:
            print(f"Updated guest {guest_long} in door_codes.csv.")

        # Write everything back
        with open("door_codes.csv", "w", newline="") as f:
            w = writer(f)
            w.writerows(rows)

    except Exception as e:
        print(
            f"Error! Something went wrong: {e}. Please fix this, "
            f"then rerun the script."
        )
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
    context = {
        "guest_name": guest_short,
        "door_code": door_code,
        "repeat": repeat,
        "baby": baby,
        "dropoff": dropoff
    }

    try:
        welcome_long = template_long.render(
            guest_name=guest_short,
            door_code=door_code,
            repeat=repeat,
            baby=baby,
            dropoff=dropoff
        )
        welcome_long = re.sub(r'\n\n+', '\n\n', welcome_long)
        pyperclip.copy(welcome_long)
        print("Copied long message to clipboard! I'll wait for you to paste it.")
        input("Press Enter when you're ready for the short message.")

    except FileNotFoundError as e:
        print(
            f"Error! Couldn't find the {e.filename} file. Please fix this, "
            f"then rerun the script."
        )
        exit(1)

def gen_short_msg():
    context = {
        "door_code": door_code
    }

    try:
        welcome_short = template_short.render(
            door_code=door_code
        )
        pyperclip.copy(welcome_short)
        print("Copied short message to clipboard! I'll wait for you to paste it.")
        input("Press Enter when you're done.")
    except FileNotFoundError as e:
        print(
            f"Error! Couldn't find the {e.filename} file. Please fix this, "
            f"then rerun the script"
        )
        exit(1)

gen_long_msg()
gen_short_msg()
store_code()

print("Thank you for using this script. Have a great day.")


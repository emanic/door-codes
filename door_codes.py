from secrets import randbelow
from datetime import datetime
from csv import reader

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
        # Prompts user for first name of guest and saves it in a name variable
        last_name = input("Last name: ")
        if not last_name.isalpha():
            print ("Invalid entry. Alphabetical characters only.")
        else:
            last_name = last_name.title().rstrip()
            break

    # Concatenates the first and last names, adding space between
    full_name = first_name + " " + last_name
    return full_name

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
                get_door_code()
                print(
                    "Collision! That door code was already issued! "
                    "Generating a new code. See {} {}.".format(num, row)
                )

# Appends the guest name, code, and arrival date to local CSV file
with open('door-codes.csv', 'a') as f:
    guest = get_name()
    door_code = get_door_code()
    ensure_unique(str(door_code))
    arrival = get_date()
    f.write("{},{},{}\n".format(guest, door_code, arrival))

# Prints summary message
print(
    "Added guest {}, using code {}, arriving {}".
    format(guest, door_code, arrival)
)

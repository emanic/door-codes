# Random door code generator script

## About the script

Python script that automates the generation and storage of random, 
eight-digit codes for smart locks. 

It checks for repeat guests and tracks the number of stays. 
It reuses the door code of a repeat guest.

It ensures that the code does not start with zero as many locks cannot
accept such values. It also checks that the code has not already been
used. If it has, it generates a new code.

It stores the code along with the name of the guest and the date of their 
arrival in a local CSV file. 

It then inserts the name of the guest and their code into a long, then 
short welcome message which it pastes to your clipboard. It supports several 
variations for the long welcome message.

This could be useful for short-term rental hosts using platforms like 
Airbnb, Vrbo, etc.


## Getting started

The script makes use of [pyperclip](https://github.com/asweigart/pyperclip) 
to interact with the local clipboard. 

1. (Linux only) If you are on Linux, you need to 
   install [xclip](https://github.com/astrand/xclip). 

   ```
   sudo apt install xclip
   ```

1. Install the other dependencies.

   ```
   pip3 install -r requirements.txt
   ```

1. Create the following local files:

   - **door_codes.csv**: can be blank

   - **welcome_regular.txt**: long message for regular check in containing strings 
     GUEST_NAME and DOOR_CODE

   - **welcome_dropoff.txt**: long message for guest wanting luggage dropoff containing 
     strings GUEST_NAME and DOOR_CODE

   - **welcome_baby.txt**: long message for guest bringing infant containing strings 
     GUEST_NAME and DOOR_CODE

   - **welcome_baby_dropoff.txt**: long message for guest dropping off lugagge _and_ bringing 
     infant containing strings GUEST_NAME and DOOR_CODE

   - **welcome_short.txt**: short message containing string DOOR_CODE


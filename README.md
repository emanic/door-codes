# Random door code generator script

## About the script

Python script that automates the generation and storage of random, 
eight-digit codes for smart locks. 

It ensures that the code does not start with zero as many locks cannot
accept such values. It also checks that the code has not already been
used. If it has, it generates a new code.

It stores the code along with the name of the guest and the date of their 
arrival in a local CSV file. 

It then inserts the name of the guest and their code into a welcome 
message which it pastes to your clipboard.

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

   - **door-codes.csv**: can be blank
   - **welcome-long.txt**: long message containing strings GUEST_NAME and DOOR_CODE
   - **welcome-short.txt**: short message containing string DOOR_CODE


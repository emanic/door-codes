# Random door code generator script

## About the script

Python script that automates the generation and storage of random, 
eight-digit codes for smart locks. It also helps with customizing
welcome messages.

It checks for repeat guests and tracks the number of stays. 
It reuses the door code of a repeat guest.

It ensures that the code does not start with zero as many locks cannot
accept such values. It also checks that the generated code has not already been
used. If it has, it generates a new code.

It stores the code along with the name of the guest and the date of their 
arrival in a local CSV file. 

It uses [Jinja](https://jinja.palletsprojects.com/en/stable/)
to allow for templating long and short welcome messages, which
are pasted in succession to your clipboard for convenience.
By default, the script sets the following variables for use in templating
your welcome messages:

- Repeat guest 
- Luggage dropoff request
- Bringing an infant
- Door code
- Guest name

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

   - **welcome_long.txt**: long message, pasted first to clipboard

   - **welcome_short.txt**: short message, pasted second to clipboard (TL;DR-type guests)


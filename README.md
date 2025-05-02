# Random door code generator script

Python script that automates the generation and storage of random, 
eight-digit codes for smart locks. 

It ensures that the code does not start with zero as many locks cannot
accept such values. It also checks that the code has not already been
used. If it has, it generates a new code.

It stores the code along with the name of the guest and the date of their 
arrival in a local CSV file. 

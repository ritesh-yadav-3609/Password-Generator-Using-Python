
# Random Password Generator
---------
## Configuration

### Installation
Install pycrypto library using 'pip install library' command

### Generate Data
Using datagenerator.py file generate random data and save in data.cf and data.df file

_________

## Generate Password

## First time generating password
1. Enter proper detail in 'user_data' variable in main.py file.
2. Enter the filename in the 'filename' variable in the main.py file to store the data to retrieve the password.
   You can use the same file name to store multiple password details.
3. Change the digit from 'values' variable and make sure it contain 3 large number seperated by space.
   Make sure enter the same value in 'values' variable for same file all the time.
4. Make 'generate' value True.
5. Run the code it will give you password.

## Retrieving password again
1. Make 'generate' value False
2. Enter the same number in 'values' variable which was entered while creating the password.
3. Enter the file name in 'filename' variable which the data is saved to retrieve the password 
4. Run the code it will give you old password again.


import random


"""
This function generate randow character and store in data.cf file
"""
# file = open("data/data.cf", "a+")
# charr = ["a","q","w","e","r","2","t","y","9","0","u","i","o","p","s","d","1","f","g","h","j","k","l","z","x","c","v","b","n","m","Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L","Z","X","C","V","B","N","6","M","!","?","5","<",">"," ",",",".","4","[","]","{","@","#","$","7","^","&","*","(",")","-","+","=","3","_","8","}","|",";",":"]
# for i in range(1,88990004):
#     num =  random.choice(charr)
#     file.write(num)
#     if i%100:
#         print('Number of characters in text file :', i, num)

"""
This function generate randow digit and store in data.df file
"""
# file = open("data/data.df", "a+")
# for i in range(1,88990004):
#     num =  random.randrange(1000000,999999999,7)
#     file.write(num)
#     if i%100:
#         print('Number of characters in text file :', i, num)


"""
Get number of character present in data.cf file
"""
file = open("data/data.cf", "r")
data = file.read()
number_of_characters = len(data)
print('Number of characters in text file :', number_of_characters)


"""
Get number of digit present in data.df file
"""
file = open("data/data.df", "r")
data = file.read()
number_of_characters = len(data)
print('Number of characters in text file :', number_of_characters)
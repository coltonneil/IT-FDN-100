"""
This module takes input from the user and outputs a string with the given inputs included
"""


# function to get users age and verify that the entered value is a number
def getage():
    # validate age, if invalid prompt user to re-enter
    while True:
        try:
            entered_age = int(input('How old are you? '))
        except ValueError:
            print('Uh oh, make sure your age is a number.')
            continue
        if entered_age <= 0:
            print('Oops you should probably be older than 0.')
            continue
        else:
            break
    return entered_age


# takes data input by user and prints it
def giveresponse(m_age,name,age,location):
    # create appropriate response based on age difference
    if m_age == age:
        age_string = 'the same age as me!'
    elif m_age > age:
        age_string = str(m_age - age) + ' year(s) younger than me.'
    else:
        age_string = str(age - m_age) + ' year(s) older than me.'
    print('Hello ' + name + ' from ' + location + ', you are ' + age_string)


# defines my age
my_age = int(24)
# get users name
user_name = input('What is your name? ').capitalize()
# get users age
user_age = getage()
# get users location
user_from_location = input('Where are you from? ').capitalize()
# call function giveresponse
giveresponse(my_age,user_name,user_age,user_from_location)



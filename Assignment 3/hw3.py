"""
Gets two numbers from a user, creates a list of numbers between those two values, prints the evens and their indexes
and sums the odds
"""


def init():
    # get start and end number from user
    user_start_num = get_num(1)
    user_end_num = get_num(user_start_num * 5)

    # build list of number from user start and end using range, initialize odd_list
    num_list = list(range(user_start_num, user_end_num + 1))
    odd_list = []

    display_results(user_start_num, user_end_num, num_list, odd_list)


# returns a validated number from the user that must be greater than num_min
def get_num(num_min):
    while True:
        tmp_num = input("Please enter a number greater than or equal to {}: ".format(num_min))
        if not tmp_num.isnumeric():
            print("You must enter a number")
            continue
        tmp_num = int(tmp_num)
        if tmp_num < num_min:
            print("Your number must be greater than or equal to {}: ".format(num_min))
            continue
        else:
            break
    return tmp_num


# checks if number is divisible by 3, 5, or both and returns fizz, buzz, or fizzbuzz as a string
def fizzbuzz(num):
    if num % 3 == 0 and num % 5 == 0:
        result = " - fizzbuzz"
    # if num is divisible by 3
    elif num % 3 == 0:
        result = " - fizz"
    # if num is divisible by 5
    elif num % 5 == 0:
        result = " - buzz"
    # num was not divisible by 3 or 5
    else:
        result = ""
    return result


# print the even numbers and their index, append all odd numbers to odds
def display_results(start, end, numbers, odds):
    print("The even numbers and indexes between {} and {} are: ".format(start, end))
    for index, number in enumerate(numbers):
        if number % 2 == 0:
            print("{} is at the index {} {}".format(number, index, fizzbuzz(number)))
        else:
            odds.append(number)

    # print the sum of the odd numbers between user start and user end
    print("The sum of odd numbers between {} and {} is: {}".format(start, end, sum(odds)))


init()

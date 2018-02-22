#!/usr/bin/env python3

import math

"""
python 3

this script calculates and splits the cost of a pizza order based on the number of slices, it will read names and slice
amount from a file named "order.txt" that is stored in its local directory, if that file is not found it will calculate
based off of a default order
"""

# establish static variables
cost = 10.00
slices_per_pizza = 8
tax_rate = 9.6
tip_rate = 15
delivery_fee = 3.99


# main function where other functions are called and final results are printed
def main():
    order_dict = get_order_dict()
    num_pizzas, left_over_slices = number_pizzas(order_dict)
    total_cost, tip_total = total(num_pizzas)
    tip_by_slice, tip_by_person = get_tip_data(tip_total, order_dict)
    cost_per = round(total_cost / len(order_dict), 2)
    print("You need {} pizzas, there will be {} left over slices".format(num_pizzas, left_over_slices))
    print("The total cost is: ${:.2f}".format(total_cost))
    print("The average cost per person is: ${:.2f}".format(cost_per))
    print("The tip per slice is: ${:.2f}".format(tip_by_slice))
    print("The tip per person, based on their number of slices is as follows:")
    for name, tip in tip_by_person.items():
        print("{} - ${:.2f}".format(name, tip))


# get dict with customer names and slice amounts either from txt file or from dict literal if txt file is missing
def get_order_dict():
    order_data = {}
    try:
        with open("order.txt", 'r') as order_file:
            for line in order_file:
                line = line.strip('\n').split(", ")
                order_data[line[0]] = int(line[1])
    except IOError:
        # use default data if file does not exist
        order_data = {"Dave": 2, "Jessica": 3, "Tom": 4, "Susan": 3, "Bill": 2, "Emily": 4, "Kaycee": 6, "John": 1}
    return order_data


# take dict containing order information and return the number of pizzas and left over slices
def number_pizzas(order_data):
    num_slices = sum(order_data.values())
    num_pizzas = math.ceil(num_slices / slices_per_pizza)
    slice_remainder = num_slices % slices_per_pizza
    if slice_remainder > 0:
        left_over_slices = 8 - (num_slices % slices_per_pizza)
    else:
        left_over_slices = 0
    return num_pizzas, left_over_slices


# take in the number of pizzas need and return the cost of the order (which includes the tip) and the tip amount
def total(num_pizzas):
    pizza_amount = num_pizzas * cost
    tax_amount = pizza_amount * (tax_rate / 100)
    tip_amount = (pizza_amount + tax_amount) * (tip_rate / 100)
    order_cost = pizza_amount + tax_amount + tip_amount + delivery_fee
    return order_cost, tip_amount


# take in the tip amount and the dict storing the order info return a dict key,value =  name, tip based on slices
def get_tip_data(tip, order):
    tip_per_slice = round(tip / sum(order.values()), 2)
    tip_dict = {}
    for name, slices in order.items():
        tip_dict[name] = slices * tip_per_slice
    return tip_per_slice, tip_dict

# takes in a prompt which should state what the user is entering, for instance prompt="Enter the number of slices",
# returns the validated number, this is not used in the txt based version of this script
def get_number(prompt, minimum=1, allow_float=False):
    while True:
        temp_num = input(prompt)
        if allow_float:
            try:
                temp_num = float(temp_num)
            except ValueError:
                print("Please input a valid number")
                continue
        else:
            try:
                temp_num = int(float(temp_num))
            except ValueError:
                print("Please input a valid number")
                continue
        if temp_num < minimum:
            print("The number must be greater than {}".format(minimum))
            continue
        break
    return temp_num

main()
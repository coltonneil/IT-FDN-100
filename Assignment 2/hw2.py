import pickle
import os

"""
"""
menu = ["New report", "Load report", "Delete Report", "Edit tax and fees", "Quit"]

report_options = ["View report", "Save report", "Edit report", "Discard report"]

edit_options = ["Buyer name", "Buyer address", "Buyer phone", "Car", "Car price"]

car_data = {
    "Chevrolet": ["Camaro", "Corvette", "Cruze", "Malibu", "Sonic", "Volt"],
    "Ford": ["Edge", "Focus", "Fusion", "Fusion Hybrid", "Mustang", "Taurus"],
    "Nissan": ["370Z", "Altima", "Leaf", "Maxima", "Murano", "Sentra"],
    "Toyota": ["86", "Avalon", "Camry", "Corolla", "Prius", "Yaris"]
}

report_template = """Hello {}!

Thank you for your purchase of a {}. Following is a break down of your total price:

Sales Price: ${:0.2f}

Tax: ${:0.2f}

Licensing Fee: ${:0.2f}

Dealer Prep Fee: ${:0.2f}

Total Price: ${:0.2f}

You have been assigned an ID number of {}. Please refer to this ID number if you have any questions"""


# present user with menu options new report, load saved report, exit program
def main_menu():
    print("\n--- Main menu ---\n")
    selection = display_options(menu, "Choose an option: ")
    print(selection)
    if selection == 1:
        report_details()
    elif selection == 2:
        load_report()
    elif selection == 3:
        delete_report()
    elif selection == 4:
        edit_fees()
    elif selection == 5:
        print("Exiting...")
        exit(0)
    else:
        print("Invalid input")
        main_menu()


# gather details such as user, car, and pricing
def report_details():
    print("\n--- Report Details ---\n")
    buyer_name = validate_name()
    buyer_addr = validate_addr()
    buyer_phone = validate_phone()
    car = get_car()
    car_price = validate_float("car price")
    user_id = gen_id(buyer_name,buyer_addr)
    report = build_report(buyer_name, buyer_addr, buyer_phone, car, car_price, user_id)
    report_menu(report, buyer_name, buyer_addr, buyer_phone, car, car_price, user_id)


# takes buyer information as input, adds information to the report template and returns the compiled report
def build_report(buyer_name, buyer_addr, buyer_phone, car, car_price, user_id):
    tax_amount = calculate_tax(car_price)
    compiled_report = report_template.format(
        buyer_name,
        car,
        car_price,
        tax_amount,
        fees.get("license fee"),
        fees.get("prep fee"),
        calculate_total(car_price, tax_amount),
        user_id
    )
    return compiled_report


# offers the user options related to the active report
def report_menu(compiled_report, buyer_name, buyer_addr, buyer_phone, car, car_price, user_id):
    print("\n--- Report Menu ---\n")
    selection = display_options(report_options, "Choose an option: ")
    if selection == 1:
        print_report(compiled_report)
        report_menu(compiled_report, buyer_name, buyer_addr, buyer_phone, car, car_price, user_id)
    elif selection == 2:
        save_report(compiled_report, user_id)
    elif selection == 3:
        edit_report(compiled_report, buyer_name, buyer_addr, buyer_phone, car, car_price, user_id)
    elif selection == 4:
        discard_report()
    else:
        print("Invalid input")
        main_menu()


# print report to the screen
def print_report(report):
    print("\n" + report + "\n")
    print("\nPlease review the sales report for accuracy.")


# saves completed report to a file, file name is the unique ID
def save_report(report, user_id):
    print("\n--- Save Report ---\n")
    report_file = open("./reports/" + user_id + ".txt", "w")
    report_file.write(report)
    report_file.close
    print("Report saved to " + user_id + ".txt\nReturning to main menu")
    main_menu()


# edit details of the active report
def edit_report(compiled_report, buyer_name, buyer_addr, buyer_phone, car, car_price, user_id):
    print("\n--- Edit Report ---\n")
    selection = display_options(edit_options, "Choose an option: ")
    if selection == 1:
        buyer_name = validate_name()
    elif selection == 2:
        buyer_addr = validate_addr()
    elif selection == 3:
        buyer_phone = "(912) 247-4965"
    elif selection == 4:
        car = get_car()
    elif selection == 5:
        car_price = validate_float("car price")
    else:
        print("Invalid input")
        edit_report(compiled_report, buyer_name, buyer_addr, buyer_phone, car, car_price, user_id)
    user_id = gen_id(buyer_name, buyer_addr)
    report = build_report(buyer_name, buyer_addr, buyer_phone, car, car_price, user_id)
    report_menu(report, buyer_name, buyer_addr, buyer_phone, car, car_price, user_id)


# discards active report and returns user to the main menu
def discard_report():
    print("\nThe active report has been discarded, returning to the main menu\n")
    main_menu()


# loads a saved report from a file, file name is the unique ID
def load_report():
    print("\n--- Load Report ---\n")
    buyer_name = validate_name()
    buyers_zip = required_string("Buyers zip code: ", required_length=5)
    user_id = gen_id(buyer_name, buyers_zip)
    report_file = open("./reports/" + user_id + ".txt", "r")
    report = report_file.read()
    report_file.close()
    print_report(report)
    main_menu()


# deletes a saved report and returns user to the main menu
def delete_report():
    print("\n--- Delete Report ---\n")
    buyer_name = validate_name()
    buyers_zip = required_string("Buyers zip code: ", required_length=5)
    user_id = gen_id(buyer_name, buyers_zip)
    if os.path.exists("./reports/" + user_id + ".txt"):
        print("Report found")
        while True:
            choice = input("Confirm deletion of " + user_id + ".txt (y/n): ")
            if choice.lower() == "y":
                os.remove("./reports/" + user_id + ".txt")
                print("Report deleted, returning to main menu\n")
                break
            elif choice.lower() == "n":
                print("Deletion cancelled, returning to main menu\n")
                break
            else:
                print("Invalid input")
                continue
    else:
        print("Report found, returning to main menu\n")
    main_menu()


# sets the sales tax, licensing fee, and dealer prep fee
def get_fees():
    try:
        fee_data_in = open("./settings/fees.txt", "rb")
        global fees
        fees = pickle.load(fee_data_in)
        fee_data_in.close()
    except IOError:
        print("\n--- Setup ---\n")
        print("Fees not found. Please set fees.")
        fee_data_out = open("./settings/fees.txt", "wb")
        tax_rate = validate_float("tax rate",True)
        prep_fee = validate_float("preparation fee",True)
        license_fee = validate_float("license fee", True)
        fee_dict = {"tax rate": tax_rate, "prep fee": prep_fee, "license fee": license_fee}
        pickle.dump(fee_dict, fee_data_out)
        fee_data_out.close()
        get_fees()


# edits the sales tax, licensing fee, and dealer prep fee
def edit_fees():
    print("\n--- Edit Fees ---\n")
    get_fees()
    selection = display_options(fees, "Select a fee to edit: ")
    tmp_fee = validate_float(selection, True)
    fees.update({selection:tmp_fee})
    fee_data_out = open("./settings/fees.txt", "wb")
    pickle.dump(fees, fee_data_out)
    fee_data_out.close()
    print("Fees have been updated, returning to the main menu")
    main_menu()


# builds a menu from an array or dictionary and presents the user with a numeric choice, returns that selection
def display_options(options, prompt):
    lookup_dict = {}
    for index, item in enumerate(options):
        print("[" + str(index+1) + "] - " + item)
        if type(options) == dict:
            lookup_dict[index + 1] = item
    while True:
        try:
            selection = int(input(prompt))
        except ValueError:
            print("Selection must be a number")
            continue
        if selection < 1 or selection > len(options) + 1:
            print("Choose a number from the list")
            continue
        else:
            break
    if type(options) == dict:
        return lookup_dict[selection]
    else:
        return selection


# generates user id which is the last 4 of the buyers last name and their zip code separated by an underscore
def gen_id(full_name,addr):
    name_list = full_name.split(" ")
    lname = name_list[-1]
    zip = addr[-5:]
    return lname[-4:].upper() + "_" + zip


# allow user to select make and model from available car data
def get_car():
    tmp_make = display_options(car_data, "Select a make: ")
    tmp_model = car_data.get(tmp_make)[display_options(car_data.get(tmp_make), "Select a model: ")-1]
    return tmp_make + " " + tmp_model


# calculates the total price including taxes and fees
def calculate_total(price, tax):
    return round(price + tax + fees.get("prep fee") + fees.get("license fee"),2)


# calculates the tax due based on the price of the car and the tax rate in the settings file
def calculate_tax(price):
    tax_rate = fees.get("tax rate") * 0.01
    return round(tax_rate * price, 2)


# get and validate the buyers name
def validate_name():
    tmp_fname = required_string("Buyers first name: ")
    tmp_lname = required_string("Buyers last name: ")
    return tmp_fname + " " + tmp_lname


# get and validate the buyers address
def validate_addr():
    tmp_street_addr = required_string("Buyers street address: ")
    tmp_city = required_string("Buyers city: ")
    tmp_state = required_string("Buyers state code: ", required_length=2)
    tmp_zip = required_string("Buyers zip code: ", required_length=5)
    return tmp_street_addr + ", " + tmp_city + ", " + tmp_state + " " + tmp_zip


# get and validate the buyers phone
def validate_phone(required_length=12):
    while True:
        tmp_phone = required_string("Buyers phone number (XXX-XXX-XXXX): ")
        if required_length != 0 and len(tmp_phone) != required_length:
            print("Must be {} characters".format(required_length))
            continue
        if tmp_phone[3] != "-" or tmp_phone[7] != "-":
            print("Must include dashes XXX-XXX-XXXX")
            continue
        tmp_phone = tmp_phone.split("-")
        if not tmp_phone[0].isnumeric() or not tmp_phone[1].isnumeric() or not tmp_phone[2].isnumeric():
            print("Must be numeric")
        else:
            break
    return "(" + tmp_phone[0] + ") " + tmp_phone[1] + "-" + tmp_phone[2]


# gets and validates floats
def validate_float(data_name, allow_zero=False):
    while True:
        try:
            tmp_float = float(input("Input " + data_name + ": "))
        except ValueError:
            print(data_name + " must be a number")
            continue
        if tmp_float < 1 and not allow_zero:
            print(data_name + " must be greater than 0")
            continue
        else:
            break
    return round(tmp_float,2)


# gets a string from the user and insures it meets set specifications
def required_string(prompt, max_length=25, required_length=0):
    while True:
        tmp = input(prompt)
        if required_length != 0 and len(tmp) != required_length:
            print("Must be {} characters".format(required_length))
            continue
        if len(tmp) == 0:
            print("Must not be blank")
            continue
        if len(tmp) > max_length:
            print("Cannot be longer than {} characters".format(max_length))
            continue
        else:
            break
    return tmp


# creates required directories if they do not already exist
def create_directories():
    if not os.path.exists("./reports"):
        os.makedirs("./reports")
    if not os.path.exists("./settings"):
        os.makedirs("./settings")


create_directories()
get_fees()
main_menu()

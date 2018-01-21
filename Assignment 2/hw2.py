import pickle

"""
Gather the following user input and store each item as a variable:
Car Make/Model
Purchase Price
After the user inputs the above information, your program should add the following values to the sale price:
Sales tax as a percent of sale price
Licensing fee
Dealer prep fee
Calculate total cost (as a float)
Assign the car a unique ID composed of the last four letters of the purchaser"s last name and their area code, separated by an underscore
Print out the information to the screen, with the same line breaks as shown in the example below
"""
car_makes = ["Chevrolet", "Ford", "Nissan", "Toyota"]

car_models = {
    "Chevrolet": ["Camaro", "Corvette", "Cruze", "Malibu", "Sonic", "Volt"],
    "Ford": ["Edge", "Focus", "Fusion", "Fusion Hybrid", "Mustang", "Taurus"],
    "Nissan": ["370Z", "Altima", "Leaf", "Maxima", "Murano", "Sentra"],
    "Toyota": ["86", "Avalon", "Camry", "Corolla", "Prius", "Yaris"]
}

report_template = """Hello {}!

Thank you for your purchase of a {}. Following is a break down of your total price:

Sales Price: ${}

Tax: ${}

Licensing Fee: ${}

Dealer Prep Fee: ${}

Total Price: ${}

You have been assigned an ID number of BIN_503. Please refer to this ID number if you have any questions"""


# present user with menu options new report, load saved report, exit program
def main_menu():
    print("-- Main menu --\n[1] - New report\n[2] - Load report\n[3] - Help\n[4] - Edit tax and fees\n[5] - Quit")
    choice = input("Choose an option: ")
    if choice == "1":
        new_report()
    elif choice == "2":
        load_report()
    elif choice == "3":
        script_help()
    elif choice == "4":
        edit_fees()
    elif choice == "5":
        print("Exiting...")
        exit(0)
    else:
        print("Invalid input")
        main_menu()


# sets the sales tax, licensing fee, and dealer prep fee
def set_fees():
    try:
        fee_data_in = open("fees.txt", "rb")
        global fees
        fees = pickle.load(fee_data_in)
        fee_data_in.close()
    except IOError:
        print("Fees not found. Please set fees.")
        fee_data_out = open("fees.txt", "wb")
        tax_rate = validate_float("tax rate",True)
        prep_fee = validate_float("preparation fee",True)
        license_fee = validate_float("license fee", True)
        fee_dict = {"tax_rate": tax_rate, "prep_fee": prep_fee, "license_fee": license_fee}
        pickle.dump(fee_dict, fee_data_out)
        fee_data_out.close()
        set_fees()


# sets the sales tax, licensing fee, and dealer prep fee
def edit_fees():
    try:
        fee_data_in = open("fees.txt", "rb")
        global fees
        fees = pickle.load(fee_data_in)
        print(fees.get("tax_rate"))
        fee_data_in.close()
    except IOError:
        #fee_data_out = open("fees.txt", "wb")
        tax_rate = validate_float("tax rate",True)
        prep_fee = validate_float("preparation fee",True)
        license_fee = validate_float("license fee", True)
        fee_dict = {"tax_rate": tax_rate, "prep_fee": prep_fee, "license_fee": license_fee}
        #pickle.dump(fee_dict, fee_data_out)
        #fee_data_out.close()
        #set_fees()


# start a new report
def new_report():
    print("-- New report --")
    report_details()
    pass


# gather details such as user, car, and pricing
def report_details():
    buyer_name = validate_name()
    buyer_addr = validate_addr()
    #buyer_phone = validate_phone()
    buyer_phone = "(912) 247-4965"
    #car = get_car()
    car = "Chevrolet Camaro"
    #car_price = validate_float("car price")
    car_price = 1000.00
    print_report(buyer_name, buyer_addr, buyer_phone, car, car_price)


# saves completed report to a file, file name is the unique ID
def save_report():
    print("save_report")
    pass


# deletes active report and returns user to the main menu
def delete_report():
    print("delete_report")
    pass


# loads a saved report from a file, file name is the unique ID
def load_report():
    print("load_report")
    pass


# print report to the screen
def print_report(buyer_Name,buyer_Addr,buyer_Phone,car,car_price):
    print(report_template.format(buyer_Name, car, car_price, 100, 100, 100, 1300))
    pass


# edit details of the active report
def edit_report():
    print("edit_report")
    pass


# get and validate the buyers name
def validate_name():
    # tmp_fname = required_string("Buyers first name: ")
    # tmp_lname = required_string("Buyers last name: ")
    tmp_fname = "Colton"
    tmp_lname = "Williams"
    return tmp_fname + " " + tmp_lname


# get and validate the buyers address
def validate_addr():
    # tmp_street_addr = required_string("Buyers street address: ")
    # tmp_city = required_string("Buyers city: ")
    # tmp_state = required_string("Buyers state code: ", required_length=2)
    # tmp_zip = required_string("Buyers zip code: ", required_length=5)
    tmp_street_addr = "2400 Elliott Ave Apt 322"
    tmp_city = "Seattle"
    tmp_state = "WA"
    tmp_zip = "98121"
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


# allow user to select make and model from available car data
def get_car():
    for index, make in enumerate(car_makes):
        print("[" + str(index+1) + "] - " + make)
    while True:
        try:
            selection = int(input("Select a make: "))
        except ValueError:
            print("Selection must be a number")
            continue
        if selection < 1 or selection > len(car_makes) + 1:
            print("Choose a number from the list")
            continue
        else:
            break
    tmp_make = car_makes[selection-1]
    for index, model in enumerate(car_models.get(tmp_make)):
        print("[" + str(index + 1) + "] - " + model)
    while True:
        try:
            selection = int(input("Select a model: "))
        except ValueError:
            print("Selection must be a number")
            continue
        if selection < 1 or selection > len(car_makes) + 1:
            print("Choose a number from the list")
            continue
        else:
            break
    tmp_model = car_models.get(tmp_make)[selection-1]
    return tmp_make + " " + tmp_model


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
    return tmp_float


# print out details about this script
def script_help():
    print("script_help")
    pass


set_fees()
main_menu()

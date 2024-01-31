#This is the file to hold the functions for user input.
#@auther Jiang Zhaorui

#test int input
def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

#test float input
def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

#test boolean input
def get_boolean_input(prompt):
    while True:
        try:
            value = bool(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

#test string input
def get_string_input(prompt):
    value = input(prompt)
    return value

#display the menu in dictionary form
def display_menu(menu_options):
    for key, option in menu_options.items():
        print(f"{key}. {option}")

#check the corresponding key in dictionary whether is right
def get_valid_menu_choice(menu_options):
    valid_choices = menu_options.keys()
    while True:
        choice = get_string_input("Enter your choice: ")
        if choice in valid_choices:
            return choice
        else:
            print("Invalid choice. Please try again.")
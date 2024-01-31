#This is the main file which will hold the Washing Machine code.
#@auther Jiang Zhaorui

#import py files and packages
import user_input as ui
from pynput import keyboard
import sys, os,time

# Global variables for washing machine and "tags"
water_temp = 20
water_amount = 10.0
rotation_speed = 600
spin_duration = 15
alternating_duration = 3
alternating_spin_repeat = 5
choice = "0"
type_choice = "0"
choice_tempt = "0"
tag = True

# Menu options / level 1 menu
main_menu_options = {
    "1": ("Quick wash"),
    "2": ("Standard wash"),
    "3": ("Thorough wash"),
    "4": ("Rinse and spin"),
    "5": ("Spin"),
    "6": ("Exit")
}

# the function used to track keyboard
def on_press(key):
    global tag
    tag = False # when there have input from keyboard, give the stop commend by using tag
    print("Washing canceled")
    print("Please be patient to wait for backing to main menu again")
    sys.stdout = open(os.devnull, 'w')

# Washing machine functions

#heat water washing machine function
def heat_water(temperature):
    current_temp = 20  # original temperature
    while current_temp < temperature:
        if tag:
            current_temp += 1 # each time temperature add 1
            print(f"Heating water: {current_temp} degrees")
            time.sleep(0.1)
        else:
            current_temp = temperature
#add water washing machine function
def add_water(amount):
    max_water = 10.0
    current_water = 0.0 # original water amount
    while current_water < amount and current_water < max_water:
        if tag:
            current_water += 0.5
            print(f"Adding water: {current_water} liters")
            time.sleep(0.1)
        else:
            current_water = max_water
#open drain washing machine function
def open_drain():
    if tag:
        print("Drain is open") # open the drain

#close drain washing machine function
def close_drain():
    if tag:
        print("Drain is close") # close the drain

#spin washing machine function
def spin(speed, duration):
    current_spin = 0
    remaining_spin = duration*speed # total spin number using 0.1s for each minute
    while remaining_spin > 0:
        if tag:
            current_spin += speed
            remaining_spin -= speed
            print(f"For each minute, Spinning: Speed={speed} RPM, Current Spin={current_spin}, Remaining={remaining_spin}")
            time.sleep(0.1)
        else:
            current_spin = duration
            remaining_spin = 0

#alternating spin washing machine function
def alternating_spin(duration, repeat):
    for _ in range(repeat):
        if tag:
            print("Spinning clockwise")
            for _ in range(duration):
                if tag:
                    print("Clockwise spin")
                    time.sleep(0.1)
                else:
                    break
            print("Spinning counterclockwise")
            for _ in range(duration):
                if tag:
                    print("Counterclockwise spin")
                    time.sleep(0.1)
                else:
                    break
        else:
            break

#lauch the machine and recieve exit command to exit
def launch_and_exit_machine():
    global type_choice
    #display the level 1 menu
    ui.display_menu(main_menu_options)
    type_choice = ui.get_valid_menu_choice(main_menu_options)
    if type_choice == "6":
        print("Exiting...")
        exit()
    else:
        #initialize the parameters
        global water_temp, water_amount, rotation_speed, spin_duration, alternating_duration, alternating_spin_repeat
        water_temp = 20
        water_amount = 10
        rotation_speed = 600
        spin_duration = 15
        alternating_duration = 3
        alternating_spin_repeat = 5

#display the run cycle process
def display_run_cycle():
    global water_temp, water_amount, rotation_speed, spin_duration, alternating_duration, alternating_spin_repeat,tag
    #start on the listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    #choose the type of washing to run cycle
    if type_choice == "1":
        for _ in range(2):
            close_drain()
            heat_water(water_temp)
            add_water(water_amount)
            spin(alternating_spin_repeat, alternating_duration)
            spin(rotation_speed, spin_duration)
            open_drain()
            spin(rotation_speed, spin_duration)
    elif type_choice == "2":
        for _ in range(3):
            close_drain()
            heat_water(water_temp)
            add_water(water_amount)
            spin(alternating_spin_repeat, alternating_duration)
            spin(rotation_speed, spin_duration)
            open_drain()
            spin(rotation_speed, spin_duration)
    elif type_choice == "3":
        for _ in range(4):
            close_drain()
            heat_water(water_temp)
            add_water(water_amount)
            spin(alternating_spin_repeat, alternating_duration)
            spin(rotation_speed, spin_duration)
            open_drain()
            spin(rotation_speed, spin_duration)
    elif type_choice == "4":
        close_drain()
        heat_water(water_temp)
        add_water(water_amount)
        spin(rotation_speed, spin_duration)
        open_drain()
        spin(rotation_speed, spin_duration)
    elif type_choice == "5":
        open_drain()
        spin(rotation_speed, spin_duration)
        print("Wash completed")
    #end the listener
    listener.stop()

#change the parameters of washing machine
def customize_wash_cycle():
    global water_temp, water_amount, rotation_speed, spin_duration, alternating_duration, alternating_spin_repeat,choice,type_choice,choice_tempt,tag

    #level 2 menu
    wash_options = {
        "1": ("Water Temperature", water_temp),
        "2": ("Water Amount", water_amount),
        "3": ("Rotation Speed", rotation_speed),
        "4": ("Spin Duration", spin_duration),
        "5": ("Alternating Duration", alternating_duration),
        "6": ("Alternating Spin Repeat", alternating_spin_repeat),
        "7": ("Back"),
        "8": ("Run cycle")
    }

    #level 3 menu
    end_menu_options = {
        "1": ("Save"),
        "2": ("Back"),
    }

    #display the level 2 menu
    ui.display_menu(wash_options)
    choice = ui.get_valid_menu_choice(wash_options)

    # revise the parameters for the washing machine in different situations
    if choice == "1":
        print("Available options for Water Temperature: 1: 20, 2: 30, 3: 40, 4: 50, 5: 60")
        water_temp_tempt = ui.get_valid_menu_choice({"1": 20, "2": 30, "3": 40, "4": 50, "5": 60})
        ui.display_menu(end_menu_options)
        choice_tempt = ui.get_valid_menu_choice(end_menu_options)
        #reserve the revised value
        if choice_tempt == "1":
            water_temp = {"1": 20, "2": 30, "3": 40, "4": 50, "5": 60}.get(water_temp_tempt)
    elif choice == "2":
        print("Available options for Water Amount: 1: 2.5, 2: 5.0, 3: 7.5, 4: 10")
        water_amount_tempt = ui.get_valid_menu_choice({"1": 2.5, "2": 5.0, "3": 7.5, "4": 10.0})
        ui.display_menu(end_menu_options)
        choice_tempt = ui.get_valid_menu_choice(end_menu_options)
        #reserve the revised value
        if choice_tempt == "1":
            water_amount = {"1": 2.5, "2": 5.0, "3": 7.5, "4": 10.0}.get(water_amount_tempt)
    elif choice == "3":
        print("Available options for Rotation Speed: 1: 400, 2: 500, 3: 600, 4: 700, 5: 800")
        rotation_speed_tempt = ui.get_valid_menu_choice({"1": 400, "2": 500, "3": 600, "4": 700, "5": 800})
        ui.display_menu(end_menu_options)
        choice_tempt = ui.get_valid_menu_choice(end_menu_options)
        #reserve the revised value
        if choice_tempt == "1":
            rotation_speed = rotation_speed_tempt
    elif choice == "4":
        print("Available options for Spin Duration: 1: 5, 2: 7, 3: 10, 4: 15")
        spin_duration_tempt = ui.get_valid_menu_choice({"1": 5, "2": 7, "3": 10, "4": 15})
        ui.display_menu(end_menu_options)
        choice_tempt = ui.get_valid_menu_choice(end_menu_options)
        #reserve the revised value
        if choice_tempt == "1":
            spin_duration = {"1": 5, "2": 7, "3": 10, "4": 15}.get(spin_duration_tempt)
    elif choice == "5":
        print("Available options for Alternating Duration: 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10")
        alternating_duration_tempt = ui.get_valid_menu_choice({"1": 1, "2": 2, "3": 3, "4": 4, "5":5, "6": 6,"7": 7, "8": 8, "9": 9, "10": 10})
        ui.display_menu(end_menu_options)
        choice_tempt = ui.get_valid_menu_choice(end_menu_options)
        #reserve the revised value
        if choice_tempt == "1":
            alternating_duration = {"1": 1, "2": 2, "3": 3, "4": 4, "5":5, "6": 6,"7": 7, "8": 8, "9": 9, "10": 10}.get(alternating_duration_tempt)
    elif choice == "6":
        print("Available options for Alternating Spin Repeat: 1: 5, 2: 6, 3: 8, 4: 10, 5: 15, 6: 20")
        alternating_spin_repeat_tempt = ui.get_valid_menu_choice({"1": 5, "2":6, "3":8, "4":10, "5":15, "6":20})
        ui.display_menu(end_menu_options)
        choice_tempt = ui.get_valid_menu_choice(end_menu_options)
        #reserve the revised value
        if choice_tempt == "1":
            alternating_spin_repeat = {"1": 5, "2":6, "3":8, "4":10, "5":15, "6":20}.get(alternating_spin_repeat_tempt)
    #back to the level 1 menu
    elif choice == "7":
        launch_and_exit_machine()
    #start to run the washing cycle
    elif choice == "8":
        display_run_cycle()
        tag = True
        sys.stdout = sys.__stdout__
        print()

# Main program loop
while True:
    #start running into level menu
    launch_and_exit_machine()
    customize_wash_cycle()
    #make the level 3 menu nack to level 2 menu
    while choice != "8":
        if choice_tempt == "1" or "2":
            customize_wash_cycle()
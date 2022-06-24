# Miniature Hotel Management System
#!/usr/bin/env python3
import sys
import os
import time
import datetime
import sqlite3
import pandas as pd
from datetime import timedelta
from sqlalchemy import create_engine
from tabulate import tabulate
from colorama import Fore, init
init(autoreset=True)

banner = """


                ██████╗  ██████╗  ██████╗ ███╗   ███╗    ██████╗  ██████╗  ██████╗ 
                ██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║    ╚════██╗██╔═████╗██╔════╝ 
                ██████╔╝██║   ██║██║   ██║██╔████╔██║     █████╔╝██║██╔██║███████╗ 
                ██╔══██╗██║   ██║██║   ██║██║╚██╔╝██║     ╚═══██╗████╔╝██║██╔═══██╗
                ██║  ██║╚██████╔╝╚██████╔╝██║ ╚═╝ ██║    ██████╔╝╚██████╔╝╚██████╔╝ 
                ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ 
                                                            
                                    HOTEL MANAGEMENT SYSTEM       
"""

connection = sqlite3.connect('hotel_db.db')
cursor = connection.cursor() # Connection for reading and manipulating database
cnx = create_engine('sqlite:///hotel_db.db').connect() # SQL Alchemy DB connection for Pandas input(dataframe) which is depended on by Tabulate

# Function to clear CLI screen
def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

# Function to print banner
def print_banner(banner_):
    clear()
    banner_ = banner_.split('\n')
    for i in banner_:
        time.sleep(0.01)
        print(Fore.MAGENTA +i)
    print(Fore.RESET + '\n\n\n')

# Function to print string line by line slowly
def fancy_print(arr):
    for i in arr:
        time.sleep(0.1)
        print(i)

# Function to authenticate Admin
def authenticate(password):
    password_input = input("Enter Admin password(password): ")
    if password_input.lower() == password[0] or password_input == "":
        clear()
        welcome_text = """
                                                           __ 
                 _ _ _ _____ __    _____ _____ _____ _____|  |
                | | | |   __|  |  |     |     |     |   __|  |
                | | | |   __|  |__|   --|  |  | | | |   __|__|
                |_____|_____|_____|_____|_____|_|_|_|_____|__|
                                                            
        """
        fancy_print(welcome_text.split('\n'))
        load_menu()
    else:
        print('Password is "password"')
        authenticate(password)

def get_customer():
    while True:
        clear()
        print("\nBOOKING INFORMATION:\n\n")
        fancy_print("NEW OR EXISTING CUSTOMER?\n\n1. Existing customer\n\n2. New customer\n".split('\n'))
        option = input("select preferred option from the list: ")

        if option == '1':
            clear()
            print(f"{'CUSTOMERS': ^58}")
            guests = pd.read_sql_query('''SELECT * FROM guests''', cnx)
            guests.set_index('guest_id', inplace=True)
            fancy_print(tabulate(guests, headers='keys', tablefmt='fancy_grid').split('\n'))

            while True:
                guest_id = int(input("\nENTER GUEST ID TO CONTINUE WITH YOUR BOOKING: "))
                if guest_id in guests.index.tolist():
                    guest_name = guests.loc[guest_id, 'guest_name']
                    clear()
                    # print(f"\nName of Customer: {guest_name}\n")
                    return [guest_id, guest_name]
                else:
                    print("\nYou entered a wrong guest ID!")

        elif option == '2':
            clear()
            while True:
                guest_name = input("\nEnter guest's name(e.g Maximus Dre): ")
                if guest_name.replace(' ', '').isalpha():
                    print(f"Name: {guest_name}\n")
                    break
                else:
                    print("Incorrect format(Only letters are allowed)\n")
                    

            while True:
                guest_phone = input("Enter guest's phone(e.g 08123456789): ")
                if guest_phone.isdigit():
                    print(f"Phone: {guest_phone}\n")
                    break
                else:
                    print("Incorrect format(Only digits are allowed)\n")

            while True:
                guest_gender = input("Enter guest's gender(enter M or F): ")
                if guest_gender.upper() == 'M' or guest_gender.upper() == 'F':
                    guest_gender = guest_gender.upper()
                    print(f"Gender: {guest_gender}\n")
                    break
                else:
                    print("Incorrect format(Enter M or F)\n")

            connection.execute("INSERT INTO guests(guest_name, phone_number, gender) VALUES(?,?,?)", (guest_name, guest_phone, guest_gender))
            connection.commit()

            guest_id = connection.execute("SELECT max(guest_id) FROM guests").fetchone()[0]
            return [guest_id, guest_name]
        else:
            print("You entered a wrong option(Enter 1 or 2)")
            continue

def select_room(room_type):
    print('\n\n\n')
    if room_type == 'regular':
        print(f"{'AVAILABLE ROOMS(REGULAR)': ^76}")
        available_rooms = pd.read_sql_query(f'''SELECT room_id, room_num, room_type, room_floor, room_price FROM rooms WHERE room_availability = 1 AND room_type = "regular"''', cnx)

    else: # room_type == 'VIP'
        print(f"{'AVAILABLE ROOMS(VIP)': ^80}")
        available_rooms = pd.read_sql_query('''SELECT room_id, room_num, room_type, room_floor, room_price FROM rooms WHERE room_availability = 1 AND room_type = "VIP"''', cnx)
        
    available_rooms.set_index('room_id', inplace=True)
    fancy_print(tabulate(available_rooms, headers='keys', tablefmt='fancy_grid').split('\n'))

    while True:
        room_to_book = input("\n\nENTER ROOM ID TO BOOK ROOM: ")
        room_id = int(room_to_book)
        if room_id in available_rooms.index.tolist():
            room_num = available_rooms.loc[room_id, 'room_num']
            room_price = available_rooms.loc[room_id, 'room_price']
            clear()
            print(f"\nYou selected room {room_num}")
            return [room_id, room_num, room_price]
        else:
            print("You entered a wrong room ID")

def select_hall(hall_type):
    print('\n\n\n')
    if hall_type == 'conference':
        print(f"{'AVAILABLE HALLS(Conference)': ^80}")
        available_halls = pd.read_sql_query('''SELECT hall_id, hall_name, hall_type, hall_price FROM halls WHERE hall_availability = 1 AND hall_type = "conference"''', cnx)

    else: # hall_type == 'dining'
        print(f"{'AVAILABLE HALLS(Dining)': ^80}")
        available_halls = pd.read_sql_query('''SELECT hall_id, hall_name, hall_type, hall_price FROM halls WHERE hall_availability = 1 AND hall_type = "dining"''', cnx)
        
    available_halls.set_index('hall_id', inplace=True)
    fancy_print(tabulate(available_halls, headers='keys', tablefmt='fancy_grid').split('\n'))

    while True:
        hall_to_book = input("\n\nENTER HALL ID TO BOOK A HALL: ")
        hall_id = int(hall_to_book)
        if hall_id in available_halls.index.tolist():
            hall_name = available_halls.loc[hall_id, 'hall_name']
            hall_price = available_halls.loc[hall_id, 'hall_price']
            clear()
            print(f"\nYou selected Hall {hall_name}")
            return [hall_id, hall_name, hall_price]
        else:
            print("\nYou entered a wrong hall ID")

def get_stay_duration():
    while True:
        stay_duration = input("How many day's are you staying( 1 - 30): ")
        if stay_duration.isdigit():
            stay_duration = int(stay_duration)
            if 0 < stay_duration <= 30: # stay_duration  > 0 days and stay_duration less than 30 days
                return stay_duration
            else:
                print("Incorrect format(Enter between 1 and 30)\n")
                continue
        else:
            print("Incorrect format(Must be a digit)\n")

def book_room(room_type):
    clear()
    #------------------------------------------#ROOM SELECTION#------------------------------------------#
    room = select_room(room_type)
    room_id = room[0]
    room_num = room[1]
    room_price = room[2]
    #------------------------------------------#RETRIEVE CUSTOMER INFO#------------------------------------------#
    guest_info = get_customer()
    guest_id = guest_info[0]
    guest_name = guest_info[1]
    #------------------------------------------#GET STAY DURATION(BETWEEN 1 - 30)#------------------------------------------#
    stay_duration = get_stay_duration()
    #------------------------------------------#GET BOOKING PERIOD#------------------------------------------#
    date_booked = datetime.date.today()
    expire_date = date_booked + timedelta(days=int(stay_duration))
    #--------------------------------------------------------------------------------------------------------------------------#

    connection.execute("INSERT INTO booked_rooms(room_id, guest_id, guest_checked_in, date_booked, date_expire) VALUES(?,?,?,?,?)", (room_id, guest_id, 0, date_booked, expire_date))
    connection.execute("UPDATE rooms SET room_availability=0 WHERE room_id=:roomid", {'roomid': room_id})

    clear()
    print("\nWould you like to check in now?\n\n1. Yes\n\n2. No")
    while True:
        option = input("\nselect preferred option: ")
        if option == '1' or option.upper() == 'Y' or option.upper() == 'YES':
            connection.execute("UPDATE booked_rooms SET guest_checked_in=1 WHERE room_id =:roomid", {'roomid': room_id})
            break
        elif option == '2' or option.upper() == 'N' or option.upper() == 'NO':
            pass
        else:
            print("\nInvalid input(Enter 1 or 2)")

    connection.commit()
    receipt_info = [['Customer', guest_name], ['Room number', room_num], ['Stay duration', str(stay_duration) + ' Day(s)'], ['Date booked', date_booked], ['Cost of Room/Day', 'N' + str(room_price)], ["Total", 'N' + str(room_price * stay_duration)]]
    generate_receipt(receipt_info)

def book_hall(hall_type):
    clear()
    #------------------------------------------#HALL SELECTION#------------------------------------------#
    hall = select_hall(hall_type)
    hall_id = hall[0]
    hall_name = hall[1]
    hall_price = hall[2]
    #------------------------------------------#RETRIEVE CUSTOMER INFO#------------------------------------------#
    guest_info = get_customer()
    guest_id = guest_info[0]
    guest_name = guest_info[1]

    date_booked = datetime.date.today()

    connection.execute("INSERT INTO booked_halls(hall_id, guest_id, date_booked) VALUES(?,?,?)", (hall_id, guest_id, date_booked))
    connection.execute("UPDATE halls SET hall_availability=0 WHERE hall_id=:hallid", {'hallid': hall_id})
    connection.commit()

    receipt_info = [['Customer', guest_name], ['Hall name', 'Hall ' +str(hall_name)], ['Date booked', date_booked], ["Total", 'N' + str(hall_price)]]
    generate_receipt(receipt_info)

def book():
    clear()
    fancy_print("\n\nBOOKING OPTIONS:\n\n1. Rooms\n2. Halls\n".split('\n'))
    b_option = input("select preferred option from the list: ")

    if b_option == '1':
        clear()
        while True:
            fancy_print("\n\nROOM TYPE:\n\n1. Regular\n2. VIP\n".split('\n'))
            room_type = input("select preferred option from list: ")

            if room_type == '1':
                book_room("regular")
                enquire()
            elif str(room_type) == '2':
                book_room("VIP")
                enquire()
            else:
                print("Invalid room type (Enter 1 or 2): ")

    elif b_option == '2':
        clear()
        while True:
            fancy_print("\nHALL TYPE:\n\n1. Conference\n2. Dining\n".split('\n'))
            hall_type = input("select preferred option from list: ")
            if hall_type == '1':
                book_hall("conference")
                enquire()
            elif hall_type == '2':
                book_hall("dining")
                enquire()
            else:
                print("Invalid hall option (Enter 1 or 2)")
    else:
        print("Invalid option (Enter 1 or 2): ")
        book()

def check_in_out():
    clear()
    fancy_print("\n\nCHECK-IN OR CHECK-OUT?\n\n1. Check guest in\n\n2. Check guest out\n\n".split('\n'))
    
    while True:
        option = input("select preferred option from list: ")

        if option == '1':
            unchecked_in_guests = pd.read_sql_query('''SELECT guest_id, room_id, date_booked, date_expire FROM booked_rooms WHERE guest_checked_in=0''', cnx)

            if len(unchecked_in_guests) < 1:
                print("\nAll guests have been checked into their respective rooms.")
                return
            else:
                unchecked_in_guests.set_index("room_id", inplace=True)
                print(f"\n\n{'GUESTS  (NOT CHECKED-IN)': ^76}")
                fancy_print(tabulate(unchecked_in_guests, headers="keys", tablefmt="fancy_grid").split('\n'))

                while True:
                    room_id = input("Enter Room ID to Check guest into: ")
                    room_id = int(room_id)
                    if room_id in unchecked_in_guests.index.tolist():
                        connection.execute("UPDATE booked_rooms SET guest_checked_in=1 WHERE room_id =:roomid", {'roomid': room_id})
                        connection.commit()

                        guest_id = unchecked_in_guests.loc[room_id, 'guest_id']
                        guest_name = connection.execute("SELECT guest_name FROM guests WHERE guest_id=:guestid", {'guestid': int(guest_id)}).fetchone()
                        room_num = connection.execute("SELECT room_num FROM rooms WHERE room_id=:roomid", {'roomid': room_id}).fetchone()
                        print(f"{Fore.GREEN}{guest_name[0]} has been successfully checked into Room {room_num[0]}!{Fore.RESET}")
                        return
                    else:
                        print("\nYou entered a wrong Room ID")
        
        elif option == '2':
            checked_in_guests = pd.read_sql_query('''SELECT guest_id, room_id, date_booked, date_expire FROM booked_rooms WHERE guest_checked_in=1''', cnx)

            if len(checked_in_guests) < 1:
                print("\nAll guests have been checked out.")
                return
            else:
                checked_in_guests.set_index("room_id", inplace=True)
                print(f"\n\n{'GUESTS (CHECKED-IN)': ^76}")
                fancy_print(tabulate(checked_in_guests, headers="keys", tablefmt="fancy_grid").split('\n'))

                while True:
                    room_id = input("\nEnter Room ID to Check guest out from: ")
                    room_id = int(room_id)
                    if room_id in checked_in_guests.index.tolist():
                        connection.execute("UPDATE booked_rooms SET guest_checked_in=0 WHERE room_id =:roomid", {'roomid': room_id})
                        connection.execute("UPDATE rooms SET room_availability=1 WHERE room_id=:roomid", {'roomid': room_id})
                        connection.commit()
                        # connection.execute("DELETE ")

                        guest_id = checked_in_guests.loc[room_id, 'guest_id']
                        guest_name = connection.execute("SELECT guest_name FROM guests WHERE guest_id=:guestid", {'guestid': int(guest_id)}).fetchone()
                        room_num = connection.execute("SELECT room_num FROM rooms WHERE room_id=:roomid", {'roomid': room_id}).fetchone()
                        print(f"\n\n{Fore.GREEN}{guest_name[0]} has been successfully checked out of Room {room_num[0]}!{Fore.RESET}")
                        return
                    else:
                        print("\nYou entered a wrong Room ID")

        else:
            print("Invalid input(Enter 1 or 2)\n")

def generate_receipt(receipt_info):
    print('\n\n')
    print(f"{'RECEIPT': ^34}")
    print(tabulate(receipt_info, tablefmt='grid'))
    guest_name = receipt_info[0][1]
    idd = receipt_info[1][1]
    with open('Receipt for '+guest_name+' ' +str(idd)+'.txt', 'w', encoding='utf8') as output:
        output.write(f"{'Receipt': ^34}\n")
        output.write(tabulate(receipt_info, tablefmt='grid'))

def check_availability():
    clear()
    fancy_print("\n\nCHECK AVAILABILITY:\n\n1. Check room availability\n2. Check hall availability\n".split('\n'))
    b_option = input("select preferred option from the list: ")

    if b_option == '1':
        clear()
        while True:
            available_rooms = pd.read_sql_query("SELECT room_id, room_num, room_type, room_floor, room_price FROM rooms WHERE room_availability = 1", cnx)
            available_rooms.set_index("room_id", inplace=True)
            if len(available_rooms) < 1:
                print(f"{Fore.YELLOW}Rooms are fully booked!{Fore.RESET}")
                return
            print(f"{'AVAILABLE ROOMS': ^50}")
            fancy_print(tabulate(available_rooms, headers='keys', tablefmt="fancy_grid").split('\n'))
            return

    elif b_option == '2':
        clear()
        while True:
            available_halls = pd.read_sql_query("SELECT hall_id, hall_name, hall_type, hall_price FROM halls WHERE hall_availability = 1", cnx)
            available_halls.set_index("hall_id", inplace=True)
            if len(available_halls) < 1:
                print(f"{Fore.YELLOW}Halls are fully booked!{Fore.RESET}")
                return
            print(f"{'AVAILABLE HALLS': ^50}")
            fancy_print(tabulate(available_halls, headers='keys', tablefmt="fancy_grid").split('\n'))
            return

def generate_report():
    clear()
    available_rooms = pd.read_sql_query("SELECT room_id, room_num, room_type, room_floor, room_price FROM rooms WHERE room_availability = 1", cnx)
    available_halls = pd.read_sql_query("SELECT hall_id, hall_name, hall_type, hall_price FROM halls WHERE hall_availability = 1", cnx)
    booked_rooms = pd.read_sql_query("SELECT room_id, room_num, room_type, room_floor, room_price FROM rooms WHERE room_availability = 0", cnx)
    booked_halls = pd.read_sql_query("SELECT hall_id, hall_name, hall_type, hall_price FROM halls WHERE hall_availability = 0", cnx)
    guests = pd.read_sql_query("SELECT * FROM guests", cnx)
    curr_time = datetime.datetime.now().strftime("%H:%M:%S")

    fancy_print(f"{'HOTEL REPORT': ^70}\nNumber of available rooms: {len(available_rooms)}\nNumber of booked rooms: {len(booked_rooms)}\nNumber of booked halls: {len(booked_halls)}\nNumber of guests: {len(guests)}\n\n".split('\n'))

    receipt_info = [['Available rooms', len(available_rooms)], ['Available halls', len(available_halls)], ['Booked rooms', len(booked_rooms)], ['Booked halls', len(booked_halls)], ['Number of guests', len(guests)]]

    with open('Report ' +str(curr_time.split(':')[1])+'.txt', 'w', encoding='utf8') as output:
        output.write(f"{'Report': ^34}\n")
        output.write(tabulate(receipt_info, tablefmt='grid'))
    return

def load_menu():
    while True:
        fancy_print(f"\n\nSelect an option from the list(Enter the option number):\n\n1. BOOKING/RESERVATION({Fore.GREEN}1{Fore.RESET})\n\n2. CHECK GUEST IN OR OUT({Fore.GREEN}2{Fore.RESET})\n\n3. CHECK ROOM/HALL AVAILABILITY({Fore.GREEN}3{Fore.RESET})\n\n4. GENERATE REPORT({Fore.GREEN}4{Fore.RESET})\n\n".split('\n'))
        option = input(Fore.GREEN + "OPTION: " + Fore.RESET)
        if option == '1':
            book()
            enquire()
        if option == '2':
            check_in_out()
            enquire()
        if option == '3':
            check_availability()
            enquire()
        if option == '4':
            generate_report()
            enquire()
        else:
            print("Invalid option(Enter between 1 to 5)")
            time.sleep(1)
            clear()

def enquire():
    while True:
        # clear()
        # print('\n'+ '#'*20)
        print(f"\n{Fore.YELLOW}Would you like to return to the Main menu or Exit?\n1. Main menu\n2. Exit\n{Fore.RESET}")
        option = input("Enter preferred option: ")
        if option == '1':
            home()
        elif option == '2':
            print('\n\nQuiting', end='')
            for i in '...':
                time.sleep(0.1)
                print(i, end='')
            clear()
            sys.exit()
        else:
            print("Invalid input (Enter 1 or 2)")

def home():
    print_banner(banner)
    load_menu()

def main():
    print_banner(banner)
    cursor.execute("SELECT password FROM admin_accounts")
    password = cursor.fetchone()
    authenticate(password)

if __name__ == '__main__':
    # main()
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Execution Interrupted!{Fore.RESET}")
        time.sleep(0.2)
        clear()
        sys.exit(0)

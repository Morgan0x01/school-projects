# For Generating Hotel's Sqlite3 Database
#!/usr/bin/env python3
import sqlite3


connection = sqlite3.connect('hotel_db.db')
cursor = connection.cursor()

rooms = [
    (1,101,0,"regular","1st floor",5000),
    (2,102,0,"regular","1st floor",5000),
    (3,103,1,"regular","1st floor",5000),
    (4,104,1,"regular","1st floor",5000),
    (5,105,1,"regular","1st floor",5000),
    (6,201,1,"regular","2nd floor",5000),
    (7,202,1,"regular","2nd floor",5000),
    (8,203,1,"regular","2nd floor",5000),
    (9,204,1,"regular","2nd floor",5000),
    (10,205,1,"regular","2nd floor",5000),
    (11,301,0,"VIP","3rd floor",15000),
    (12,302,0,"VIP","3rd floor",15000),
    (13,303,1,"VIP","3rd floor",15000),
    (14,304,1,"VIP","3rd floor",15000),
    (15,305,1,"VIP","3rd floor",15000)
]

halls = [
    (1,"A",0,"conference",25000),
    (2,"B",1,"conference",25000),
    (3,"C",1,"conference",25000),
    (4,"D",1,"dining",25000),
    (5,"E",0,"dining",25000),
    (6,"F",1,"dining",25000)
]

guests = [
    (1,"John Doe","08123456789","M"),
    (2,"Mary Doe","07123456789","F"),
    (3,"Elon Musk","09123456789","M"),
    (4,"Pavel Durov","08023456789","M"),
    (5,"Operah Winfrey","07023456789","F")
]

admin_accounts = [
    ("Admin","password", "2021-09-07")
]

booked_rooms = [
    (1,1,1,"2021-09-06","2021-09-07"),
    (11,3,0,"2021-09-06","2021-09-07"),
    (12,4,1,"2021-09-06","2021-09-07"),
    (2,2,0,"2021-09-06","2021-09-07"),
]

booked_halls = [
    (1,3,"2021-09-06"),
    (5,4,"2021-09-06")
]

cursor.execute("CREATE TABLE rooms(room_id integer not null primary key autoincrement, room_num integer, room_availability smallint, room_type text, room_floor text, room_price integer)")
cursor.executemany("INSERT INTO rooms VALUES (?,?,?,?,?,?)", rooms)

cursor.execute("CREATE TABLE halls(hall_id integer not null primary key autoincrement, hall_name varchar, hall_availability smallint, hall_type text, hall_price integer)")
cursor.executemany("INSERT INTO halls VALUES (?,?,?,?,?)", halls)

cursor.execute("CREATE TABLE guests(guest_id integer not null primary key autoincrement, guest_name text, phone_number text, gender varchar)")
cursor.executemany("INSERT INTO guests VALUES (?,?,?,?)", guests)

cursor.execute("CREATE TABLE admin_accounts(username text, password text, last_login text)")
cursor.execute("INSERT INTO admin_accounts VALUES('Admin','password','2021-09-07')")

cursor.execute("CREATE TABLE booked_rooms(room_id integer not null, guest_id integer, guest_checked_in smallint, date_booked text, date_expire text)")
cursor.executemany("INSERT INTO booked_rooms VALUES(?,?,?,?,?)", booked_rooms)

cursor.execute("CREATE TABLE booked_halls(hall_id integer not null primary key autoincrement, guest_id integer, date_booked text)")
cursor.executemany("INSERT INTO booked_halls VALUES (?,?,?)", booked_halls)

print("ROOMS TABLE:")
for row in cursor.execute("SELECT * FROM rooms"):
    print(row)

print("\n\nHALLS TABLE:")
for row in cursor.execute("SELECT * FROM halls"):
    print(row)

print("\n\nGUESTS TABLE:")
for row in cursor.execute("SELECT * FROM guests"):
    print(row)

print("\n\nADMIN ACCOUNTS:")
for row in cursor.execute("SELECT * FROM admin_accounts"):
    print(row)

print("\n\nBOOKED ROOMS:")
for row in cursor.execute("SELECT * FROM booked_rooms"):
    print(row)

print("\n\nBOOKED HALLS:")
for row in cursor.execute("SELECT * FROM booked_halls"):
    print(row)

connection.commit()
connection.close()
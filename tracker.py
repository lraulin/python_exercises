#!/usr/bin/env python3
# Uses sqlite to track data such as weight, etc.

import sqlite3
import time

# Uses sqlite to track data such as weight, etc.

import sqlite3
import time

GOLDEN_RATIO = (1 + 5 ** 0.5) / 2  # ≈1.618
ideal_waist_height_ratio = .46
height = 177  # cm
ideal_waist = int(height * ideal_waist_height_ratio)
# measured at the broadest point around the shoulders, just above the nipples
ideal_shoulders = int(height * ideal_waist_height_ratio * GOLDEN_RATIO)

print("Target waist size: {} cm\nTarget shoulder size: {} cm".format(
    ideal_waist, ideal_shoulders))

conn = sqlite3.connect('my_tracker.db')
c = conn.cursor()

# c.execute('''CREATE TABLE waist_size (
#              date DATE NOT NULL, waist_size INTEGER, PRIMARY KEY (date))
# ''')

today = time.strftime("%Y-%m-%d")
print("Today is {}".format(today))

# Check if we want to enter new data for today.
newinput = input("Enter new data? (y/n)\n>")
# If input begins with the letter 'y', the answer is 'yes'. Convert newinput to boolean.
newinput = newinput.lower().strip()[0] == 'y'

if newinput:
    # Get new waist size
    while True:
        try:
            waist = int(input(
                "What is your waist size (in cm) today? (Enter any non-numeric string to skip.)\n>"))
        except ValueError:
            print("Value Error. Enter waist size as a whole number in cm.")
            continue
        else:
            break

    new_waist_data = (today, waist)

    while True:
        try:
            shoulders = int(input(
                "What is your shoulder size (in cm) today? (Enter any non-numeric string to skip.)\n>"))
        except ValueError:
            print("Value Error. Enter waist size as a whole number in cm.")
            continue
        else:
            break

    new_shoulder_data = (today, shoulders)

    try:
        c.execute('''INSERT INTO waist_size
                 VALUES (?, ?)''', new_waist_data)
    except sqlite3.Error as e:
        print(e)

    try:
        c.execute('''INSERT INTO shoulder_size
                 VALUES (?, ?)''', new_shoulder_data)
    except sqlite3.Error as e:
        print(e)
else:
    c.execute('''SELECT waist_size
                         FROM waist_size
                         WHERE date =(
                               SELECT MAX(date) FROM waist_size);''')
    waist = c.fetchone()[0]
    print("Most recent waist size: {} cm".format(waist))
    c.execute('''SELECT shoulder_size
                         FROM shoulder_size
                         WHERE date =(
                               SELECT MAX(date) FROM shoulder_size);''')
    shoulders = c.fetchone()[0]
    print("Most recent shoulder width: {} cm".format(shoulders))


adonis_index = shoulders / waist
waist_height_ratio = waist / height
print("Your current Adonis Index is {:.2f}".format(adonis_index))
print(
    "Your current waist-to-height ratio is {:.2f}".format(waist_height_ratio))
if waist_height_ratio >= .53:
    print("""
You're fat as fuck! Your health is at risk and you look disgusting!
You have the risk equivalent to BMI of 25!
Do something about it, fatty!
    """)
elif waist_height_ratio >= .51:
    print("""
You're still fat! You still have risk equivalent to BMI of 25!
Lose more weight, fatso!
    """)
elif waist_height_ratio >= .50:
    print("""
You're still fat! Look at that gut! Gross!
    """)
elif waist_height_ratio >= .49:
    print("""
Better, but you're still too fat!
    """)
elif waist_height_ratio >= .48:
    print("""
You're getting there! Keep losing weight!
    """)
elif waist_height_ratio >= .47:
    print("""
Looking good! But don't start pigging out yet!
    """)
else:
    print("""
You are a god among men. Get more muscle, and don't get fat again!
    """)

# print waist_size database
# c.execute("SELECT * FROM waist_size")
# rows = c.fetchall()
# 94

conn.commit()
conn.close()

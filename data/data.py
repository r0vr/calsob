import re
import sqlite3
import os
import sys
import datetime
import time
from datetime import date

conn = sqlite3.connect(
    "data.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
)
cur = conn.cursor()


def initialize_database():
    print("Creating database.")
    cur.execute("""
            CREATE TABLE IF NOT EXISTS userdata(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Substance TEXT NOT NULL,
            QuitDate TIMESTAMP)
                """)
    print("Database created.")


def add_data(substance, lastdate):
    while True:
        substance = input("Please enter the substance: ")
        indate = input("Please enter the date of last use 'yyyymmdd': ")
        try:
            lastdate = datetime.datetime.strptime(indate, "%Y%m%d")

            cur.execute("SELECT MAX (id) FROM userdata")
            result = cur.fetchone()[0]
            new_id = 1 if result is None else result + 1
            cur.execute(
                """INSERT INTO userdata (Substance, QuitDate)
                VALUES (?, ?);""",
                (substance, lastdate),
            )
            conn.commit()
            print(f"New entry added with id {new_id}.")
            break
        except ValueError:
            return "Invalid."


def get_current_date(subcheck):
    while True:
        subcheck = int(
            input("Please enter the id of the substance you want to track: ")
        )
        query = "SELECT * FROM userdata WHERE id = ?"
        cur.execute(query, (subcheck,))
        result = cur.fetchone()[0]
        if result == subcheck:
            subname = "SELECT Substance FROM userdata where id = ?"
            cur.execute(subname, (subcheck,))
            name_result = cur.fetchone()[0]
            print(f"ID {subcheck} is {name_result}.")
            time.sleep(2)
            ques = "SELECT QuitDate FROM userdata WHERE Substance = ?;"
            cur.execute(ques, (name_result,))
            date_result = cur.fetchone()[0]
            print(f"You last used {name_result} on {date_result}")
            time.sleep(2)
            now = date.today()
            findate = (now - date_result.date()).days
            finalprin = print(f"It has been {findate} days. Good work! ")
            return finalprin
        else:
            return "Invalid entry"


def show_all():
    try:
        cur.execute("SELECT * FROM userdata;")
        results = cur.fetchall()
        if not results:
            print("No records found.")
            return

        print("\n" + "=" * 50)
        print("ID | Substance | QuitDate")
        print("-" * 50)

        for row in results:
            id_val = row[0]
            substance = row[1]
            quit_date = row[2]

            if isinstance(quit_date, datetime.datetime):
                formatted_date = quit_date.strftime("%Y-%m-%d")
            else:
                formatted_date = str(quit_date)
            print(f"{id_val} | {substance} | {formatted_date}")
        print("=" * 50)
    except Exception as e:
        print(f"Error retrieving data: {e}")


def remove_entry():
    rem_id = int(
        input("Please enter the id of the substance you wish to remove: "))
    order = "DELETE FROM userdata WHERE id = ?"
    cur.execute(order, (rem_id,))
    conn.commit()
    print("Entry removed.")

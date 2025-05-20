# CalSob - Owen's attempt to both help himself stay off the yayo and fire water.
# Also to make something without having an AI involved at any point.

import os
import json
import sys
import data.data
from pathlib import Path


def setup():
    project_root = os.path.dirname(os.path.abspath(__file__))
    ud_db = Path("data/data.db")
    if ud_db.is_file():
        print("Db file detected.")
        return False
    else:
        data.data.initialize_database()
        print("Database initialized")
        return True


def entry():
    data.data.add_data(None, None)


def date_check():
    data.data.get_current_date(None)


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Environment Setup")
        print("2. Add Substance")
        print("3. Time Tracker")
        print("4. View All")
        print("5. Delete Entry")
        print("6. Quit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            print("You selected Option One")
            setup()
        elif choice == "2":
            print("You selected Option Two")
            entry()
        elif choice == "3":
            print("You selected Option Three")
            date_check()
        elif choice == "4":
            print("You selected Option Four")
            data.data.show_all()
        elif choice == "5":
            print("You selected Option Five")
            data.data.remove_entry()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main_menu()

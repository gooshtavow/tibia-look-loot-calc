# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

# Feel free to contact the repository owner at GitHub

import math
import re
import os
import sys

item_data = []
item_names = set()

def load_csv_into_memory():
    with open ("./sorted_items_and_values.csv", "r") as f:
        for line in f:
            line = line[:-1].split(",")
            object = {
                "name": line[0],
                "plural": line[1],
                "weight": float(line[2]),
                "value": int(line[3]),
                "amount": 0
            }
            item_data.append(object)
            item_names.add(line[0])
            item_names.add(line[1])


def parse_input(input):
    loot_text = None
    if input == "paste.txt":
        loot_text = open("paste.txt", "r")
    else:
        loot_text = input

    itemlist = []
    parsed_item = []

    for line in loot_text:
        item = re.findall(r"You see (\d*)[\s]*([^.\(]+)", line)
        if item:
            item = list(item[0])
            # Now, item[0] holds the amount and item[1] holds item name

            # Remove "a", "an" and whitespaces
            if item[0] == "" and item[1][0] == "a":
                if item[1][1:3] == "n ":
                    item[1] = item[1][3:]
                elif item[1][1] == " ":
                    item[1] = item[1][2:]
            if item[1][-1] == " ":
                item[1] = item[1][:-1]

            # Remove "that..." for rings
            if "that is" in item[1] or "that will" in item[1]:
                aux = ""
                item[1] = item[1].split(" ")
                for word in item[1]:
                    if word == "that":
                        break
                    else:
                        aux = aux + word + " "
                item[1] = aux[:-1]
            if item[0] == "":
                parsed_item.append(item[0])
            else:
                parsed_item.append(int(item[0])) # amount
            parsed_item.append(item[1]) # name

        weight = re.findall(r"weighs? (\d+.\d\d)", line)
        if weight:
            parsed_item.append(float(weight[0])) # weight
            itemlist.append(parsed_item)
            parsed_item = []

    if input == "paste.txt":
        loot_text.close()

    return itemlist


def calculate_value(item_list):
    # item[0] = amount
    # item[1] = name
    # item[2] = weight
    total_value = 0
    for item in item_list:
        if item[1] in item_names:
            singular_item = next((it for it in item_data if it["name"] == item[1]), False)
            if singular_item:
                if math.isclose(item[2], singular_item["weight"], abs_tol=0.001):
                    singular_item["amount"] += 1
                    total_value += singular_item["value"]
                else:
                    singular_item["amount"] += (item[2]/singular_item["weight"])
                    total_value += (item[2]/singular_item["weight"]) * singular_item["value"]
            else:
                plural_item = next((it for it in item_data if (it["plural"] == item[1]) and math.isclose(item[2], item[0] * it["weight"], abs_tol=0.001)), False)
                if plural_item:
                    plural_item["amount"] += item[0]
                    total_value += plural_item["value"] * item[0]
    return int(total_value)

def main():
    try:
        load_csv_into_memory()
    except:
        print("Couldn't load sorted_items_and_values.csv.")
        raise

    # Windows only: use -c to read input from clipboard.
    if os.name == "nt" and len(sys.argv) >= 2 and sys.argv[1] == "-c":
        from tkinter import Tk
        tkinter_root = Tk()
        tkinter_root.withdraw()
        clipboard = tkinter_root.clipboard_get()
        tkinter_root.destroy()

        item_list = parse_input(clipboard.splitlines())
        loot_value = calculate_value(item_list)
    # Or read from "paste.txt"
    else:
        item_list = parse_input("paste.txt")
        loot_value = calculate_value(item_list)

    for item in item_data:
        if item["amount"] != 0:
            print(f'{int(item["amount"])}x {item["name"]}: {int(item["value"] * item["amount"])} gold.')
    print(f'Total value: {loot_value} gold.')

if __name__ == "__main__":
    main()